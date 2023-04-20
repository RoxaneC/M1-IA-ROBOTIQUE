#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:37:06 2022

@author: 21205907
"""

from gurobipy import *
import numpy as np
from scipy.linalg import block_diag


def resolutionUtilite(n, p, U, w):

    # calcul de w' selon le vecteur de poids w
    w_prime = [w[i] - w[i+1] for i in range(len(w)-1)]
    w_prime.append(w[-1])
    
    
    ## AUTOMATISATION DU MODÈLE SELON LES PARAMÈTRES
    # sous matrice représentant les contraintes sur r_k et b_ik
    sm_rkbik = np.bmat([np.ones((n,1)), -1*np.eye(n)])
    sm_rb = np.kron(np.eye(n), sm_rkbik)

    # sous mtrice représentant les contraintes sur les utilités z_i(x)
    sm_zi = np.multiply(U, -1)
    sm_z = np.kron(np.ones((n,1)), block_diag(*sm_zi))

    # sous matrice représentant les contraintes du nombres d'objets affectés
    sm_x = np.bmat([[np.kron(np.ones((1,n)), np.eye(p))], [np.ones((1,n*p))]])

    # sous matrice pour le remplissage par 0 du reste
    sm_zero = np.zeros((p+1, (n+1)*n))

    # Assemblage de la matrice des contraintes
    a = np.bmat( [[sm_rb, sm_z], [sm_zero, sm_x]] ).tolist()

          
    # Récupération des nombre de variables, contraintes, etc
    nbVar = n*(n+1) + p*n       # On a n 'r_k'   +   n*n 'b_ik'   +   n*p 'x_ij'
    colonnes = range(nbVar)
            
    # Explicitation des indices des colonnes représentants les variables r_k, b_ik et x_ij
    colonnes_rk = [i*(n+1) for i in range(n)]
    colonnes_bik = [i for i in range(n*(n+1)) if i not in colonnes_rk]
    colonnes_x = [i for i in range(n*(n+1), nbVar)]
    
    
    # Second membre
    b = np.concatenate( (np.zeros((1,n*n)), np.ones((1,p)), p), axis = None )

    # Coefficients de la fonction objectif
    c = []
    for i in range(n):
        aux = np.concatenate( (i+1, -1*np.ones((1,n))), axis = None) * w_prime[i]
        c.extend(aux.tolist())

    for i in range(len(colonnes_x)):
        c.append(0)
        

    ## RÉSOLUTION
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
    obj = 0
    for j in colonnes:
        obj += c[j] * x[j]
            
    # Définition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)

    # Définition des contraintes
    for i in range(len(a)-1):
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    m.addConstr(quicksum(a[-1][j]*x[j] for j in colonnes) == b[-1], "Contrainte%d" % len(a))


    # Résolution
    m.optimize()


    # Facilite la lecture finale du résultat
    list_names = []
    for i in range(n):
        for j in range(p):
            s = "x_" + str(i+1) + "," + str(j+1)
            list_names.append(s)

    # Affichage des résultats
    print("")                
    print('Solution optimale:')
    ind=0
    for j in colonnes_x:
        print(list_names[ind], '=', x[j].x)
        ind+=1
              
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    
