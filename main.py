import pandas as pd
import numpy as np
from datetime import datetime
import random
import calendar
import ast
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity, sigmoid_kernel

meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
app = FastAPI()
movies_wc = pd.read_parquet('movies_cleaned.parquet') 


@app.get('/')
def message():
    return "Proyecto Integrador sobre Recomendacion de Peliculas"

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
   
    try:
        mes_numero = meses.index(mes.lower()) + 1
        filas_con_mes = movies_wc[movies_wc['release_date'].dt.month == mes_numero]
        cant_meses = len(filas_con_mes)
        return {'mes':mes, 'cantidad':cant_meses}

    except ValueError:
        return {'Error': 'ingrese el mes por su nombre, por ejemplo: enero'}
    


@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    
    try:
        dia_numero = dias.index(dia.lower()) + 1
        filas_con_dias = movies_wc[movies_wc['release_date'].dt.dayofweek == dia_numero]
        cant_dias = len(filas_con_dias)
        return {'dia':dia, 'cantidad':cant_dias}
    except ValueError:
        return {'Error':'Ingrese el dia nuevamente, evite usar acentos. Ejemplo: lunes'}


@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
                
    try:
        movie = movies_wc[movies_wc['title'].str.lower()==titulo.lower()]    
        titulo_pelicula = movie['title'].iloc[0]
        anio = movie['release_year'].iloc[0]
        popularidad = movie['popularity'].iloc[0]    
        return {'titulo': f'{titulo_pelicula}','año': f'{anio}','popularidad': f'{popularidad.round(2)}'}
    except IndexError:
        return {'Error': 'Lo sentimos, la pelicula no esta en nuestro catalogo'}
        

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    
    try:
        movie = movies_wc[movies_wc['title'].str.lower()==titulo.lower()]
        titulo_pelicula = movie['title'].iloc[0]
        anio = movie['release_year'].iloc[0]
        votos = movie['vote_count'].iloc[0].astype(int)
        promedio = movie['vote_average'].iloc[0]

        if votos >= 2000:
            return {'titulo':f'{titulo_pelicula}', 'año':f'{anio}','voto_total':f'{votos}', 'voto_promedio':f'{promedio}'}
    except IndexError:
        return {'Error':'La pelicula no esta en el catalogo o no tiene suficientes valoraciones'}


@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):

    movies = movies_wc['cast'].str.lower()
    lista_indices = list(movies[movies.str.contains(nombre_actor.lower())].index.values)
    cant_peli = len(lista_indices)
    if cant_peli > 0:
        ret_prom = 0
        for indice in lista_indices:
            ret_prom += movies_wc.iloc[indice]['return']
        if cant_peli > 0:
            ret_prom = (ret_prom/cant_peli).round(2)
        else:
            cant_peli = 0
        lista_return = [movies_wc['return'].iloc[_] for _ in lista_indices]
        valor_max = max(lista_return)
        indice_max_return = lista_indices[lista_return.index(valor_max)]
        return {'actor': f'{nombre_actor}','movie_count': f'{cant_peli}',
                'max_return': f'{movies_wc.iloc[indice_max_return]["return"].round(2)}',
                'average_return': f'{ret_prom}'}
    else:
        return {'Error': 'Actor no encontrado, ingrese actor/actiz nuevamente, por ejemplo: Tom Hanks'}


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
     
    movies = movies_wc['director'].str.lower()
    lista_indices = list(movies[movies.str.contains(nombre_director.lower())].index.values)
    if len(lista_indices)> 0:
        lista_movies = [movies_wc['title'].iloc[_] for _ in lista_indices]
        lista_anios = [movies_wc['release_year'].iloc[_] for _ in lista_indices]
        lista_ganancia = [movies_wc['revenue'].iloc[_] for _ in lista_indices]
        lista_presupuesto = [movies_wc['budget'].iloc[_] for _ in lista_indices]
        lista_retorno = [movies_wc['return'].iloc[_] for _ in lista_indices]
        retorno_total = sum(lista_retorno)
        return {'director': f'{nombre_director}','retorno_total_director': f'{retorno_total}',
               'peliculas': f'{lista_movies}','anio': f'{lista_anios}','retorno_pelicula': f'{lista_retorno}',
               'budget_pelicula': f'{lista_presupuesto}','revenue_pelicula': f'{lista_ganancia}' }
    else:
        return {'Error':'Director/a no encontrado/a, ingrese director/a nuevamente, por ejemplo: James Cameron'}
    
    
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo):
    
    try:
        semilla = random.randint(0, 1000)
        movies_wc_small = movies_wc.sample(frac=0.25, random_state=semilla)
        #movies_wc_small = movies_wc_small.append(movies_wc[movies_wc['title']==titulo])
        movies_wc_small = pd.concat([movies_wc_small, movies_wc[movies_wc['title']==titulo]], ignore_index=True)
        movies_wc_small.drop_duplicates(subset=['title'], inplace=True)
        
        movies_wc_small['tagline'] = movies_wc_small['tagline'].fillna('')
        movies_wc_small['over_tag'] = movies_wc_small['overview'] + movies_wc_small['tagline']
        movies_wc_small['over_tag'] = movies_wc_small['over_tag'].fillna('')
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 1),min_df=1, stop_words='english')
        matriz_frec = tf.fit_transform(movies_wc_small['over_tag'])
        cosine_sim = linear_kernel(matriz_frec, matriz_frec)
        movies_wc_small = movies_wc_small.reset_index()
        titulos = movies_wc_small['title']
        indices = pd.Series(movies_wc_small.index, index=movies_wc_small['title']).drop_duplicates()

        idx = indices[titulo]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movie_indices = [i[0] for i in sim_scores]
        lista = list(titulos.iloc[movie_indices])
        
        return {'Lista recomendada': lista }
     
    except KeyError:
        return {'Error':'Lo sentimos, la pelicula no esta en el catalogo'}


