# All About Movies

A partir de un dataset de peliculas se hace un analisis exploratorio del mismo luego de un proceso de ETL, se genera una API para poder interactuar 
y realizar varias consultas, ademas se genera un sistema de recomendación de peliculas aplicando Machine Larning<br> <br>

<p align=center><img src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/proceso.jpg"><p> <br> 
  
 ## Introducción
 Se trabaja sobre el siguiente dataset de <a href="https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset">Kaggle</a>, el mismo es
  un dataset muy completo y detallado con alrededor de 45.000 peliculas de todos los tiempos. Para realizar el proyecto se requiere extraer los datos, adecuarlos y disponibilizarlos para que las siguientes etapas que son las del analisis de los mismos se pueda hacer adecuadamente. Tambien para que cualquier persona interesada pueda interactuar realizandoles consultas a traves de la nube. 
  En este repositorio encontraras las diferentes herramientas con las que se fueron desarrollando cada una de las etapas 
  definidas en el proyecto, se detalla la tabla de contenidos:
  
## Table of Contents

- [ETL](#ETL)
- [Querys](#Querys)
- [API](#API)
- [EDA](#EDA)
- [PreML](#PreML)
- [ML](#ML)
- [Gradio y Hugging Face](#Gradio)
- [Datos Iniciales](#Datos)
  
## <a href="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/Parte1-ETL.ipynb">ETL </a>
Se comienza haciento un proceso de Extracción, Transformación y Carga (ETL) para limpiar el dataset de datos anomalos y desanidar columnas que vienen de esa manera en el original, tambien se adecuan los formatos acordes a las consultas que se le van a relizar posteriormente, y por ultimo se cargan en diferentes archivos para el posterior uso de los mismos de acuerdo los requerimientos de las
etapas posteriores
  
## <a href="[https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/Parte1-ETL.ipynb](https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/Parte2-Consultas_y_API.ipynb)">EDA</a>
Una vez que se asegura la calidad de los datos de entrada se pasa al analisis de los mismos (EDA) y se extrae mucha informacion valiosa como por ejemplo:
  
  - Cuantos datos faltantes hay en que atributos se encuentran?
  - Hay datos atipicos, y si es asi en que atributos estan?
  - Cuantas peliculas hay por genero?
  - Que director dirigio mas peliculas?
  - Que actor/actriz participo en mas peliculas?
  - Cuantas peliculas hay por genero cinamatografico?
  - Que relacion hay entre la popularidad de la pelicula y el presupuesto que se asigno para realizarla?
  - Las peliculas con mayor presupuesto fueron las que tuvieron mejor recaudacion?
  - Cuales son las palabras que estan mas presentes en los titulos, descripciones y frases celebres de las peliculas? 
  
 
## API
Y para hacerlo un poco mas dinamico se hace una API en FastAPI para poder realizar consultas relacionadas con las peliculas, se hace un deploy en Render para hacer disponibles esas consultas en la nube y que cualquier persona pueda utilizarla desde el lugar donde se encuentre y con cualquier dispositivo con el que cuente.  
   
<a href="https://deta.space/discovery/r/r1z3sqkuowog8y3r"><img width="70%" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/api%20consultas.png"></a>
  
Una vez que ingreses agrega ("/docs") a la direccion url:<br>
  
<img src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/ingresar%20consultas.png">
  
Al ingresar podrás ver un menu con consultas, elige alguna de ellas, para probarla.
  
<img width= "70%" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/probandoConsulta.gif">
  
## EDA
El EDA nos permite familiarizarnos aún más con los daos, podemos conocer si hay errores, duplicados, valores faltantes, relaciones, entre otros. Uno de los problemas que me enfrenté al usar un dataset tan grande (1.5GB) es que mi computadora no tenia la suficiente capacidad, por lo que tuve que recurrir a tomar solo una muestra y así explorar las librerias especiales para el EDA, como son *pandas profiling, sweetviz, autoviz. Los reportes html que se generan puedes encontrarlos en esta <a href="https://github.com/hikikae/From-ETL-to-Machine-Learning/tree/main/Reportes%20EDA">carpeta<a>. 

- <a href="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/Parte3-EDA-1.ipynb">Parte 1.</a> Utilizando todos los datos (1.5GB)
- <a href="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/Parte3-EDA-2.ipynb">Parte 2. </a> Tomando una muestra <br>
  
<img width= "50%" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/reporteEDA.png"> <br>
 
<img width= "30%" height="200px" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/grafica.png"> <img height="200px" width= "30%" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/violin.png">

## <a href="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/Parte3-PreML.ipynb">PreML</a>
Una vez que tuve el EDA me encontré con nuevas interogantes como son:
  
- Numero de peliculas que ha calificado cada usuario
- Distribución de las calificaciones
- Película que más calificaciones tiene
- Película que menos calificaciones tiene
- Película más vista

Me pareció importante mencionar estos hallazgos y te invito a que los revises.
  
## <a href="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/Parte4-ML%20y%20Gradio.ipynb">ML</a> 
Para realizar una recomendación de una película, utilice un filtro colaborativo basado en SVD (Descomposción en Valores singulares), que sirve para reducir la dimensionalidad que para el caso de tanto volumen de datos, acorta los tiempos de procesamiento y la librerría Surprise que ayuda a aplicar los algoritmos de recomendadion. 
  
Este enfoque colaborativo se basa en la idea de que los usuarios con gustos similares calificarán de manera similar las mismas películas. 

## Gradio y Hugging Face
En el notebook anterior al final encontrarás el código que utilicé para cargar el modelo de ML utilicé Gradio y lo deployé por medio de Hugging Face.

<img width="70%" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/gradio.png">
 
  
Antes de hacer una prueba revisemos rápidamente algunos identificadores de películas.

<img width="70%" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/titulosPeliculas.png">
  
  
Te muestro como hacer una prueba con los datos más básicos:
<img width="70%" src="https://github.com/hikikae/From-ETL-to-Machine-Learning/blob/main/images/recomendacionML.gif">

  
## <a href="https://github.com/hikikae/From-ETL-to-Machine-Learning/tree/main/dataset"> Datos Iniciales</a>
    - Plataformas
        - amazon_prime_titles.csv
        - disney_plus_titles.csv
        - hulu_titles.csv
        - netflix_titles.csv
    - Ratings
        - 1.csv
        - 2.csv
        - 3.csv
        - 4.csv
        - 5.csv
        - 6.csv
        - 7.csv
        - 8.csv

## Agradecimiento y Contacto
Gracias por interesarte en mi proyecto y si tienes alguna duda no dudes en contactarte conmigo.

Angélica García Díaz ---- <a href="https://www.linkedin.com/in/angelica-garc%C3%ADa-diaz/">LinkedIn </a>, mail:  angelicagarciad@gmail.com <br>

 😇
                        
     
