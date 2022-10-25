import psycopg2
import smtplib,ssl
from email.message import EmailMessage
import joblib

def migracion_datos(datos):
	conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
	cursor = conexion.cursor()
	sql = 'INSERT INTO "Email"(nombre,fecha,asunto,cuerpo) VALUES (%s,%s,%s,%s)'
	rango = len(datos)
	if rango == 4:
		data = (datos[0],datos[1],datos[2], str(datos[3]))
		cursor.execute(sql,data)
		conexion.commit()
		conexion.close()
'''
	else:
		data = (datos[0],datos[1],datos[2], "")
		cursor.execute(sql,data)
		conexion.commit()
		conexion.close()
'''
def consulta_datos_cuerpo():
	conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
	cursor = conexion.cursor()
	sql = 'SELECT cuerpo FROM "Email"'
	cursor.execute(sql)
	data_cuerpo = []
	for sentencia in cursor:
		data_cuerpo.extend(sentencia)
	conexion.close()
	return data_cuerpo

def consulta_datos_from():
	conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
	cursor = conexion.cursor()
	sql = 'SELECT nombre FROM "Email"'
	cursor.execute(sql)
	data_from = []
	for sentencia in cursor:
		data_from.extend(sentencia)
	conexion.close()
	return data_from

def consulta_plantilla():
        conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
        cursor = conexion.cursor()
        sql = 'SELECT *  FROM "Plantilla"'
        cursor.execute(sql)
        plantilla = []
        for sentencia in cursor:
                plantilla.extend(sentencia)
        conexion.close()
        return plantilla

def Enviar_Email(nombre, cuerpo, asunto):
	email_sender = 'lopez.vicio.2b@gmail.com'
	email_password = "efemcujwlfpcslbn"
	email_receiver = nombre

	subject = asunto
	body = cuerpo

	em =EmailMessage()
	em['front'] = email_sender
	em ['to'] = email_receiver
	em['subject'] = subject
	em.set_content(body)

	context = ssl.create_default_context()

	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(email_sender,email_password)
		smtp.sendmail(email_sender,email_receiver, em.as_string())


def Clasificador(cuerpo):
	data = cuerpo
	vector = joblib.load('vectorizer.joblib')
	clasificador = joblib.load('SVC.joblib')
	transformacion = vector.transform(data)
	resultado = clasificador.predict(transformacion)

	return resultado



