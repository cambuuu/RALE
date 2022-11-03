from __future__ import print_function
import os.path, sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.

def create_service():
    ruta = sys.path
    CLIENT_SECRET_FILE = ruta[0]+'/credenciales.json'
    API_NAME ='gmail'
    API_VERSION='v1'
    SCOPES =['https://mail.google.com/']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(ruta[0]+'/token.json', 'w') as token:
            token.write(creds.to_json())
    service = build(API_NAME, API_VERSION, credentials=creds)

    return service

def crear_borrador(cuerpo,cliente,asunto):
    service = create_service()
    body = cuerpo
    message = EmailMessage()
    message['from'] = 'portafolio.duocuc.2022@gmail.com'
    message['to'] = cliente
    message['subject'] = asunto
    message.set_content(body)
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'message': {'raw': encoded_message}}
    drafts =  service.users().drafts().create(userId='me',body=create_message).execute()

