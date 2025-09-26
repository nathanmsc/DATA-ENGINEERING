import os
import random
import gspread
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from functools import cached_property
from google.oauth2.service_account import Credentials
from typing import Type, Optional, Tuple, Dict, Any

load_dotenv()

SHEET_ID = os.getenv("SHEET_ID")
WORKSHEET = os.getenv("WORKSHEET")

class GoogleDriveClient:
    """Cliente interno para autenticação e acesso ao Google Sheets via gspread."""

    @cached_property
    def scopes(self):
        scopes_env = os.getenv("GOOGLE_SCOPES")
        if not scopes_env:
            raise ValueError("⚠️ Variável de ambiente GOOGLE_SCOPES não encontrada no .env")
        return scopes_env.split(",")

    @cached_property
    def credentials(self):
        credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
        if not credentials_file:
            raise ValueError("⚠️ Variável de ambiente GOOGLE_CREDENTIALS_FILE não definida.")
        return Credentials.from_service_account_file(credentials_file, scopes=self.scopes)

    @cached_property
    def client(self):
        return gspread.authorize(self.credentials)


# -----------------------------
# Pydantic Schema de Input
# -----------------------------
class GetNextPostInput(BaseModel):
    """Parâmetros para buscar o próximo post no Google Sheets."""
    sheet_id: str = Field(..., description="ID do Google Sheet")
    worksheet_name: str = Field(..., description="Nome da aba (worksheet) dentro do Google Sheet")


# -----------------------------
# Tool Customizada
# -----------------------------
class GetNextPostTool(BaseTool):
    name: str = "get_next_post"
    description: str = (
        "Busca a próxima linha de postagens em um Google Sheet (pula cabeçalho). "
        "Útil para gerenciar conteúdo social em planilhas."
    )
    args_schema: Type[BaseModel] = BaseModel  # sem inputs externos

    def _run(self) -> Optional[Tuple[int, Dict[str, Any]]]:
        sheet_id = os.getenv("SHEET_ID")
        worksheet_name = os.getenv("WORKSHEET")

        client = GoogleDriveClient().client
        sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
        data = sheet.get_all_records()
        for idx, row in enumerate(data, start=2):  # start=2 para ignorar cabeçalho
            return idx, row
        return None

    async def _arun(self) -> str:
        raise NotImplementedError("Execução assíncrona não implementada.")


# -----------------------------
# Outro exemplo: buscar por linha
# -----------------------------
class GetPostByLineInput(BaseModel):
    """Parâmetros para buscar uma linha específica do Google Sheet."""
    sheet_id: str = Field(..., description="ID do Google Sheet")
    worksheet_name: str = Field(..., description="Nome da aba (worksheet)")
    line_number: int = Field(..., description="Número da linha desejada (>=2, pois 1 é cabeçalho)")


class GetPostByLineTool(BaseTool):
    name: str = "get_post_by_line"
    description: str = "Busca dados de uma linha específica em um Google Sheet."
    args_schema: Type[BaseModel] = GetPostByLineInput

    def _run(self, line_number: int) -> Optional[Tuple[int, Dict[str, Any]]]:
        client = GoogleDriveClient().client
        sheet = client.open_by_key(os.getenv("SHEET_ID")).worksheet(os.getenv("WORKSHEET"))

        header = sheet.row_values(1)
        row_values = sheet.row_values(line_number)

        if not row_values:
            return None

        row_dict = dict(zip(header, row_values))
        return line_number, row_dict

    async def _arun(self, sheet_id: str, worksheet_name: str, line_number: int) -> str:
        raise NotImplementedError("Execução assíncrona não implementada.")
    
# ---------------------------------------
# Input Pydantic
# ---------------------------------------
class GetRandomPostInput(BaseModel):
    """Parâmetros para buscar uma linha aleatória do Google Sheet."""
    sheet_id: str = Field(..., description="ID do Google Sheet")
    worksheet_name: str = Field(..., description="Nome da aba (worksheet) dentro do Google Sheet")

# ---------------------------------------
# Tool
# ---------------------------------------

class GetRandomPostTool(BaseTool):
    name: str = "get_random_post"
    description: str = (
        "Conta o total de linhas de dados em um Google Sheet (ignora cabeçalho) "
        "e retorna uma linha aleatória com seu conteúdo."
    )
    args_schema: Type[BaseModel] = BaseModel  # sem inputs externos

    def _run(self) -> Optional[Tuple[int, Dict[str, Any]]]:
        sheet_id = os.getenv("SHEET_ID")
        worksheet_name = os.getenv("WORKSHEET")

        # Conecta ao Google Sheets
        client = GoogleDriveClient().client
        sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)

        # Conta todas as linhas que contêm dados
        all_values = sheet.get_all_values()
        total_rows = len(all_values)

        if total_rows <= 1:
            return None

        # Escolhe aleatoriamente uma linha a partir da 2
        random_line = random.randint(2, total_rows)
        header = all_values[0]
        row_values = all_values[random_line - 1]

        if not row_values:
            return None

        row_dict = dict(zip(header, row_values))
        return random_line, row_dict

    async def _arun(self) -> str:
        raise NotImplementedError("Execução assíncrona não implementada.")





