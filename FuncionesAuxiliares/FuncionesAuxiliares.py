import numpy as np
import math
import pandas as pd
import networkx as nx
import random
import collections
import matplotlib.pyplot as plt

def construye_matriz_adyacencias(columnaA,columnaB,pesos,N,nodos,base):
    """
    Esta función ayuda a generar las matrices iniciales con la información
    de las distancias de las estaciones y las alfuencias de cada estación
    
    Itera a través de las bases iniciales de información donde se encuentra 
    la relación entre cada estación y genera una matriz de 164 * 164 que son 
    el número de estaciones en el sistema de transporte colectivo en CDMX
    
    """
    df1=np.zeros((N,N))
    matriz=pd.DataFrame(df1)
    matriz.columns=matriz.index=nodos
    
    for i in nodos:
        for j in nodos:
            matriz[i][j]=base[(base[columnaA]==i)&(base[columnaB]==j)][pesos]
    
    matriz = matriz.fillna(0)
    
    return matriz

def adj_matrix_2_edge_list(adj_matrix, index_name):
    """
    Esta función solamente transforma cualquier matriz cuadrada en una 
    lista de tuplas en el formato "edges list", lo cuál es muy útil
    para realizar los grafos. 
    
    Funciona iterando sobre los indices de la matriz, tomando i y j y 
    el valor respectivo. Elimina la traza para evitar grafos ciclicos.
    
    Index_name debe tener el mismo número de columnas que adj_matrix
    
    """
    edge_list = []
    matrix_len= len(adj_matrix)
    for i in range(matrix_len):
        for j in range(matrix_len):
                if i==j:
                    pass
                elif adj_matrix[i][j]==0:
                    pass
                else:
                    edge_list.append((index_name[i],index_name[j],adj_matrix[i][j]))
    edge_list = tuple(edge_list) 
    return edge_list

def algoritmo_dijkstra(matriz,origen,destino):
    """
    Esta función calcula la ruta más corta bajo una matriz previamente definida
    bajo el algoritmo dijkstra
    
    Funciona generando un grafo con los nodos de la matriz deseada y los pesos entre
    cada uno, para finalmente generar un listado de los nodos (en este caso estaciones)
    por las que el método sugiere ir de acuerdo a los criterios establecidos en la matriz
    
    """
    
    matrix = np.asarray(matriz.values)
    nodos = matriz.index

    edges_list=adj_matrix_2_edge_list(matrix, nodos)
    size = len(nodos)
    G = nx.Graph() 
    node_list = range(size)
    for node in node_list:
        G.add_node(node)
    G.add_weighted_edges_from(edges_list)
    
    ruta_final = nx.dijkstra_path(G, str(origen), str(destino))
    
    return ruta_final

################################Funciones Grafos###############################################

def adj_matrix_2_edge_list_1(adj_matrix):
    """
    Esta función solamente transforma cualquier matriz cuadrada en una 
    lista de tuplas en el formato "edges list", lo cuál es muy útil
    para realizar los grafos. 
    
    Funciona iterando sobre los indices de la matriz, tomando i y j y 
    el valor respectivo. Elimina la traza para evitar grafos ciclicos.
    
    """
    edge_list = []
    matrix_len= len(adj_matrix)
    for i in range(matrix_len):
        for j in range(matrix_len):
                if i==j:
                    pass
                else:
                    edge_list.append((i,j,adj_matrix[i][j]))
    edge_list = tuple(edge_list) 
    return edge_list


def plot_weighted_graph(matriz_adj):
    """
    input: matriz de adj
    output: grafo con weighted edges
    Esta es la función que crea el grafo. Toma una matriz de adj,
    la convierte en una edges list y crea el grafo con cada vertices proporcional 
    al valor que recibe en la matriz de adj.
    
    """
    edges_list=adj_matrix_2_edge_list_1(matriz_adj)
    # tamaño de la matriz
    size=max([row[0] for row in edges_list])+1
    
    # Creamos el objeto grafo y le indicamos la cantidad de nodos
    G = nx.Graph() 
    node_list = range(size)
    for node in node_list:
        G.add_node(node)
 
    # Indicamos que queremos una distribución simétrica y circular de los nodos
    # esto lo podemos cambiar a cualquier otra presentaciòn estética
    pos=nx.spring_layout(G)
    #nx.draw_networkx_nodes(G,pos,node_color='blue',node_size=300)
    # Graficamos las red
    # graficamos en un canvass amplio 
    plt.figure(6,figsize=(16,16)) 
    nx.draw(
    G, pos, edge_color='black', width=1, 
        linewidths=1, node_size=600, node_color='pink', 
        alpha=0.9,with_labels = True)
    
    # Agregamos los datos de los vertices y pesos
    G.add_weighted_edges_from(edges_list)
    
    # Ahora pintamos de manera iterativa cada vertice y su peso
    # a la par que normalizamos los pesos para que los vertices no nos salgan tan desproporcionados
    tupla_pesos = []
    for (node1,node2,data) in G.edges(data=True):
        tupla_pesos.append(data['weight']) #we'll use this when determining edge thickness
 
    pesos_unicos = list(set(tupla_pesos))
    for i in pesos_unicos:
        vertices_con_peso = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==i]
        # normalizamos un poco los pesos para que la anchura sea proporcional a su peso
        # este *1 lo tenemos que aumentar cuando haya pocos nodos y disminuir cuando 
        # haya más por cuestiones esteticas
        anchura = i*len(node_list)*.75/sum(tupla_pesos)
        nx.draw_networkx_edges(G,pos,edgelist=vertices_con_peso,width=anchura)
 
    plt.axis('off')
    plt.title('Grafo con vertices proporcionales (valor abs)')
    plt.show() 

def plot_labeled_graph(matriz_adj):
    """
    input: matriz de adj
    output: grafo con pesos no visibles
    
    """
    edges_list=adj_matrix_2_edge_list_1(matriz_adj)
    # tamaño de la matriz
    size=max([row[0] for row in edges_list])+1
    
    # Creamos el objeto grafo y le indicamos la cantidad de nodos
    G = nx.Graph() 
    node_list = range(size)
    for node in node_list:
        G.add_node(node)


    # Agregamos la lista de pesos en un diccionario para que sea fácil de interpretar por la función.

    G.add_weighted_edges_from(edges_list)
    edge_labels = dict([((n1, n2), round(d['weight'], 2))
                    for n1, n2, d in G.edges(data=True)])
    # graficamos en un canvass amplio 
    plt.figure(6,figsize=(16,16)) 

    # Indicamos que queremos una distribución simétrica y circular de los nodos
    # esto lo podemos cambiar a cualquier otra presentaciòn estética
    pos=nx.spring_layout(G)
    #pos = nx.spring_layout(G) #este lo activamos si queremos una gráfica asimétrica

    # Graficamos las red

    nx.draw(
    G, pos, edge_color='black', width=1, 
        linewidths=1, node_size=600, node_color='pink', 
        alpha=0.9,with_labels = True)
    # Graficamos las labels de los pesos
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,font_size=10)
 
    plt.axis('off')
    plt.title('Grafo con etiquetas de pesos')
    plt.show()