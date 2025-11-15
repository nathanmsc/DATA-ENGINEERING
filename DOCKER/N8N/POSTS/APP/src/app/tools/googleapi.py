import os
import random
from io import BytesIO
from functools import cached_property
from typing import Optional, Tuple, Dict, Any, Type

import gspread  # type: ignore
from pydantic import BaseModel, Field  # type: ignore
from crewai.tools import BaseTool  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload  # type: ignore
from google.oauth2.service_account import Credentials  # type: ignore
from dotenv import load_dotenv  # type: ignore

# Carrega variáveis do .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# =====================================================
# Google Drive / Sheets Client
# =====================================================
class GoogleDriveClient:
    """Cliente unificado para autenticação e operações com Google Drive e Google Sheets."""

    @cached_property
    def scopes(self) -> list[str]:
        scopes_env = os.getenv("GOOGLE_SCOPES")
        if not scopes_env:
            raise ValueError("⚠️ Variável de ambiente GOOGLE_SCOPES não encontrada no .env")
        return [scope.strip() for scope in scopes_env.split(",")]

    @cached_property
    def credentials(self) -> Credentials:
        print("BASE_DIR:", BASE_DIR)

        credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")


        # Caminho absoluto baseado no diretório /src/app/tools
        credentials_path = os.path.join(BASE_DIR, credentials_file)
        credentials_path = os.path.abspath(credentials_path)
        print("BASE_DIR:", credentials_path)

        if not os.path.exists(credentials_path):
            raise FileNotFoundError(
                f"⚠️ Arquivo de credenciais não encontrado em: {credentials_path}"
            )

        return Credentials.from_service_account_file(credentials_path, scopes=self.scopes)

    @cached_property
    def sheets_client(self):
        """Cliente para Google Sheets via gspread"""
        return gspread.authorize(self.credentials)

    @cached_property
    def drive_service(self):
        """Cliente para Google Drive API"""
        return build("drive", "v3", credentials=self.credentials)

    # ------------------- DRIVE METHODS -------------------
    def download_file(self, file_id: str) -> BytesIO:
        """Baixa um arquivo do Google Drive e retorna como BytesIO."""
        request = self.drive_service.files().get_media(fileId=file_id)
        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.seek(0)
        return fh

    def make_file_public(self, file_id: str) -> str:
        """Define permissão pública e retorna URL direta de download."""
        permission = {"role": "reader", "type": "anyone"}
        self.drive_service.permissions().create(fileId=file_id, body=permission).execute()
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    def upload_file_to_drive(
        self, file_path: str, file_name: str, folder_id: Optional[str] = None
    ) -> str:
        """Faz upload de um arquivo local para o Google Drive e retorna o file_id."""
        file_metadata = {"name": file_name}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        # Determina mimetype
        mimetype = "application/octet-stream"
        if file_path.endswith(".png"):
            mimetype = "image/png"
        elif file_path.endswith((".jpg", ".jpeg")):
            mimetype = "image/jpeg"

        media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)

        file = (
            self.drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file.get("id")


# =====================================================
# Pydantic Schemas
# =====================================================
class GetNextPostInput(BaseModel):
    sheet_id: str = Field(..., description="ID do Google Sheet")
    worksheet_name: str = Field(..., description="Nome da aba (worksheet)")


class GetPostByLineInput(BaseModel):
    sheet_id: str
    worksheet_name: str
    line_number: int = Field(..., ge=2, description="Número da linha (>=2, pois 1 é cabeçalho)")


class GetRandomPostInput(BaseModel):
    sheet_id: str
    worksheet_name: str


class GetPostByLineInput(BaseModel):
    """Parâmetros necessários para buscar uma linha no Google Sheet."""

    sheet_id: str = Field(..., description="ID da planilha do Google Sheets.")
    worksheet_name: str = Field(..., description="Nome da aba dentro da planilha.")
    line_number: int = Field(..., ge=2, description="Número da linha a ser buscada (mínimo 2, pois a linha 1 é cabeçalho).")    


class DownloadFileInput(BaseModel):
    file_id: str
    output_file: str


class UploadFileInput(BaseModel):
    file_path: str
    file_name: str
    folder_id: Optional[str] = None


class MakeFilePublicInput(BaseModel):
    file_id: str


# =====================================================
# Tools
# =====================================================
class GetNextPostTool(BaseTool):
    name: str = "get_next_post"
    description: str = "Busca a próxima linha de postagens em um Google Sheet (ignora cabeçalho)."
    args_schema: Type[BaseModel] = BaseModel  # não recebe input externo

    def _run(self) -> Optional[Tuple[int, Dict[str, Any]]]:
        sheet_id = os.getenv("SHEET_ID")
        worksheet_name = os.getenv("WORKSHEET")
        client = GoogleDriveClient().sheets_client
        sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
        data = sheet.get_all_records()
        for idx, row in enumerate(data, start=2):
            return idx, row
        return None


class GetPostByLineTool(BaseTool):
    name: str = "get_post_by_line"
    description: str = "Busca dados de uma linha específica no Google Sheet."
    args_schema: Type[BaseModel] = GetPostByLineInput

    def _run(self, sheet_id: str, worksheet_name: str, line_number: int):
        client = GoogleDriveClient().sheets_client
        sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
        header = sheet.row_values(1)
        row_values = sheet.row_values(line_number)
        if not row_values:
            return None
        return line_number, dict(zip(header, row_values))


class GetRandomPostTool(BaseTool):
    name: str = "get_random_post"
    description: str = "Retorna uma linha aleatória de um Google Sheet."
    args_schema: Type[BaseModel] = BaseModel

    def _run(self) -> Optional[Tuple[int, Dict[str, Any]]]:
        sheet_id = os.getenv("SHEET_ID")
        worksheet_name = os.getenv("WORKSHEET")
        client = GoogleDriveClient().sheets_client
        sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)

        all_values = sheet.get_all_values()
        total_rows = len(all_values)
        if total_rows <= 1:
            return None

        random_line = random.randint(2, total_rows)
        header = all_values[0]
        row_values = all_values[random_line - 1]
        if not row_values:
            return None
        return random_line, dict(zip(header, row_values))
    

