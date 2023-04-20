#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 16:16:41 2022

@author: 21205907
"""

from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt

dico_arcs ={'x_1':'AB', 'x_2':'AC', 'x_3':'AD', 'x_4':'BE', 'x_5':'BC','x_6':'BD', 'x_7':'DC', 'x_8':'DF', 'x_9':'CE', 'x_10':'CF',
            'x_11':'EG', 'x_12':'FG'}

list_names = ['x_1', 'x_2', 'x_3', 'x_4', 'x_5', 'x_6', 'x_7', 'x_8', 'x_9', 'x_10',
            'x_11', 'x_12', 'x_13', 'x_14', 'x_15', 'r_16', 'x_17', 'x_18', 'b_1,1',
            'b_2,1', 'r_2', 'b_2,1', 'b_2,2']



def poids(n,alpha):
    w = np.zeros(n)
    for i in range(1,n+1):
        w[i-1] = ((n-i+1)/n)**alpha - ((n-i)/n)**alpha
    return w

def w_prime(w):
    w_p = [w[i] - w[i+1] for i in range(len(w)-1)]
    w_p.append(w[-1])
    return w_p


# on tire au hasard 20 fois les temps de trajets des deux scénarios
# c'est donc les valeurs de z1 et z2 qui changent donc on doit modifier la matrice des contraintes

def matrice_contraintes(t1,t2):

    a = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # contraintes sur arcs
         [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0,-1,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 1,-1, 0,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 1, 0, 1, 0,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 0,-1, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,-1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
         [t1[0], t1[1], t1[2], t1[3], t1[4], t1[5], t1[6], t1[7], t1[8], t1[9], t1[10], t1[11], 1,-1, 0, 0, 0, 0],  # r1 z1
         [t2[0], t2[1], t2[2], t2[3], t2[4], t2[5], t2[6], t2[7], t2[8], t2[9], t2[10], t2[11], 1, 0,-1, 0, 0, 0],  # r1 z2
         [t1[0], t1[1], t1[2], t1[3], t1[4], t1[5], t1[6], t1[7], t1[8], t1[9], t1[10], t1[11], 0, 0, 0, 1,-1, 0],  # r2 Z1
         [t2[0], t2[1], t2[2], t2[3], t2[4], t2[5], t2[6], t2[7], t2[8], t2[9], t2[10], t2[11], 0, 0, 0, 1, 0,-1]]  # r2 z2
    return a


def solve(nbcont,nbvar,nb_scenarios,alpha,t1,t2):

    n = nb_scenarios
    nb = np.zeros(n)
    for i in range(n):
        nb[i] = i+1

    # Intervalles de nos variables
    lignes = range(nbcont)
    colonnes = range(nbvar)

    # Explicitation des colonnes représentants les variables rk, bik et xi
    colonnes_rk = [12, 15]
    colonnes_bik = [13, 14, 16, 17]
    colonnes_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # Explicitation des lignes pour les signes des contraintes
    lignes_egal = [0, 4, 5, 6, 7, 8, 9]
    lignes_inf = [1, 2, 3, 10, 11]

    # Matrice des contraintes
    a = matrice_contraintes(t1,t2)

    # Second membre
    b = [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]

    # mes poids :
    w = poids(n,alpha)
    w_p = w_prime(w)
    w_p1 = w_p[0]
    w_p2 = w_p[1]

    # Coefficients de la fonction objective
    c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, nb[0]*w_p1, -w_p1, -w_p1, nb[1]*w_p2, -w_p2, -w_p2]

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

    # stockage des résultats pour construire graphiques:
    result = np.zeros((len(colonnes_x)))
    for j in colonnes_x :
        result[j] = x[j].x
    # détermination du scénario : (qui fonctionnera lorsque on aura une valeur correcte de fonction objectif)
    scenario_1 = np.zeros(12)
    scenario_2 = np.zeros(12)

    for i in range(12):
        for j in range(10,12):
            scenario_1[i] = a[j][i]
        for j in range(12,14):
            scenario_2[i] = a[j][i]

    valeur_chemin = m.objVal
    scenario = 0
    valeur_s1 = 0
    valeur_s2 = 0

    for i in range(12):
        valeur_s1 += scenario_1[i] * x[j].x
        valeur_s2 += scenario_2[i] * x[j].x
    if valeur_s1 == valeur_s2 :
        scenario = 0
    elif valeur_s1 == valeur_chemin :
        scenario = 1
    elif valeur_s2 == valeur_chemin :
        scenario = 2
    
    # Affichage des résultats
    print("")
    print('Solution optimale:')
    for j in colonnes_x:
        print(list_names[j], '=', x[j].x)
        somme1 = 0
        somme2 = 0
        if x[j].x == 1 :
            print('arc :',dico_arcs.get(list_names[j]))
            print('coût arc dans scnéario 1 :',t1[j])
            print('coût arc dans scnéario 2 :', t2[j])
            somme1 += t1[j]
            somme2 += t2[j]
        print("coût du chemin scénario 1 :", somme1)
        print("coût du chemin scnénario 2 :", somme2)
    print("")
    print('Valeur de la fonction objectif :', m.objVal)

    print("Scénario :",scenario)
    return result
# fonction renvoie quels arc ont été sélectionés, soit le meilleur chemin robuste

# on veut :
# n=2
# 20 instances de chemins
# pour : alpha = 1, alpha = 2, alpha = 3, alpha = 4, alpha = 5 soit 5 graphiques :
# il faudrait que ma fonction renvoie les résultats des arcs et le scénario choisit comme ça
# je met les variables de l'autre scénario pour faire mon graph
n = 2
nbcont = 14
nbvar = 18

# tirage des 20 instances de temps pour mes scénarios
tS1 = []
tS2 = []
for i in range(20):
    tS1.append(np.random.randint(1,10, size=12).tolist())
    tS2.append(np.random.randint(1,10, size=12).tolist())

for alpha in range(1,6):
    plt.figure()

    axe_abscisse = []
    axe_ordonne = []
    for i in range(20):
        result = solve(nbcont,nbvar,n,alpha, tS1[i], tS2[i]) # un array
        for y in range(12):
            if result[y]== 1:
                axe_abscisse.append(tS1[i][y])
                axe_ordonne.append(tS2[i][y])

    plt.scatter(axe_abscisse,axe_ordonne)

    plt.title("Impact de la pondération sur la robustesse, alpha %x" %alpha)
    plt.xlabel("scénario 1")
    plt.ylabel("scénario 2")
    nfile = "./graph/pondération_alpha%x" %alpha + ".png"
    plt.savefig(nfile)

plt.show()
