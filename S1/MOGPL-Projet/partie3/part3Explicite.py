#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 17:22:31 2022

@author: 21205907
"""

from gurobipy import *


nbcont=5
nbvar=10

list_names = ['r_1','b_1,1','b_2,1',
              'r_2','b_2,1','b_2,2',
              'x_1','x_2','x_3','x_4']

# Intervalles de nos variables
lignes = range(nbcont)
colonnes = range(nbvar)

# Explicitation des colonnes représentants les variables r_k, b_ik et x_i
colonnes_rk = [0,3]
colonnes_bik = [1,2,4,5]
colonnes_x = [6,7,8,9]

# Matrice des contraintes
a = [[1, -1,  0,  0,  0,  0, -19,  -6, -17,  -2],
     [1,  0, -1,  0,  0,  0,  -2, -11,  -4, -18],
     [0,  0,  0,  1, -1,  0, -19,  -6, -17,  -2],
     [0,  0,  0,  1,  0, -1,  -2, -11,  -4, -18],
     [0,  0,  0,  0,  0,  0,  40,  50,  60,  50]]

# Second membre
b = [0,0,0,0, 100]

# Coefficients de la fonction objective
c = [1,-1,-1,2,-1,-1,0,0,0,0]

# Création de modèle
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
          
    # les x_i sont binaires (1 ou 0)
    if i in colonnes_x:
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))

     
# MAJ du modèle pour integrer les nouvelles variables
m.update()
obj = LinExpr();
obj = 0
for j in colonnes:
    obj += c[j] * x[j]
        
# Définition de l'objectif (maximisation de la fonction objectif)
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
