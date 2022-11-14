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