class GetPostDailyTool(BaseTool):
    name: str = "get_post_daily"
    description: str = "Busca dados de uma linha específica na aba diária do Google Sheet."
    args_schema: Type[BaseModel] = GetPostByLineInput

    def _run(
        self, sheet_id: str, line_number: int
    ) -> Optional[Dict[str, Any]]:
        """Retorna os dados de uma linha específica na worksheet diária."""
        client = GoogleDriveClient().sheets_client
        sheet = client.open_by_key(sheet_id).worksheet(os.getenv("WORKSHEET_DAILY"))

        header = sheet.row_values(1)
        row_values = sheet.row_values(line_number)
        if not row_values:
            return None
        return dict(zip(header, row_values))

    async def _arun(
        self, sheet_id: str, worksheet_name: str, line_number: int
    ) -> str:
        raise NotImplementedError("Execução assíncrona não implementada.")



class DownloadFileTool(BaseTool):
    name: str = "download_file"
    description: str = "Baixa um arquivo do Google Drive e salva localmente."
    args_schema: Type[BaseModel] = DownloadFileInput

    def _run(self, file_id: str, output_file: str) -> str:
        client = GoogleDriveClient()
        file_bytes = client.download_file(file_id)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(file_bytes.getbuffer())
        return output_file


class UploadFileTool(BaseTool):
    name: str = "upload_file_to_drive"
    description: str = "Faz upload de um arquivo local para o Google Drive e retorna o file_id."
    args_schema: Type[BaseModel] = UploadFileInput

    def _run(self, file_path: str, file_name: str, folder_id: Optional[str] = None) -> str:
        client = GoogleDriveClient()
        return client.upload_file_to_drive(file_path, file_name, folder_id)


class MakeFilePublicTool(BaseTool):
    name: str = "make_file_public"
    description: str = "Torna um arquivo do Google Drive público e retorna a URL de download."
    args_schema: Type[BaseModel] = MakeFilePublicInput

    def _run(self, file_id: str) -> str:
        client = GoogleDriveClient()
        return client.make_file_public(file_id)
