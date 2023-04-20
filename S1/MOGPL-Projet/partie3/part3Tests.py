import numpy as np
import time
import matplotlib.pyplot as plt

from part3Automatique import resolutionCoutBudget


## TESTS ET CALCUL DU TEMPS D'ÉXECUTION
N = [2,5,10]        # nombre d'objectifs
P = [5,10,15,20]        # nombre de projets

# initialisation de l'affichage graphique
plt.figure()
plt.title("Temps d'execution selon P projets et N objectifs")
plt.xlabel("P")
plt.ylabel("Tps d'éxecution (sec)")

# boucle de test sur différents n
for n in N:
    # stocke les temps des 10 instances pour ce n
    tps_N = []

    # valeurs de pondération arbitrairement choisies entre 1 et n*n (maximum peu probable)
    # (pour s'assurer une décroissance STRICTE, on fait la somme cumulée des tirages entre 1 et n)
    w = np.cumsum(np.random.randint(1,n, size=n)).tolist()
    # tri dans l'ordre décroissant du vecteur des pondérations
    w.sort(reverse=True)

    # boucle de test sur différents p
    for p in P:
        # stocke les temps des 10 instances pour ce p
        tps_P = []

        # boucle de test sur 10 instances
        for i in range(10):
            # valeurs d'utilité arbitrairement choisies entre 0 et 100
            U = np.random.randint(100, size=(n,p)).tolist()
            # coûts arbitrairement choisis entre 0 et 100
            C = np.random.randint(100, size=p).tolist()
            # calcul du budget selon les coûts
            B = sum(C) /2
            
            # execution et calcul du temps
            debut = time.time()
            resolutionCoutBudget(n,p,U,C,B,w)
            fin = time.time()
            tps_P.append(fin - debut)
            
        # calcul et stockage du temps moyen pour p
        tps_N.append(np.mean(tps_P))
        
    # Affichage et sauvegarde des temps d'execution pour une meilleure interprétation
    plt.plot(P, tps_N, label="N= %i" %n)

plt.legend()
plt.savefig('./graph/tps_execution_part3.png')
plt.show()
