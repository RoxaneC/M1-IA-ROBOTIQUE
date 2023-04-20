# M1-MOGPL-Projet

Ce projet a pour but de réflechir sur des questions d'optimisation équitable. Le code présent ici répond à plusieurs cas particuliers mentionnés dans l'article joint au sujet.

## Prérequis

Ce projet a été développé en Python3 et requiert donc un executeur python.

Il utilise divers modules qui sont indispensables à son fonctionnement :

* gurobipy              (résolution de programme linéaire)
* numpy                 (simplification de l'usage des listes)
* scipy.linalg          (simplification de construction de matrice par blocs)
* time                  (calcul du temps d'execution)
* matplotlib.pyplot     (affichage et sauvegarde des graph)

Ces modules peuvent être installé si besoin par la commande `pip install <nom_du_module>`

## Descriptions

L'archive est découpée en 4 sous dossiers correspondant chacun au code de la partie du sujet correspondante. Il faut en extraire les dossiers pour pouvoir executer les différentes parties.

Le dossier `partie1` contient le code répondant à la question 4 de la première partie (exemple 1 du sujet). Il ne contient que le fichier `part1Question4.py` effectuant à la résolution de cet exemple.

Le dossier `partie2` contient le code répondant aux problematiques de la deuxième partie :

* Le fichier `part2Explicite.py` décrit de manière explicite les définitions des différentes matrices pour le premier exemple de l'article. Les valeurs de la matrice des contraintes, du second membre et de la fonction objectif sont entrée à la main en suivant le raisonnement indiqué dans le rapport.
* Le fichier `part2Automatique.py` automatise pour des entrées différentes la résolution du problème d'affectation d'objets selon le nombre de personnes et leurs utilités relatives.
* Le fichier `part2Verif.py` vérifie le bon fonctionnement de la formule automatique de résolution suivant l'exemple de l'article.
* Le fichier `part2Tests.py` effectue plusieurs tests de résolution selon des nomdres d'agents, d'objets, et des valeurs d'utilités différentes. Il effectue également un calcul moyen du temps d'execution selon ces paramètres. (attention, suivant l'aléatoire, le temps d'execution peut devenir très long; `Ctrl + C` permet de sortir de la boucle actuelle et donc de forcer la fin de calcul pour l'instance en cours).

Le dossier `partie3` contient le code répondant aux problematiques de la troisième partie :

* Le fichier `part3Explicite.py` décrit de manière explicite les définitions des différentes matrices pour le deuxième exemple de l'article. Les valeurs de la matrice des contraintes, du second membre et de la fonction objectif sont entrée à la main en suivant le raisonnement indiqué dans le rapport.
* Le fichier `part3Automatique.py` automatise pour des entrées différentes la résolution du problème d'acceptation de projets selon les objectifs et leurs utilités relatives.
* Le fichier `part3Verif.py` vérifie le bon fonctionnement de la formule automatique de résolution suivant l'exemple de l'article.
* Le fichier `part3Tests.py` effectue plusieurs tests de résolution selon des nomdres d'agents, d'objets, et des valeurs d'utilités différentes. Il effectue également un calcul moyen du temps d'execution selon ces paramètres.

Le dossier `partie4` contient le code répondant aux problematiques de la quatrième partie :

* Le fichier `question4_1.py` calcule le chemin le plus rapide pour chaque scénario du sommet a vers le sommet g du graphe donnée en exemple dans l'énoncé, pour cela on résouds un programme linéaire en se basant sur la contrainte de conservation du flot et on minimise le coût du chemin en minimisant la somme des coût des arcs.
* Le fichier `question4_2.py`calcule le chemin le plus robuste à travers les deux scénarios possibles du sommet a vers le sommet g du graphe donnée en exemple dans l'énoncé, pour cela nous linéarisons d'abord le problème puis nous appliquons les contraintes du problème linéarisé et les contraintes de conservation du flot, nous cherchons à maximiser sur des coûts négatifs.
* Le fichier `question4_3.py` reprend l'algorithme de la question précédente et itère selon des pondérations des scénarios différentes afin d'observer l'effet de la pondération sur la robustesse du chemin. Nous visualisons les résultats des différentes itérations (20) pour chaque vecteur de poids, avec 5 vecteur de poids différents.
* Le deuxième fichier `question4_3_v2.py` présente une autre manière d'implémenter le même programme linéaire avec une implémentation manuelle des contraintes du PL et seules les contraintes sur la conservation de flot sont modélisées dans la matrice des contraintes. Devant l'incohérence de nos résultats de notre code nous avons tenter une autre implémentation du même PL afin de voir si l'on obtenais quelque chose de différents nous ne sommes toutefois pas parvenues à régler les beugs de cette nouvelle implémentation.

## Éxecution

Pour executer l'un des programmes, utiliser dans un terminal dans le repertoire courant :
`python </partieX/nom_du_fichier.py>`   (remplacer X par la partie concernée)

## Auteurs

Développé par CELLIER Roxane et REY Soraya