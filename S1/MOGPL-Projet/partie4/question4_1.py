#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:27:27 2022

@author:    21110121
"""
from gurobipy import *

dico_sommets = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7}

V1 = [1,2,3,4,5,6,7]
E1 = [(1,2,5),(1,4,2),(1,3,10),(2,5,4),(2,3,4),(2,4,1),(4,3,1),(4,6,3),(3,5,3),(3,6,1),(5,7,1),(6,7,1)]
V2 = [1,2,3,4,5,6,7]
E2 = [(1,2,3),(1,4,6),(1,3,4),(2,5,6),(2,3,2),(2,4,3),(4,3,4),(4,6,5),(3,5,1),(3,6,2),(5,7,1),(6,7,1)]

G1 = V1,E1
G2 = V2,E2

def solve(G):
    
    V,E = G
    
    m = Model("mogplex")
    
    # déclaration des variables de décision
    x = {}
    for (i,j,_) in E:
        x[(i,j)] = m.addVar(vtype=GRB.BINARY, name = "x%s%s"%(i,j))
    
    c = {}
    for (i,j,k) in E:
        c[(i,j)] = k
        
    m.update()
    
    # définition de l'objectif 
    
    obj = LinExpr()
    obj = 0
    for (i,j,_) in E:
        obj += c[(i,j)] * x[(i,j)]
        
    m.setObjective(obj,GRB.MINIMIZE)
    
    # définition des contraintes
    
    for(i,j,_) in E :
        if i != 1 :
            preds = [(i2,j2) for (i2,j2,c2) in E if(j2==i)]
            m.addConstr(x[(i,j)]<=quicksum([x[ind] for ind in preds]),"Contrainte conservation %s"%(i))
            
    for i in V:
        if i != 1 :
            preds = [(i2,j2) for (i2,j2,c2) in E if(j2==i)]
            m.addConstr(quicksum([x[ind] for ind in preds])<=1,"Contrainte unique %s"%(i))
        
    preds = [(i2,j2) for (i2,j2,c2) in E if j2==7]
    m.addConstr(quicksum([x[ind] for ind in preds])==1, "Contrainte atteint sommet g")
    
    m.optimize()
    
    # Affichage des résultats
    print("")                
    print('Solution optimale:')
    for (i,j) in x:
        print((i,j), '=', x[(i,j)].x)
              
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    
    if(m.status == GRB.INFEASIBLE):
        print("pas de chemin plus rapide")
        
# pour le scénario 1 :
        
solve(G1)

print("===========")
    
# pour le scénario 2 :
    
solve(G2)