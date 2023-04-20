import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import pandas as pd


POI_FILENAME = "TME2/data/poi-paris.pkl"
parismap = mpimg.imread('TME2/data/paris-48.806-2.23--48.916-2.48.jpg')
## coordonnees GPS de la carte
xmin, xmax = 2.23, 2.48  # coord_x min et max
ymin, ymax = 48.806, 48.916  # coord_y min et max
coords = [xmin, xmax, ymin, ymax]


class Density(object):
    def fit(self,data):
        pass

    def predict(self,data):
        pass

    def score(self,data):
        #A compléter : retourne la log-vraisemblance
        eps = 1e-10
        pred = self.predict(data)
        like = pred + np.where(pred == 0, eps, 0)
        return np.log(like).sum()

class Histogramme(Density):
    def __init__(self,steps=10):
        Density.__init__(self)
        self.steps = steps

    def fit(self,x):
        #A compléter : apprend l'histogramme de la densité sur x
        self.hist, self.edges = np.histogramdd(x, self.steps)

    def to_bin(self, x):
        taille = len(x)
        d1_min, d1_max = x[:,0].min(), x[:,0].max()     # min et max de première dimension
        d2_min, d2_max = x[:,1].min(), x[:,1].max()     # min et max de deuxième dimension
        d1_step = (d1_max-d1_min)/self.steps[0]       # taille du step sur dimension 1
        d1_steps = d1_min + d1_step * list(range(self.steps[0]))    # liste des changements de bins en dimension 1
        d2_step = (d2_max-d2_min)/self.steps[1]       # taille du step sur dimension 2
        d2_steps = d2_min + d2_step * list(range(self.steps[1]))    # liste des chnagements de bins en dimension 2

        res = []

        for i in range(taille):
            d1_indice = np.asarray(x[i,0]<d1_steps).nonzero() [0]
            d2_indice = np.asarray(x[i,2]<d2_steps).nonzero() [0]


    def predict(self,x):
        #A compléter : retourne la densité associée à chaque point de x
        taille = len(x)
        pred = []
        pass

class KernelDensity(Density):
    def __init__(self,kernel=None,sigma=0.1):
        Density.__init__(self)
        self.kernel = kernel
        self.sigma = sigma

    def fit(self,x):
        self.x = x

    def predict(self,data):
        #A compléter : retourne la densité associée à chaque point de data
        pass

def get_density2D(f,data,steps=100):
    """ Calcule la densité en chaque case d'une grille steps x steps dont les bornes sont calculées à partir du min/max de data. Renvoie la grille estimée et la discrétisation sur chaque axe.
    """
    xmin, xmax = data[:,0].min(), data[:,0].max()
    ymin, ymax = data[:,1].min(), data[:,1].max()
    xlin,ylin = np.linspace(xmin,xmax,steps),np.linspace(ymin,ymax,steps)
    xx, yy = np.meshgrid(xlin,ylin)
    grid = np.c_[xx.ravel(), yy.ravel()]
    res = f.predict(grid).reshape(steps, steps)
    return res, xlin, ylin

def show_density(f, data, steps=100, log=False):
    """ Dessine la densité f et ses courbes de niveau sur une grille 2D calculée à partir de data, avec un pas de discrétisation de steps. Le paramètre log permet d'afficher la log densité plutôt que la densité brute
    """
    res, xlin, ylin = get_density2D(f, data, steps)
    xx, yy = np.meshgrid(xlin, ylin)
    plt.figure()
    show_img()
    if log:
        res = np.log(res+1e-10)
    plt.scatter(data[:, 0], data[:, 1], alpha=0.8, s=3)
    show_img(res)
    plt.colorbar()
    plt.contour(xx, yy, res, 20)


def show_img(img=parismap):
    """ Affiche une matrice ou une image selon les coordonnées de la carte de Paris.
    """
    origin = "lower" if len(img.shape) == 2 else "upper"
    alpha = 0.3 if len(img.shape) == 2 else 1.
    plt.imshow(img, extent=coords, aspect=1.5, origin=origin, alpha=alpha)
    ## extent pour controler l'echelle du plan


def load_poi(typepoi,fn=POI_FILENAME):
    """ Dictionaire POI, clé : type de POI, valeur : dictionnaire des POIs de ce type : (id_POI, [coordonnées, note, nom, type, prix])
    
    Liste des POIs : furniture_store, laundry, bakery, cafe, home_goods_store, 
    clothing_store, atm, lodging, night_club, convenience_store, restaurant, bar
    """
    poidata = pickle.load(open(fn, "rb"))
    data = np.array([[v[1][0][1],v[1][0][0]] for v in sorted(poidata[typepoi].items())])
    note = np.array([v[1][1] for v in sorted(poidata[typepoi].items())])
    return data,note
    

plt.ion()
# Liste des POIs : furniture_store, laundry, bakery, cafe, home_goods_store, clothing_store, atm, lodging, night_club, convenience_store, restaurant, bar
# La fonction charge la localisation des POIs dans geo_mat et leur note.
geo_mat, notes = load_poi("bar")
geo_mat2, notes2 = load_poi("restaurant")

# Affiche la carte de Paris
show_img()
# Affiche les POIs
plt.scatter(geo_mat[:,0],geo_mat[:,1],alpha=0.8,s=3,label="Bar")
plt.scatter(geo_mat2[:,0],geo_mat2[:,1],alpha=0.8,s=3,label="Restaurant")
plt.show()
