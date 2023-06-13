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
    return "Bienvenido a All About Movies"

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
   
    try:
        mes_numero = meses.index(mes.lower()) + 1                                   #Se convierte el mes ingresado en un valor numerico
        filas_con_mes = movies_wc[movies_wc['release_date'].dt.month == mes_numero] #Se genera una lista con las coincidencias
        cant_meses = len(filas_con_mes)                                             #Se cuenta la cantidad de coincidencias
        return {'mes': mes, 'cantidad': cant_meses}
    except ValueError:
        return {'Error': 'ingrese el mes por su nombre, por ejemplo: enero'}
    


@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    
    try:
        dia_numero = dias.index(dia.lower()) + 1                                        #Se convierte el dia ingresado en un valor numerico
        filas_con_dias = movies_wc[movies_wc['release_date'].dt.dayofweek == dia_numero]#Se genera una lista con las coincidencias
        cant_dias = len(filas_con_dias)                                                 #Se cuenta la cantidad de coincidencias
        return {'dia':dia, 'cantidad':cant_dias}
    except ValueError:
       return {'Error':'Ingrese el dia nuevamente, evite usar acentos. Ejemplo: lunes'}


@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
                
    try:
        movie = movies_wc[movies_wc['title'].str.lower()==titulo.lower()]               #Se matchea con la pelicula ingresada
        titulo_pelicula = movie['title'].iloc[0]                                        #Se guarda el titulo de la pelicula
        anio = movie['release_year'].iloc[0]                                            #Se guarda el año de lanzamiento de la pelicula
        popularidad = movie['popularity'].iloc[0]                                       #Se guarda la popularidad
        return {'titulo': titulo_pelicula,'año': anio,'popularidad': popularidad.round(2)}
    except IndexError:
        return {'Error': 'Lo sentimos, la pelicula no esta en nuestro catalogo'}
                

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    
    try:
        movie = movies_wc[movies_wc['title'].str.lower()==titulo.lower()]               #Se matchea con la pelicula ingresada
        titulo_pelicula = movie['title'].iloc[0]                                        #Se guarda el titulo de la pelicula
        anio = movie['release_year'].iloc[0]                                            #Se guarda el año de lanzamiento
        votos = movie['vote_count'].iloc[0].astype(int)                                 #Se guarda la cantidad de votos recibidos en TMDB
        promedio = movie['vote_average'].iloc[0]                                        #Se guarda el puntaje promedio obtenido de las reseñas

        if votos >= 2000:                                                               #Si la cantidad de votos recibidos es mayor a 2000 retorno los valores guardados previamente
            return {'titulo':titulo_pelicula, 'año':anio,'voto_total':votos, 'voto_promedio':promedio}
    except IndexError:
        return {'Error':'La pelicula no esta en el catalogo o no tiene suficientes valoraciones'}
    

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):

    movies = movies_wc['cast'].astype(str).str.lower()                                   #Se convierten los valores a string y se los pone en minuscula
    lista_indices = list(movies[movies.str.contains(nombre_actor.lower())].index.values) #Se matchea con el actor ingresado
    cant_peli = len(lista_indices)                                                       #Cantidad de coincidencias
    if cant_peli > 0:                                                                    #Si hubo coincidencia
        ret_prom = 0
        for indice in lista_indices:
            ret_prom += movies_wc.iloc[indice]['return']                                 #Se acumula el retorno que tuvo
        if cant_peli > 0:
            ret_prom = (ret_prom/cant_peli).round(2)                                     #Se calcula el promedio
        else: 
            cant_peli = 0
        lista_return = [movies_wc['return'].iloc[_] for _ in lista_indices]              #Se listan todos los retornos que tuvo el actor
        valor_max = max(lista_return)                                                    #Se elige el mayor
        indice_max_return = lista_indices[lista_return.index(valor_max)]                 #Se guarda el indice que tuvo el maximo para poder devolver el maximo retorno
        return {'actor': nombre_actor,'movie_count': cant_peli,
        'max_return': movies_wc.iloc[indice_max_return]["return"].round(2), 
        'average_return': ret_prom}
    else:
        return {'Error': 'Actor no encontrado, ingrese actor/actiz nuevamente, por ejemplo: Tom Hanks'}


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
     
    movies = movies_wc['director'].str.lower()                                             #Se convierte la columna director a minuscula
    lista_indices = list(movies[movies.str.contains(nombre_director.lower())].index.values)#Se matchea con el director ingresado
    if len(lista_indices)> 0:                                                              #Si hubo coincidencias
        lista_movies = [movies_wc['title'].iloc[_] for _ in lista_indices]                 #Se guardan los titulos de peliculas que dirigio
        lista_anios = [movies_wc['release_year'].iloc[_] for _ in lista_indices]           #Se guardan los años de lanzamientos
        lista_ganancia = [movies_wc['revenue'].iloc[_] for _ in lista_indices]             #Se guardan las recaudaciones
        lista_presupuesto = [movies_wc['budget'].iloc[_] for _ in lista_indices]           #Se guardan los presupuestos
        lista_retorno = [movies_wc['return'].iloc[_] for _ in lista_indices]               #Se guardan los retornos
        retorno_total = sum(lista_retorno)                                                 #Se suman los retornos
        return {'director': nombre_director,'retorno_total_director': retorno_total,
                'peliculas': lista_movies,'anio': lista_anios,'retorno_pelicula': lista_retorno,
                'budget_pelicula': lista_presupuesto,'revenue_pelicula': lista_ganancia }
    else:
        return {'Error':'Director/a no encontrado/a, ingrese director/a nuevamente, por ejemplo: James Cameron'}    
    
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo):
    
    try:
        semilla = random.randint(0, 1000)                                                       #Se cambia la semilla cada vez que se llama a la funcion
        movies_wc_small = movies_wc.sample(frac=0.1, random_state=semilla)                      #Se toma una muestra del 10% del dataframe, en cada llamada la muestra cambia ya que la semilla es diferente
        movies_wc_small = pd.concat([movies_wc_small, movies_wc[movies_wc['title']==titulo]], ignore_index=True)#Se suma la pelicula ingresada al dataframe 
        movies_wc_small.drop_duplicates(subset=['title'], inplace=True)                         #Se elimina duplicados por si la pelicula ingresada justo habia sido seleccionada en el 10%      
        movies_wc_small['tagline'] = movies_wc_small['tagline'].fillna('')                      #Se rellena con strings vacios en la columna de la frase celebre donde haya valores nulos 
        movies_wc_small['over_tag'] = movies_wc_small['overview'] + movies_wc_small['tagline']  #Se crea una columna nueva con la suma de la frase celebre de la pelicula y el resumen de la misma
        movies_wc_small['over_tag'] = movies_wc_small['over_tag'].fillna('')                    #Se rellena con strings vacios donde quedaron datos nulos
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 1),min_df=1, stop_words='english') #Se crea un objeto TfidfVectorizer que convierte documentos de texto en una matriz de características TF-IDF.
        matriz_frec = tf.fit_transform(movies_wc_small['over_tag'])                             #Se crea una matriz de características TF-IDF donde cada fila representa una pelicula y cada columna representa un término en el cuerpo.
        cosine_sim = linear_kernel(matriz_frec, matriz_frec)                                    #Se calcula la similitud del coseno entre todas las películas en la matriz de características.
        movies_wc_small = movies_wc_small.reset_index()                                         #Se resetean indices
        titulos = movies_wc_small['title']                                                      #Se crea una serie con los titulos de las peliculas
        indices = pd.Series(movies_wc_small.index, index=movies_wc_small['title']).drop_duplicates() #Se crea una serie con los indices de las peliculas  
        idx = indices[titulo]                                                                   #Se obtiene el indice de la pelicula ingresada
        sim_scores = list(enumerate(cosine_sim[idx]))                                           #Se obtiene la similitud entre la pelicula ingresada y el dataframe muestreado
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)                       #Se ordena la lista de similitudes
        sim_scores = sim_scores[1:6]                                                            #Se eligen las 5 primeras
        movie_indices = [i[0] for i in sim_scores]                                              #Se obtiene los indices de las elegidas
        lista = list(titulos.iloc[movie_indices])                                               #Se listan las peliculas elegidas por su similitud
        
        return {'Lista recomendada': lista }
     
    except KeyError:
        return {'Error':'Lo sentimos, la pelicula no esta en el catalogo'}


print(get_director('Woody Allen'))
print(recomendacion('Minions'))