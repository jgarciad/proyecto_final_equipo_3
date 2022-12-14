## Metro CDMX: encontrando la ruta más corta

### Miembros del equipo y roles

| Nombre  | Clave única |
| ------------- | ------------- |
| Sandra Thalía España Gómez  | 203200  |
| Marco Ramos  | 142244  |
| Aline Lizeth Pérez López  | 203096  |
| Jorge García Durante  | 202945  |

### Objetivo. 

El objetivo de este proyecto consiste en encontrar la ruta más corta entre un par de estaciones del metro de la Ciudad de México. La ruta más corta se mide bajo dos contextos que son los siguientes:

* Distancia en metros. Se obtiene la distancia en metros por cada estación que se obtienen de la página oficial del metro de la CDMX.
* Afluencia. Se considera la afluencia promedio de personas por estación con el afán de encontrar la ruta con menor número de personas por estación.

### Solución teórica del problema

La formulación matemática del problema es:

$$\min \displaystyle\sum_{(i,j) \in E} c(i,j)x(i,j)$$

$\textrm{s.t.}$

$$\displaystyle\sum_{j:(i,j) \in E} x(i,j) - \displaystyle\sum_{j:(j,i) \in E} x(j,i) = b_i\:\:\:\:i=1,..,n$$

$$b_s=1, b_d=-1$$

$$b_i = 0, i\neq s,d $$

$$x(i,j) \in \{0,1\}, \forall (i,j)\in E$$

La metodología ocupada para atacar este problema consiste es utilizar el algoritmo de Dijkstra. Este tipo de métodos son conocidos como reconfiguración de etiquetas y no es el único de su clase. 

### Aplicando el algoritmo

Para aplicar el algoritmo se hizo lo siguiente:

* Se define un grafo en donde cada estación será un nodo. La conexión entre estaciones representa las aristas y el peso de cada arista estará dado por la distancia o por la afluencia según sea el problema que estemos atacando.
* Se usa la función _dijkstra_path_ de la librería _NetworkX_ de python. Dicha función recibe como parámetros un grafo, un nodo origen y un nodo desino, el resultado será un arreglo listando en orden los nodos que representan la ruta más corta. 

### Resultados y conclusiones

Al implementar el algoritmo se observan resultados muy interesantes. En primera instancia se verificaron los resultados y durante la verificación notamos que a veces la ruta más corta, aplicada a la vida real, puede no ser la más adecuada por ejemplo, en cuestión de transbordes entre líneas del metro. Este tipo de situaciones motivan a poder incluir otros factores que motivan a poder plantear un problema que derive en una solución más sofisticada. 

### Referencias

1. Festa, P. (2006). Shortest path algorithms. In Handbook of optimization in telecommunications (pp. 185–210). Springer.
2. Dijkstra, E. W. (2022). A note on two problems in connexion with graphs. In Edsger wybe dijkstra: His life, work, and legacy (pp. 287–290).
3. Dijkstra’s Shortest Path Algorithm - A Detailed and Visual Introduction. (2020). In freeCodeCamp.org. https://www.freecodecamp.org/news/dijkstras-shortest-path-algorithm-visual-introduction/
4. Dijkstra_path — NetworkX 2.8.8 documentation. (n.d.). Retrieved December 5, 2022, from https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html
5. Sanchez, G. (2012). Mapa del metro del DF con RgoogleMaps? In Mextadísticas. https://mextatistics.wordpress.com/2012/05/10/mapa-del-metro-del-df-en-rgooglemaps/
6. Optimización. (n.d.). Retrieved December 7, 2022, from https://itam-ds.github.io/analisis-numerico-computo-cientifico/README.html
