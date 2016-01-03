#!/usr/bin/python

###############################################################################
# Almacenamiento y Recuperacion de la Informacion                             #
# Fco. Javier Fernandez-Bravo Penuela                                         #
# Escuela Superior de Informatica - UCLM                                      #
# Implementacion del algoritmo PageRank para el calculo de notas              #
# El programa se ejecuta por linea de ordenes recibiendo como argumento el    #
# nombre de un archivo conteniendo una matriz cuadrada con los valores        #
# numericos que cada grupo asigna como nota a los demas grupos, asi como al   #
# suyo propio. El programa sigue la implementacion del algoritmo PageRank,    #
# con la salvedad del calculo del numero de enlaces de salida de cada uno     #
# de los nodos. Dado que la matriz de notas define un grafo completo, no      #
# tiene sentido aplicar el algoritmo PageRank estandar. En su lugar, se       #
# considera que cada nodo tiene un numero de enlaces a otro nodo de valor     #
# igual a la nota numerica que el primer nodo le asigna al segundo. De igual  #
# forma, en el momento de calcular el total de enlaces de salida de un nodo,  #
# se considera que es igual a la suma de las puntuaciones numericas que dicho #
# nodo asigna. Se toma como situacion de convergencia aquella en la que se    #
# haya completado un numero de iteraciones del algoritmo que no sea menor que #
# log(N), donde N es la dimension de la matriz de notas. Debido a que el      #
# algoritmo PageRank incorpora un mecanismo de normalizacion, con el que las  #
# sumas de los "ranks" de todos los nodos siempre sumara 1, tomamos el rank   #
# de cada nodo como la proporcion en la que este contribuye al calculo de la  #
# nota final. Asi, la nota final de un grupo A sera el sumatorio de la nota   #
# que le asigna cada grupo B multiplicada por la puntuacion de rank del grupo #
# B, para todos los grupos en la matriz de notas                              #
###############################################################################

from __future__ import division
from sys import argv, exit
import numpy as np
from math import log

def pagerank(rp, iteration = 1):
	rpp = np.zeros(s)
	c = 0
	for i in range(s):
		for j in range(s):
			# Calculo de R'(p) para cada grupo
			# Todos los grupos apuntan a todos los grupos, con un numero de 
			# enlaces igual a la calificacion que le asignan
			# R'(p) = E(q:q->p) R(q)/Nq
			rpp[i] += grades[j, i] * rp[j] / nq[j]
		c += rpp[i]
	# La constante normalizadora, c, se define como la inversa del sumatorio 
	# de los R'(p)
	c = 1 / c
	# Normalizacion de los R'(p) multiplicandolos por c
	for i in range(s):
		rp[i] = c * rpp[i]
	# Si no se ha alcanzado la situacion de convergencia, se vuelve a iterar
	if iteration < log(s):
		pagerank(rp, iteration + 1)

if len(argv) != 2:
	print 'python pagerank <input_file.txt>'
	exit(0)
grades = None
with open(argv[1], 'r') as f:
	grades = f.readlines()
if grades == None:
	exit(1)
grades[:] = [line[:-1].split() for line in grades]
s = len(grades)
nq = np.zeros(s)
# Obtenemos la matriz de notas en formato numerico, 
# leida del archivo de entrada
grades = np.array(grades, dtype = float)
# Calculamos nq, el numero de enlaces de salida, para cada uno de los grupos 
# (nodos) como la suma de todas las notas que asigna
for indexes, value in np.ndenumerate(grades):
	nq[indexes[0]] += value
# Inicialmente todos los grupos tienen la misma puntuacion de rank, 
# la inversa del numero de grupos
rp = [1 / s for n in range(s)]
pagerank(rp)
marks = np.zeros(s)
# Calculamos la nota final de cada grupo en base al rank de cada uno de los 
# grupos y la calificacion que dicho grupo le asigna
for indexes, value in np.ndenumerate(grades):
	marks[indexes[1]] += rp[indexes[0]] * value
print marks

