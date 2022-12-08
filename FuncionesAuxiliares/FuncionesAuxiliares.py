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
