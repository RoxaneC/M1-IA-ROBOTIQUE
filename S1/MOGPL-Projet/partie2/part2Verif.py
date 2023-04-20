from part2Automatique import resolutionUtilite


## VÉRIFICATION ET TESTS AVEC L'EXEMPLE DE L'ARTICLE
# nb d'agents
n = 3
# nb d'objets
p = 6
# utilité
U = [[325, 225, 210, 115, 75, 50],
     [325, 225, 210, 115, 75, 50],
     [325, 225, 210, 115, 75, 50]]
# pondération
w1 = [3,2,1]
w2 = [10,7,1]
w3 = [1/3,1/3,1/3]

resolutionUtilite(n,p,U,w1)
resolutionUtilite(n,p,U,w2)
resolutionUtilite(n,p,U,w3)
