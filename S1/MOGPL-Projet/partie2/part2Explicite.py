#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:14:46 2022

@author: 21205907
"""

import numpy as np
from gurobipy import *


# nb d'agents
n = 3
# nb d'objets
p = 6
# utilité
z = [325, 225, 210, 115, 75, 50]
# pondération
w = [3,2,1]
w_prime = [1,1,1]

list_names = ['r_1','b_1,1','b_2,1','b_3,1',
              'r_2','b_2,1','b_2,2','b_3,2',
              'r_3','b_1,3','b_2,3','b_3,3',
              'x_1,1','x_1,2','x_1,3','x_1,4','x_1,5','x_1,6',
              'x_2,1','x_2,2','x_2,3','x_2,4','x_2,5','x_2,6',
              'x_3,1','x_3,2','x_3,3','x_3,4','x_3,5','x_3,6']

# intervalles de nos variables
lignes = range(16)
colonnes = range(30)

# Explicitation des colonnes représentants les variables r_k, b_ik et x_ij
colonnes_rk = [0,4,8]
colonnes_bik = [1,2,3,5,6,7,9,10,11]
colonnes_x = [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]

# Matrice des contraintes
# -> r1  b11  b21  b31   r2  b21  b22  b32   r3  b13  b23  b33  x11  x12  x13  x14  x15  x16  x21  x22  x23  x24  x25  x26  x31  x32  x33  x34  x35  x36
a = [[1,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [1,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50,   0,   0,   0,   0,   0,   0],
     [1,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50],
     [0,   0,   0,   0,   1,  -1,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   1,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   1,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50],
     [0,   0,   0,   0,   0,   0,   0,   0,   1,  -1,   0,   0,-325,-225,-210,-115, -75, -50,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   1,   0,  -1,   0,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50,   0,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,-325,-225,-210,-115, -75, -50],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   1],
     [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1]]


# Second membre
b = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,6]

# Coefficients de la fonction objectif
c = [1,-1,-1,-1,2,-1,-1,-1,3,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

m = Model("mogplex")     
        
# Déclaration variables de décision
x = []
for i in colonnes:
     # les r_k sont réels non bornés
    if i in colonnes_rk:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r%d" % (i+1)))
    
    # les b_ik sont supérieurs ou égaux à 0
    if i in colonnes_bik:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d" % (i+1)))
          
    # les x_ij sont binaires (1 ou 0)
    if i in colonnes_x:
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))


# MAJ du modèle pour integrer les nouvelles variables
m.update()
obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
        
# MAJ du modèle pour integrer les nouvelles variables
m.setObjective(obj,GRB.MAXIMIZE)

# Définition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

# Résolution
m.optimize()

# Affichage des résultats
print("")                
print('Solution optimale:')
for j in colonnes_x:
    print(list_names[j], '=', x[j].x)
          
print("")
print('Valeur de la fonction objectif :', m.objVal)
