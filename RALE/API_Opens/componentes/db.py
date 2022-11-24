import psycopg2

def migracion_datos(datos):
	conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
	cursor = conexion.cursor()
	sql = 'INSERT INTO "Email"(nombre,fecha,asunto,cuerpo) VALUES (%s,%s,%s,%s)'
	insert = str(datos[0]),str(datos[1]),str(datos[2]),str(datos[3])
	cursor.execute(sql,insert)
	conexion.commit()
	conexion.close()

def consulta_plantilla():
        conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
        cursor = conexion.cursor()
        sql = 'SELECT asunto_plantilla,cuerpo_plantilla FROM "Plantilla"'
        cursor.execute(sql)
        plantilla = []
        for sentencia in cursor:
                plantilla.extend(sentencia)
        conexion.close()
        return plantilla

def registro_email(condicion):
	conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
	cursor = conexion.cursor()
	sql = 'SELECT id FROM "Email" WHERE fecha = %s;'
	cursor.execute(sql,(condicion,))
	id = ''
	for sentencia in cursor:
		id = sentencia
	email = id[0]
	conexion.close()
	return email

def consulta_abogado():
	conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
	cursor = conexion.cursor()
	sql = 'SELECT id FROM "Abogado" WHERE id = 1'
	cursor.execute(sql)
	id = 0
	for sentencia in cursor:
		id = sentencia
	abogado = id[0]
	conexion.close()
	return abogado

def migracion_solicitud(data):
	conexion = psycopg2.connect(database = "Opens", user = "opensrale", password = "rale2022", host = "localhost", port = "5432")
	cursor = conexion.cursor()
	sql = 'INSERT INTO "Solicitud"(descripcion,fecha,prediccion,id_email_id,id_abogado_id) VALUES (%s,CURRENT_TIMESTAMP,%s,%s,%s)'
	insert = str(data[0]),str(data[1]),data[2],data[3]
	cursor.execute(sql,insert)
	conexion.commit()
	conexion.close()
