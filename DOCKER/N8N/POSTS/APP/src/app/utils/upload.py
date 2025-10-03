import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from dotenv import load_dotenv

# Escopo da API: permite acesso total aos arquivos do Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]


def upload_to_drive(file_path):
    """Faz o upload de um arquivo para o Google Drive."""
    token = '/home/user/DATA-ENGINEERING/DOCKER/N8N/POSTS/APP/src/app/config/token.json'


    # Carrega ou gera as credenciais de acesso
    creds = None
    

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(token, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token, "w") as token:
            token.write(creds.to_json())

    try:
        # Cria o serviço da API do Google Drive
        service = build("drive", "v3", credentials=creds)

        # Prepara o arquivo para upload
        file_name = os.path.basename(file_path)
        file_metadata = {"name": file_name}
        media = MediaFileUpload(file_path, resumable=True)

        # Realiza o upload
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        print(f"Upload bem-sucedido! ID do arquivo: {file.get('id')}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
file = '/home/user/DATA-ENGINEERING/DOCKER/N8N/POSTS/APP/src/app/config/token.json'
if __name__ == "__main__":
    # Substitua pelo caminho do arquivo que você deseja enviar
    upload_to_drive(file)
