#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.


from gurobipy import *
import gurobipy as gurobipy
import numpy as np
import matplotlib.pyplot as plt
import random as rand

dico_arcs ={'x_1':'AB', 'x_2':'AC', 'x_3':'AD', 'x_4':'BE', 'x_5':'BC','x_6':'BD', 'x_7':'DC', 'x_8':'DF', 'x_9':'CE', 'x_10':'CF',
            'x_11':'EG', 'x_12':'FG'}

# matrice des contraintes sur les arcs

a = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # contraintes sur arcs
     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
     [1, 0, 0,-1,-1,-1, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 1,-1, 0,-1,-1, 0, 0],
     [0, 1, 0, 0, 1, 0, 1, 0,-1,-1, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 1, 0,-1, 0],
     [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,-1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]]

# Explicitation des lignes pour les signes des contraintes
lignes_egal = [0, 4, 5, 6, 7, 8, 9]
lignes_inf = [1, 2, 3]
colonnes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11]
# Second membre
bsecond = [1, 1, 1, 1, 0, 0, 0, 0, 0, 1]

def temps_trajets_aleatoires():
    t = []
    for i in range(12):
        t.append([int((rand.random() * 100) % 20)])
    return t

# définition des paramètres :
n = 2
iteration = 20
v = 7 # nombre de sommets
w_stockage = []
# initialisation des résultats
t1 = []
t2 = []

for alpha in range(1,6):
    w = np.zeros(n) #initialise les poids
    for i in range(n):
        w[i] = (n-(i+1)+1/n)**alpha - (n-(i+1)/n)**alpha
    w_prim = [w[i] - w[i + 1] for i in range(len(w) - 1)]
    w_prim.append(w[n - 1])
    w_stockage.append(w)
    t1_it = []
    t2_it = []
    for i in range(iteration):
        cout1 = temps_trajets_aleatoires()
        cout2 = temps_trajets_aleatoires()
        cout = np.array([cout1,cout2])
        range_sommets = v
        range_scenarios = n
        m = Model("moglpex")
        x = []
        # déclaration des variables
        for i in range(12):
            x.append(m.addVar(vtype = GRB.BINARY, name="x%d"%(i)))
        for s in range(range_scenarios):
            z = np.array([m.addVar(vtype=GRB.CONTINUOUS,lb=0,name="z%d"%(i+1))])
            r = np.array([m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r%d" % (i + 1))])
            for k in range(range_scenarios):
                b = np.array([m.addVar(vtype=GRB.CONTINUOUS,lb=0,name="b%d_%d"%(s+1,k+1))])
        m.update()
        #définition des contraintes sur les arcs
        # on part de a
        # on arrive à g
        # somme des arc entrant - somme arcs sortant = 0
        for i in lignes_inf:
            m.addConstr(quicksum(a[i][j] * x[j] for j in colonnes) <= bsecond[i], "Contrainte d'infériorité")
        for i in lignes_egal:
            m.addConstr(quicksum(a[i][j] * x[j] for j in colonnes) == bsecond[i], "Contrainte d'égalité")
        #définition des contraintes du PL :
        for s in range(range_scenarios):
            vari = 0
            for i in range(12):
                vari += quicksum([cout[s][i]*x[i]])
            m.addConstr(z[s] == vari, "définition de z")
        for k in range(range_scenarios) :
            for i in range(range_scenarios) :
                m.addConstr(r[k]-b[i][k]<=-z[i],"contrainte de mon PL pour des temps de trajets négatifs")
        obj = LinExpr();
        obj = 0
        for k in range(range_scenarios):
            obj += w_prim[k] * ((k + 1) * r[k] - quicksum(b[i][k] for i in range(range_scenarios)))

        m.setObjective(obj, GRB.MAXIMIZE)
        m.optimize()
        # récupération du résultat pour l'itération
        vari = []
        for i in range(range_sommets):
            vari.append([x[i, j].x if isinstance(x[i, j], gurobipy.Var) else 0 for j in range(range_sommets)])
        x = np.array(vari)
        t1_it.append(z[0].x)
        t2_it.append(z[1].x)
    # récupération du résultat pour toutes les itérations
    t1.append(t1_it)
    t2.append(t2_it)

# affichage des résultats
for i in range(5):
    label = 'w = (' + str(w_stockage[i][0]) + ', ' + str(w_stockage[i][1]) + ')'
    plt.scatter(t1[i], t2[i], label=label)
plt.title('Etude de l\'impact de la pondération sur la robustesse du chemin optimal')
plt.xlabel('temps de trajet scenario 1')
plt.ylabel('temps de trajet scenario 2')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()




