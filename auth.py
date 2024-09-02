import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


# Carrega as variáveis do arquivo .env
load_dotenv()

# Define o escopo para a API do Google People
SCOPES = ['https://www.googleapis.com/auth/contacts']

# Valores das variáveis de ambiente
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')

def authenticate():
    creds = None

     # Verifique se as variáveis de ambiente foram carregadas corretamente
    if CLIENT_SECRET_FILE is None or CREDENTIALS_FILE is None:
        raise ValueError("As variáveis CLIENT_SECRET_FILE ou CREDENTIALS_FILE não foram definidas no arquivo .env")
    
    # Carrega as credenciais salvas, se disponíveis
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
    
    # Se não houver credenciais ou as credenciais não forem válidas, faça a autenticação novamente
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        # Salve as credenciais para reutilização futura
        with open(CREDENTIALS_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds
