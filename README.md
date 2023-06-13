# All About Movies

<img width="70%" src="https://github.com/SebaCen/All-about-movies/blob/main/src/Portada.jpg"> 


A partir de un dataset de peliculas se hace un analisis exploratorio del mismo luego de un proceso de ETL, se genera una API para poder interactuar 
y realizar varias consultas, ademas se genera un sistema de recomendación de peliculas aplicando Machine Larning<br> <br>


 ## Introducción
 Se trabaja sobre el siguiente dataset de <a href="https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset">Kaggle</a>, el mismo es un dataset muy completo y detallado con alrededor de 45.000 peliculas de todos los tiempos. 
  
Para realizar el proyecto se requiere extraer los datos, adecuarlos y disponibilizarlos, para que las siguientes etapas que son las del analisis de los mismos se pueda hacer adecuadamente.
  
  Tambien para que cualquier persona interesada pueda interactuar realizandoles consultas a traves de la nube. 
  
  En este repositorio encontraras las diferentes herramientas con las que se fueron desarrollando cada una de las etapas 
  definidas en el proyecto, se detalla la tabla de contenidos:
  
## Tabla de Contenidos

- [ETL](#ETL)
- [EDA](#EDA)
- [API](#API)
- [ML](#ML)
  
## <a href="https://github.com/SebaCen/All-about-movies/blob/main/All_About_Movies_ETL.ipynb">ETL </a>

Se comienza haciento un proceso de Extracción, Transformación y Carga (ETL) para limpiar el dataset de datos anomalos y desanidar columnas que vienen de esa manera en el original, tambien se adecuan los formatos acordes a las consultas que se le van a relizar posteriormente, y por ultimo se cargan en diferentes archivos para el posterior uso de los mismos de acuerdo los requerimientos de las
etapas posteriores
  
## <a href="https://github.com/SebaCen/All-about-movies/blob/main/All_About_Movies_EDA.ipynb">EDA</a>
Una vez que se asegura la calidad de los datos de entrada se pasa al analisis de los mismos (EDA) y se extrae mucha informacion valiosa como por ejemplo:
  
  - Cuantos datos faltantes hay, y en que atributos se encuentran?
  - Hay datos atipicos, y si es asi en que atributos estan?
  - Cuantas peliculas hay por genero?
  - Que director dirigio mas peliculas?
  - Que actor/actriz participo en mas peliculas?
  - Cuantas peliculas hay por genero cinamatografico?
  - Que relacion hay entre la popularidad de la pelicula y el presupuesto que se asigno para realizarla?
  - Las peliculas con mayor presupuesto fueron las que tuvieron mejor recaudacion?
  - Cuales son las palabras que estan mas presentes en los titulos, descripciones y frases celebres de las peliculas? 
  
 
##  <a href="https://github.com/SebaCen/All-about-movies/blob/main/main.py">API</a>
Y para hacerlo un poco mas dinamico se hace una API en FastAPI para poder realizar consultas relacionadas con las peliculas, se hace un deploy en Render para hacer disponibles esas consultas en la nube y que cualquier persona pueda utilizarla desde el lugar donde se encuentre y con cualquier dispositivo que cuente.  

https://all-about-movies-mv2h.onrender.com/
  
Una vez que se ingresa se puede agregar ("docs") al final de la url y se podran hacer consultas a traves de interface para tal fin
 
 
  
Las consultas que se le pueden realizar a la API son las siguientes:
  
  - Cantidad de peliculas estrenadas por mes del año
  
  'https://all-about-movies-mv2h.onrender.com/cantidad_filmaciones_mes/Junio'
  
  - Cantidad de peliculas estrenadas por dia de la semana
  
  'https://all-about-movies-mv2h.onrender.com/cantidad_filmaciones_dia/jueves'
  
  - Popularidad de una pelicula determinada
 
  'https://all-about-movies-mv2h.onrender.com/score_titulo/Minions' 
  
  - Puntaje promedio de reseña de una pelicula determinada
  
  'https://all-about-movies-mv2h.onrender.com/votos_titulo/American%20Pie'
  
  - Cantidad de peliculas en las que participo un actor/actriz determinado y el exito del mismo
  
  'https://all-about-movies-mv2h.onrender.com/get_actor/Robert%20Redford'
  
  - Cantidad de peliculas que dirigio determinado director y el listado de las mismas junto con su respectivo exito
  
  'https://all-about-movies-mv2h.onrender.com/get_director/Woody%20Allen'
  
## <a href="https://github.com/SebaCen/All-about-movies/blob/main/All_About_Movies_Funciones.ipynb">ML</a> 

  Para realizar un sistema de recomendacion de peliculas se utilizo Machine Learning en particular el metodo de similitud del coseno, usando el resumen de la pelicula y la frase celebre asociada a tal pelicula como datos de entrada. Con esto se busco similaridades con el resto de las peliculas del dataset. 
  
Se decidio trabajar con un dataset reducido aleatoriamente para que cada vez que se le pide una recomendación, pueda dar resultados similares pero diferentes entre si, ya que las peliculas con las que busca la similitud van cambiando constantemente.

https://all-about-movies-mv2h.onrender.com/recomendacion/Shrek



## Agradecimiento
Espero te haya gustado el proyecto y no dudes en consultarme cualquier duda. Gracias.

 ## Contacto
Sebastián Centurión 
  
e-mail:  sebastian.centurion@gmail.com 

  
                        
     
