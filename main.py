import pandas as pd
import numpy as np
from datetime import datetime
import calendar
import ast
from fastapi import FastAPI

url = 'https://drive.google.com/file/d/1QuvhMiZLka18ZXnx8o1P5C8Cf5oHCgjL/view?usp=sharing'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
app = FastAPI()
movies_wc = pd.read_csv(url) 
movies_wc['release_date'] = pd.to_datetime(movies_wc['release_date'])

@app.get('/')
def message():
    return "Proyecto Integrador sobre Recomendacion de Peliculas"

@app.get('/mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
   
    try:
        mes_numero = meses.index(mes.lower()) + 1
        filas_con_mes = movies_wc[movies_wc['release_date'].dt.month == mes_numero]
        cant_meses = len(filas_con_mes)
        #return (f"{cant_meses} cantidad de películas fueron estrenadas en el mes de {mes}") 
        return {'mes':mes, 'cantidad':cant_meses}

    except ValueError:
        return {'Error': 'ingrese el mes por su nombre, por ejemplo: enero'}
    
dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

@app.get('/dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    
    try:
        dia_numero = dias.index(dia.lower()) + 1
        filas_con_dias = movies_wc[movies_wc['release_date'].dt.dayofweek == dia_numero]
        cant_dias = len(filas_con_dias)
        return {'dia':dia, 'cantidad':cant_dias}
    #return (f'{cant_dias} cantidad de películas fueron estrenadas en los días {dia}')
    except ValueError:
        return {'Error':'Ingrese el dia nuevamente, evite usar acentos. Ejemplo: lunes'}

print(cantidad_filmaciones_dia('jueves'))
