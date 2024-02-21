# Readify

Readify es un sistema de recomendación de libros que constituye el *Proyecto Investigativo* de la asignatura: *Sistemas de Recuperación de Información* de la carrera de *Ciencias de la Computación*, *Universidad de la Habana*, . Cuenta con una base de datos de *271360* libros obtenidos de *´Amazon Web Services´*, y recopilados en [kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data), una comunidad de IA y Machine Learning que provee conjuntos de datos para varios temas de proyectos. El objetivo es tomar un conjunto de libros que el usuario ha leído y calificado, y a partir de este se le recomiendan otros libros que pueden interesarle. 



------

## Autores:

Claudia Alvarez Martínez

Roger Moreno Gutiérrez





## Tecnologías:

El funcionamiento del proyecto está basado en APIs, definidas en un servidor de **Django**, por lo que el lenguaje de programación fundamental en el backend es **python**, la interfaz gráfica es una *Single Page Application (SPA)* desarrollada en **React**, y utiliza el lenguaje **typescript**. En el directorio raiz del proyecto se encuentra el archivo `requirements.txt`, que contiene las dependencias fundamentales del servidor de Django, mientras que las dependencias de React están en `src/gui/package.json`. Para instalarlas se puede iniciar una terminal y:

Desde la carpeta raiz, para instalar las dependencias de Django:

```bash
pip install -r requirements.txt
```

Desde el directorio `.../src/gui`, para instalar las dependencias de React:

```bash
npm install
```





## Instrucciones de ejecución:

