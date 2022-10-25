import imaplib
import email
from email.header import decode_header
from db import *

username = 'lopez.vicio.2b@gmail.com'
password = 'efemcujwlfpcslbn'
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, password)
status, mensajes = imap.select("INBOX")
N = 2
mensajes = int(mensajes[0])
data = []
for i in range(mensajes, mensajes - N, -1):
    try:
        res, mensaje = imap.fetch(str(i), "(RFC822)")
    except:
        break
    for respuesta in mensaje:
        temp = []
        if isinstance(respuesta, tuple):
            mensaje = email.message_from_bytes(respuesta[1])
            subject = decode_header(mensaje["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            from_ = mensaje.get("From")
            if mensaje.is_multipart():
                for part in mensaje.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        temp.append(from_)
                        temp.append(mensaje["Date"])
                        temp.append(subject)
                        temp.append(body)
            data.append(temp)

imap.close()
valores = ""
for correo in range(len(data)):
     valores = data[correo]
     migracion_datos(datos = valores)
cuerpo = consulta_datos_cuerpo()
nombre = consulta_datos_from()

final = Clasificador(cuerpo = cuerpo)
plantilla = consulta_plantilla()
asunto = plantilla[1]
body = plantilla[2]
for i in range(len(final)):
     clasificador = final[i]
     from_ = nombre[i]
     if clasificador == 'Despido':
         Enviar_Email(nombre = from_, cuerpo = body, asunto = asunto)

