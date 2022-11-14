from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
from bs4 import BeautifulSoup
from db import migracion_datos,consulta_plantilla
import base64, os.path, sys, joblib

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
    nombre_etiqueta = ['Nuevos(RALE)','Por Enviar','No Aplica']
    for i in range(3):
        cuerpo_etiqueta = {'name': nombre_etiqueta[i], 'labelListVisibility'   : 'labelShow', 'messageListVisibility' : 'show'}
        crear = service.users().labels().create(userId = 'me', body = cuerpo_etiqueta).execute()

def get_etiqueta():
    service = create_service()
    resultado = service.users().labels().list(userId = 'me').execute()
    etiqueta = resultado.get('labels',[])
    total_etiqueta = []
    for labels in etiqueta:
        total_etiqueta.append(labels['id'])
    if len(total_etiqueta) == 14:
        crear_etiqueta()

    etiquetas_nuevas = [total_etiqueta[-3],total_etiqueta[-2],total_etiqueta[-1]]
    return etiquetas_nuevas

def crear_borrador(cuerpo,asunto,cliente,solicitud):
    service = create_service()
    body = "Estimando,\nEspero se encuentre bien, le comento que su solicitud con el siguiente asunto:\n\n<"+solicitud+">\n\n"\
          + cuerpo
    message = EmailMessage()
    message['from'] = 'opens.rale.2022@gmail.com'
    message['to'] = cliente
    message['subject'] = asunto
    message.set_content(body)
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'message': {'raw': encoded_message}}
    drafts =  service.users().drafts().create(userId='me',body=create_message).execute()

def mover_email():
    service = create_service()
    labels = get_etiqueta()
    resultado = service.users().messages().list(userId = 'me', labelIds= ['INBOX'], q = 'is:unread', maxResults = 1).execute()
    mensaje = resultado.get('messages', [])
    for id in mensaje:
        service.users().messages().modify(userId = 'me', id = id['id'], body = {'removeLabelIds':['INBOX'], 'addLabelIds':[labels[0]]}).execute()


def get_email():
    service = create_service()
    labels = get_etiqueta()
    msj = service.users().messages().list(userId='me', labelIds = [labels[0]], q = 'is:unread').execute()
    messages = msj.get('messages',[])
    data = []
    for id in messages:
        temp = []
        result = service.users().messages().get(userId='me', id = id['id']).execute()
        payload = result['payload']['headers']
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
        payload = result['payload']
        parts = payload.get('parts')[0]
        cuerpo = parts['body']['data']
        cuerpo = cuerpo.replace("-","+").replace("_","/")
        decoded_cuerpo = base64.b64decode(bytes(cuerpo, 'UTF-8'))
        soup = BeautifulSoup(decoded_cuerpo , "lxml")
        mensaje = soup.body()
        if len(mensaje) > 1 :
            juntar_mensaje = ""
            for i in mensaje:
                juntar_mensaje = juntar_mensaje+" "+str(i)
                print(juntar_mensaje)
            temp.append(juntar_mensaje)
        else:
            temp.append(mensaje)
        temp.append(id['id'])
        data.append(temp)

    return data

def clasificador():
    informacion = get_email()
    ruta = sys.path
    vector = joblib.load(ruta[0]+'/vectorizer.joblib')
    clasificador = joblib.load(ruta[0]+'/SVC.joblib')
    for i in range(len(informacion)):
        procesar = [str(informacion[i][3])]
        data = vector.transform(procesar)
        valor = clasificador.predict(data)
        informacion[i].append(valor)
    return informacion

def main():
    mover_email()
    service = create_service()
    data = clasificador()
    etiqueta = get_etiqueta()
    plantilla = consulta_plantilla()
    for i in range(len(data)):
        email = data[i]
        if email[5] == 'Despido':
            asunto = plantilla[0]
            cuerpo = plantilla[1]
            cliente = email[0]
            solicitud = email[2]
            crear_borrador(cuerpo = cuerpo, asunto = asunto,cliente = cliente, solicitud = solicitud)
            service.users().messages().modify(userId = 'me', id = email[4], body = {'removeLabelIds':['UNREAD'],'addLabelIds': [etiqueta[1]]}).execute()
        else:
            service.users().messages().modify(userId = 'me', id = email[4], body = {'removeLabelIds':['UNREAD'],'addLabelIds': [etiqueta[2]]}).execute()

mover_email()
