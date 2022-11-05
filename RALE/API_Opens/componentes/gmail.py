from __future__ import print_function
import os.path, sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
from bs4 import BeautifulSoup
from db import migracion_datos, consulta_plantilla
import base64, joblib, email, sys

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

def crear_etiqueta():
    service = create_service()
    label_body = {"name": "Aplica","messageListVisibility": "show","labelListVisibility": "labelShow",}
    service.users().labels().create(userId='me', body=label_body).execute()
    label_body = {"name": "No Aplica","messageListVisibility": "show","labelListVisibility": "labelShow",}
    service.users().labels().create(userId='me', body=label_body).execute()

def mostrar_etiqueta():
    service = create_service()
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    etiquetas = []
    for label in labels:
        nombre = label['id']
        etiquetas.append(nombre)
    if len(etiquetas) == 14:
        crear_etiqueta()
    else:
        pass

def crear_borrador(cuerpo,cliente,asunto,solicitud):
    service = create_service()
    body = "En relación al asunto:\n\n<"+str(solicitud)+">\n\n"+cuerpo
    message = EmailMessage()
    message['from'] = 'portafolio.duocuc.2022@gmail.com'
    message['to'] = str(cliente)
    message['subject'] = str(asunto)
    message.set_content(body)
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'message': {'raw': encoded_message}}
    drafts =  service.users().drafts().create(userId='me',body=create_message).execute()

def leer_email():
    service = create_service()
    resultado = service.users().messages().list(userId = 'me', labelIds = ['INBOX'], q = 'is:unread', maxResults = 2).execute()
    emails = resultado.get('messages',[])
    data_email = []
    for msg in emails:
        temp = []
        rst = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = rst['payload']['headers']
        for value in payload:
            if value['name'] == 'From':
                name = value['value']
                temp.append(name)
            if value['name'] == 'Date':
                fecha = value['value']
                temp.append(fecha)
            if value['name'] == 'Subject':
                asunto = value['value']
                temp.append(asunto)
        payload = rst['payload']
        parts = payload.get('parts')[0]
        data = parts['body']['data']
        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode (bytes(data, 'UTF-8'))
        soup = BeautifulSoup(decoded_data , "lxml")
        mssg_body = soup.body()
        temp.append(mssg_body)
        temp.append(rst['id'])
        data_email.append(temp)

    return data_email

def clasificar():
    ruta = sys.path
    email = leer_email()
    valor = []
    for cuerpo in range(len(email)):
        temp = email[cuerpo]
        vector = joblib.load(ruta[0]+'/vectorizer.joblib')
        clasificador = joblib.load(ruta[0]+'/SVC.joblib')
        data = vector.transform([str(temp[3])])
        resultado = clasificador.predict(data)
        temp.append(resultado)
        valor.append(temp)
    return valor

def main():
    emails = clasificar()
    service = create_service()
    plantilla = consulta_plantilla()
    for i in range(len(emails)):
        temp = emails[i]
        cliente = temp[0]
        asunto = plantilla[1]
        cuerpo = plantilla[2]
        solicitud = temp[2]
        if temp[5] == 'Despido':
            mostrar_etiqueta()
            crear_borrador(cuerpo = cuerpo, cliente = cliente, asunto = asunto, solicitud = solicitud)
            service.users().messages().modify(userId='me', id=temp[4] , body={ 'removeLabelIds': ['UNREAD']}).execute()
            service.users().messages().modify(userId='me', id=temp[4] , body={ 'addLabelIds': ['Label_11']}).execute()
        else:
            service.users().messages().modify(userId='me', id=temp[4] , body={ 'removeLabelIds': ['UNREAD']}).execute()
            service.users().messages().modify(userId='me', id=temp[4] , body={ 'addLabelIds': ['Label_12']}).execute()
        migracion_datos(datos = temp)
