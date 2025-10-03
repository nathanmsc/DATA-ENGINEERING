import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopos necessários para acessar o Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

Token = '/home/user/DATA-ENGINEERING/DOCKER/N8N/POSTS/APP/src/app/config/token.json'

def autenticar_google_drive():
    """
    Autentica no Google Drive usando OAuth2.
    Retorna o serviço do Google Drive autenticado.
    """
    creds = None
    
    # O arquivo token_stored.json armazena os tokens de acesso e refresh do usuário
    # É criado automaticamente quando o fluxo de autorização é concluído pela primeira vez
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Se não há credenciais válidas disponíveis, solicita login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Atualizando token expirado...')
            creds.refresh(Request())
        else:
            print('Iniciando fluxo de autenticação OAuth2...')
            flow = InstalledAppFlow.from_client_secrets_file(
                Token, SCOPES)
            # Usa o servidor local para receber o callback
            creds = flow.run_local_server(port=8000)
        
        # Salva as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print('Credenciais salvas com sucesso!')
    
    return creds

def listar_arquivos(service, num_arquivos=10):
    """
    Lista os arquivos do Google Drive como exemplo.
    """
    try:
        results = service.files().list(
            pageSize=num_arquivos,
            fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('Nenhum arquivo encontrado.')
            return
        
        print(f'\n{len(items)} arquivos encontrados:')
        for item in items:
            print(f"- {item['name']} ({item['mimeType']})")
    
    except HttpError as error:
        print(f'Ocorreu um erro: {error}')

def main():
    """
    Função principal que executa a autenticação e testa o acesso.
    """
    print('=== Autenticação Google Drive com OAuth2 ===\n')
    
    # Autentica no Google Drive
    creds = autenticar_google_drive()
    
    # Cria o serviço do Google Drive
    try:
        service = build('drive', 'v3', credentials=creds)
        print('\nAutenticação realizada com sucesso!')
        
        # Testa listando alguns arquivos
        listar_arquivos(service)
        
        return service
    
    except HttpError as error:
        print(f'Erro ao criar serviço: {error}')
        return None

if __name__ == '__main__':
    service = main()