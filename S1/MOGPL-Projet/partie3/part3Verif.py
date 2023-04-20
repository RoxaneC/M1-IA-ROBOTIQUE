from part3Automatique import resolutionCoutBudget


## VÉRIFICATION ET TESTS AVEC L'EXEMPLE DE L'ARTICLE
# nb d'agents
n = 2
# nb d'objets
p = 4
# utilité
U = [[19,6,17,2],
     [2,11,4,18]]
# couts
C = [40,50,60,50]
# budget
B = 100
# pondération
w1 = [2,1]
w2 = [10,1]
w3 = [1/2,1/2]

resolutionCoutBudget(n,p,U,C,B,w1)
resolutionCoutBudget(n,p,U,C,B,w2)
resolutionCoutBudget(n,p,U,C,B,w3)