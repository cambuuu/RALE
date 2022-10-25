import pickle
import numpy as np

a = np.array('Elimina la información de exploración al cerrar todas las ventanas de InPrivate Guarda las colecciones, los favoritos y las descargas (pero no el historial de descargas)Impide que las búsquedas de Microsoft Bing se asocien contigo')
with open('model.sav','rb') as file:
	model = pickle.load(file)

respuesta = model.predict(a)
print(respuesta)


