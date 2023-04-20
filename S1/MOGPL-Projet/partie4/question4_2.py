#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 16:16:41 2022

@author: 21205907
"""

from gurobipy import *

nbcont = 14
nbvar = 18

# Explicitation des variables x :
# x1 : arc AB
# x2 : arc AC
# x3 : arc AD
# x4 : arc BE
# x5 : arc BC
# x6 : arc BD
# x7 : arc DC
# x8 : arc DF
# x9 : arc CE
# x10 : arc CF
# x11 : arc EG
# x12 : arc FG
list_names = ['x_1', 'x_2', 'x_3', 'x_4', 'x_5','x_6', 'x_7', 'x_8', 'x_9', 'x_10',
              'x_11', 'x_12', 'x_13', 'x_14', 'x_15','r_16','x_17', 'x_18','b_1,1',
              'b_2,1','r_2', 'b_2,1', 'b_2,2']

# Intervalles de nos variables
lignes = range(nbcont)
colonnes = range(nbvar)

# Explicitation des colonnes représentants les variables rk, bik et xi
colonnes_rk = [12, 15]
colonnes_bik = [13,14,16,17]
colonnes_x = [0,1,2,3,4,5,6,7,8,9,10,11]
# Explicitation des lignes pour les signes des contraintes
lignes_egal = [0,4,5,6,7,8,9]
lignes_inf = [1,2,3,10,11]


# Matrice des contraintes

a = [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # contraintes sur arcs
     [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
     [1,0,0,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,1,0,0,1,-1,0,-1,-1,0,0,0,0,0,0,0,0],
     [0,1,0,0,1,0,1,0,-1,-1,0,0,0,0,0,0,0,0],
     [0,0,0,1,0,0,0,0,1,0,-1,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,1,0,1,0,-1,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
     [5,1,2,4,4,1,1,3,3,1,1,1,1,-1,0,0,0,0], # r1 z1
     [5,1,2,4,4,1,1,3,3,1,1,1,1,0,-1,0,0,0], # r1 z1
     [3,3,6,6,2,1,4,5,1,2,1,1,0,0,0,1,-1,0], # r2 Z2
     [3,3,6,6,2,1,4,5,1,2,1,1,0,0,0,1,0,-1]] # r2 z2

# Second membre
b = [1,1,1,1,0,0,0,0,0,1,0,0]

# Coefficients de la fonction objective
c = [0,0,0,0,0,0,0,0,0,0,0,0,1, -1, -1, 2, -1, -1]

# Création de modèle
m = Model("mogplex")

# Déclaration variables de décision
x = []
for i in colonnes:
    # les rk sont réels non bornés
    if i in colonnes_rk:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r%d" % (i + 1)))

    # les bik sont supérieurs ou égaux à 0
    if i in colonnes_bik:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d" % (i + 1)))

    # les xi sont binaires (1 ou 0)
    if i in colonnes_x:
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (i + 1)))
# MAJ du modèle pour integrer les nouvelles variables
m.update()
obj = LinExpr();
obj = 0
for j in colonnes:
    obj += c[j] * x[j]

# Définition de l'objectif (maximisation de la fonction objectif)
m.setObjective(obj, GRB.MAXIMIZE)

# Définition des contraintes
for i in lignes_inf:
    m.addConstr(quicksum(a[i][j] * x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
for i in lignes_egal:
    m.addConstr(quicksum(a[i][j] * x[j] for j in colonnes) == b[i], "Contrainte%d" % i)

# Résolution
m.optimize()

# Affichage des résultats
print("")
print('Solution optimale:')
for j in colonnes_x:
    print(list_names[j], '=', x[j].x)

print("")
print('Valeur de la fonction objectif :', m.objVal)
