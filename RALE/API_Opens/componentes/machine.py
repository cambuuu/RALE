#pip install -U scikit-learn scipy matplotlib
import imaplib, email
import joblib

def clasificar(correo):
    data = [correo]
    vector = joblib.load('vectorizer.joblib')
    clasificador = joblib.load('SVC.joblib')
    data = vector.transform(data)
    valor = clasificador.predict(data)
    return valor

def connect(email):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    password= 'mzfzqybucciwgmou'
    imap.login(email, password)
    return imap

def disconnect(imap):
    imap.logout()

def mover_email(id_email):
    imap = connect('portafolio.duocuc.2022@gmail.com')
    imap.select(mailbox = '"INBOX"', readonly = False)
    resp, items = imap.search(None, 'All')
    email_ids  = items[0].split()
    latest_email_id = [email_ids[-2],email_ids[-1]]

    for uid in latest_email_id:
        if uid == id_email:
            resp, data = imap.fetch(uid, '(RFC822)')
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            msg_uid = email.message_from_string(raw_email_string)

            imap.store(uid,'+X-GM-LABELS', '"Aplica"')
    disconnect(imap)