Una vez instaladas todas las dependencias, se puede ejecutar el proyecto, pero antes es necesario realizar un precómputo de los datos que ayuda a un manejo más eficiente de los datos en ejecución, para ello se ejecuta el archivo `setup.py` desde una terminal del sistema en el directorio``../src/code/`:

```bash
py setup.py
```

Luego de precomputar los datos, se pueden iniciar ambos servidores.

Para ello se ejecuta el servidor de Django desde `.../src/code`, con el siguiente comando en la terminal:

```bash
py manage.py
```

Y el servidor de React en un entorno de desarrollo desde `.../src/gui`, con el comando en la terminal:

```bash
npm run dev
```

Una vez iniciados ambos servidores se puede acceder desde el navegador a la interfaz web por la dirección que se muestra en la terminal del servidor de React.

> Las acciones anteriores se resumieron en un archivo ejecutable en la raiz del proyecto. Para **Mac** o **Linux** el archivo `startup.sh` y para **Windows** `startup.bat`





## Sobre los datos:

En el directorio `.../src/data` se encuentran los datos fundamentales para el funcionamiento del proyecto.



### Dataset:

`Books.csv`: Contiene *271360* libros, de los cuales se tiene información como su identificador ISBN, el título, el autor, el año de su publicación, la editora que lo publica, el URL de imágenes de la portada en varios tamaños, el promedio de puntuación basada en usuarios, y la cantidad de puntuaciones.

`Users.csv`: Tiene la representación de los usuarios, donde la identificación de los usuarios se han anonimizado mapeando esta a números enteros. Además contiene datos demográficos como la ubicación de estos y la edad.

`Ratings.csv`: Es un registro de calificaciones de los libros, cada fila contiene el rating otorgado por un usuario a un libro, ya sea de forma explícita expresado en una escala de 1-10, o de forma implícita con un 0.

> En Teoría de la recomendación, las calificaciones explícitas son probablemente las más precisas, pero su desventaja es el esfuerzo extra que requieren del usuario. POr otro lado las calificaciones implícitas pueden recopilarse en un mayor volumen y sin la intervención del usuario, pero no se puede asegurar que el comportamiento del usuario es correctamente interpretado



### Auxiliares:

`log.txt`: Es un archivo en el que se escribe constantemente un log del flujo del servidor al manejar las solicitudes de recomendación, ofreciendo información de los resultados.

`config.json`: Contiene la configuración de la recomendación que se realiza, de la que se hablará posteriormente.

`book_user_list.json` y `user_book_list.json`: Almacenan las relaciones implícitas entre usuarios y libros.

`explicit_ratings_matrix.json`: Diccionario de diccionarios, que representa la matriz de los ratings explícitos de los usuarios a los libros.

`indexed_books.json`: Diccionario con toda la información de los libros, que se almacena en esta estructura para un acceso más rápido.

`user_books.json`: Contiene información de los ratings del usuario de la app a libros, es el conjunto de datos a partir del cual se hace la recomendación personalizada.

`users_avg_rating.json`: Almacena el rating promedio de cada usuario de la base de datos.





## Enfoque teórico:

La técnica fundamental utilizada en el desarrollo de nuestro sistema de recomendación es la llamada **"Recomendación Colaborativa"**. La idea básica de este sistema es que si los usuarios comparten los mismos intereses en el pasado (si les interesaron los mismos libros), tendrán gustos similares en el futuro. Por ejemplo, si dos usuarios *A* y *B*, tienen un historial de gustos muy parecido, y el usuario *A* ha leído un libro que *B* no ha visto aún, es una buena idea recomendárselo. Este tipo de recomendación colaborativa se dice: "**basada en usuarios**"

¿Cómo encontramos usuarios con gustos similares al usuario para el que se quiere hacer recomendaciones?

Una métrica comunmente utilizada para determinar el conjunto de usuarios similares es el **Coeficiente de correlación de Pearson**, que arroja resultados en el conjunto $x \in [-1 , 1]$. Este se calcula en función de las calificaciones explícitas de los usuarios a los libros, las que se pueden situar en una matriz para una mejor representación. Sea $R$ la matriz descrita anteriormente, y sea $\bar{r_{a}}$ la calificación promedio del usuario $a$.
$$
simPearson(a, b) = \frac{\sum_{p \in P}{(r_{a,p} - \bar{r_a})(r_{b,p} - \bar{r_b})}}{\sqrt{\sum_{p \in P}{(r_{a,p} - \bar{r_a})^2}} {\sqrt{\sum_{p \in P}{(r_{b,p} - \bar{r_b})^2}}}}
$$
El conjunto de libros que un usuario cualquiera ha visto, es muy pequeño en comparación con el conjunto total de libros, lo que nos hace ver que la representación matricial anterior tiene muchos vacíos, es decir, es muy dispersa. Esta es una de las principales limitaciones de este método si se hace de forma exhaustiva.

El problema de (*Data sparsity*) ataca a la eficiencia de cualquier algoritmo si se examinan todos los casos, por lo que hemos optado por un método basado en grafos propuesto por ***Huang, H. Chen***, y *D. Zeng*, en el artículo "*[Applying associative retrieval techniques to alleviate the sparsity problem in collaborative filtering](https://repository.arizona.edu/bitstream/handle/10150/105493/huang.pdf)*". La propuesta busca explotar la supuesta transitividad en los gustos de los lectores, representando las relaciones de los usuarios con los libros en un grafo bipartito, para el cual, la matriz anterior indica la adyacencia entre los vertices. Sea A el usuario para el que se quiere hacer la recomendación. Si nos centramos como inicio de camino el vétice que representa a A, podemos notar que los caminos de tamaño 1 terminan en los libros que A ha calificado (denotemos el conjunto como **l1**); los caminos de tamaño 2 terminan en usuarios, a los que llamaremos vecinos de A (denotado como **l2**); y todo vértice final de un camino de tamaño 3 es un libro que potencialmente se puede recomendar (conjunto **l3**).

Con la búsqueda anterior en el grafo se pueden reducir los conjuntos de usuarios con los que comparar a A, y de libros para los que analizar una posible recomendación. 

Una vez determinada la similitud entre los usuarios, ¿cómo se puede hacer un ranking para recomendar los libros?

De la mano del coeficiente de correlacion de Pearson viene una fórmula que nos hace una predicción del posible rating que el usuario $a$ le dará a un libro $p$, basandose en los coeficientes anteriores y tomando solo el conjunto de los vecinos más cercanos de $a$, el que definiremos como: $N =$ {$b \in l2 | simPearson(a, b) > 0$}.
$$
pred(a, p) = \bar{r_a} + \frac{\sum_{v \in N}{simPearson(a, v) * (r_{v, p} - \bar{r_v})}}{\sum_{v \in N}{simPearson(a, v)}}
$$
Dadas las predicciones para todos los libros de $l3$, podemos ordenarlos, y ese será el resultado de la recomendación.





## El flujo:

Partamos de una selección mínima para el conjunto de gustos del usuario. Para ello hemos preestablecido una calificación de 10 al libro: *Harry Potter and the Chamber of Secrets (Book 2)*.



### Familizarización con la Interfaz:

Al iniciar el proyecto se mostrarán dos colecciones de 10 recomendaciones, la primera, ***Made for you***, representa el principal resultado de recomendacion de libros. La otra colección inicialmente se llama ***More from J. K. Rowling***. Ofrecen información extra del libro al hacer click sobre cada resultado individual. Ambas se explicarán más adelante.

En la barra de navegación en la parte superior se puede ver el logo de la aplicación, y dos botones, uno para cambiar la configuración de la recomendacion, y el botón ***My Library***. Empecemos por este último. Desde aquí se puede ver la lista de libros para los que el usuario ha dado un feedback al sistema de recomendación, mostrando además la calificación que se le dió. En la parte central y superior se muestra una barra de búsqueda que permite buscar libros por su título o autor para añadir a la lista del usuario, al presionar el botón para añadirlos se pedirá una puntuación en el rango $[1, 10]$ para calificar el libro. Una vez calificado se actualizará la recomendación.

El otro botón de la barra de navegación es el de ***Settings***. Muestra al usuario varios switch con los que puede modificar el enfoque de la recomendación. Hablemos de esto. En nuestro sistema una recomendación hace por defecto una búsqueda en el grafo bipartito de Huang, esto contrarresta la dispersion de los datos en la matriz de ratings implícitos, determinando un grupo de vecinos ($l2$), y por tanto un conjunto inicial de libros recomendados ($l3$). Una forma de reducir este conjunto de libros recomendados aún más es tomar solo aquellos que hayan sido leídos por algún vecino cercano del usuario, y esto es, los que tengan un coeficiente de Pearson positivo. La forma de tomar el conjunto de libros recomendados la hemos encapsulado en lo que llamamos ***Selection method***, donde la opción ***All*** devuelve el conjunto $l3$, y ***Pearson*** el conjunto aún más reducido. Luego necesitamos ordenar los resultados de la recomendación por algún criterio. A esto le llamaremos ***Ranking method***. Una primera idea ha sido devolverlos en el orden de la cantidad de ratings explícitos que tienen, esta es la opción ***Count***. El otro método aplica la predicción del rating del usuario para los libros de la selección de Pearson, cuya expresión matemática se ha visto anteriormente.

En la colección ***Made for you*** se muestran resultados de recomendación en base a todo el conjunto de libros, y siguiendo los métodos elegidos para la selección y el ranking.

La colección ***More from {AUTHOR}*** muestra una lista de recomendación que también cumple con los métodos elegidos, pero esta vez se determina cuál es el autor favorito del usuario y los resultados solo son de ese autor.



### Estructura del servidor:

En el archivo `setup.py` se realiza un análisis del conjunto de datos inicial, creando varios archivos json donde se guarda información que hace más eficiente el procesamiento de las recomendaciones. 

El directorio `.../src/code/api` contiene la aplicación de Django que mantiene una conexión entre el servidor y la interfaz web. Dentro de este directorio se encuentra el archivo `views.py`, este es el encargado de contener las APIs que escuchan solicitudes http. Inicialmente en este archivo se cargan los datos en variables de que se utilizarán para respondes las peticiones. Luego tenemos las dos funciones que responden a las solicitudes de ambas colecciones.

```python
@api_view(['GET'])
def main_recommendation(request):

@api_view(['GET'])
def author_recommendation(request):
```

 El flujo básico de estas determina los conjuntos $l1$, $l2$ y $l3$. En dependencia de la configuración que se tenga se selecciona un subconjunto de $l3$ y se ordenan los resultados, pasando a devolver una lista de estos. En particular la segunda función elige el autor favorito del usuario determinando de entre todos, al que mayor promedio de calificaciones le ha asignado. 

Luego aparecen el resto de las APIs que ayudan a manejar la interacción del usuario.

En el archivo `utils.py` se encuentran las implementaciones de las funciones de los métodos de selección, ranking, la de la búsqueda en el grafo y la que imprime el log en el txt.





## Bibliografía:

[1] Recommender Systems, An Introduction. (Dietman Jannach, Markus Zanker, Alexander Felfernig, Gerhard Friederich) (2011), http://www.cambridge.org/9780521493369

