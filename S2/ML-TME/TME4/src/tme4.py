import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mltools import plot_data, plot_frontiere, make_grid, gen_arti


def perceptron_loss(w,x,y):
    y = y.reshape(-1,1)
    w = w.reshape(-1,1)
    x = x.reshape(y.shape[0],w.shape[0])
    
    cost = np.maximum(0, - np.multiply(y, x@w))
    return cost

def  perceptron_grad(w,x,y):
    y = y.reshape(-1,1)
    w = w.reshape(-1,1)
    x = x.reshape(y.shape[0],w.shape[0])
    
    grad = np.where(perceptron_loss(w,x,y) > 0, 0, np.multiply(y, x))
    return grad


class Lineaire(object):
    def __init__(self,loss=perceptron_loss,loss_g=perceptron_grad,max_iter=100,eps=0.01):
        self.max_iter, self.eps = max_iter,eps
        self.w = None
        self.loss,self.loss_g = loss,loss_g
        
    def fit(self,datax,datay):
        self.w = np.random.randn(datax.shape[1],1)
        datay = datay.reshape(-1,1)

        w_list = []
        cost_list = []

        for _ in range(self.max_iter):
            grad = self.loss_g(self.w,datax,datay)
            self.w = self.w + self.eps * grad.mean(axis=0).reshape(-1,1)
            w_list.append(self.w)

            cost = self.loss(self.w,datax,datay)
            cost_list.append(cost.mean())

        return np.array(w_list), np.array(cost_list)

    def predict(self,datax):
        label = np.sign(datax@self.w)
        return label

    def score(self,datax,datay):
        y_hat = self.predict(datax).reshape(-1,1)
        score = (y_hat == datay).mean()
        return score

def load_usps(fn):
    with open(fn,"r") as f:
        f.readline()
        data = [[float(x) for x in l.split()] for l in f if len(l.split())>2]
    tmp=np.array(data)
    return tmp[:,1:],tmp[:,0].astype(int)

def get_usps(l,datax,datay):
    if type(l)!=list:
        resx = datax[datay==l,:]
        resy = datay[datay==l]
        return resx,resy
    tmp =   list(zip(*[get_usps(i,datax,datay) for i in l]))
    tmpx,tmpy = np.vstack(tmp[0]),np.hstack(tmp[1])
    return tmpx,tmpy

def show_usps(data):
    plt.imshow(data.reshape((16,16)),interpolation="nearest",cmap="gray")



if __name__ =="__main__":
    ### Avec données du tme3 ###
    ## Tirage d'un jeu de données aléatoire avec un bruit de 0.1
    datax, datay =  gen_arti(nbex=1000,data_type=0,epsilon=0.1)
    ## Fabrication d'une grille de discrétisation pour la visualisation de la fonction de coût
    grid, x_grid, y_grid = make_grid(xmin=-2, xmax=2, ymin=-2, ymax=2, step=100)
    
    # Apprentissage
    L = Lineaire()
    w_list, cost_list = L.fit(datax, datay)
    w_opt = L.w
    
    ## Visualisation des données et de la frontière de décision pour un vecteur de poids w
    plt.figure()
    plot_frontiere(datax,lambda x : np.sign(x.dot(w_opt)),step=100)
    plot_data(datax,datay)
    
    # Visualisation du coût par itérations
    plt.figure()
    plt.plot(np.linspace(0, 99, 100), cost_list)
    plt.show()
    
    
    ### Avec données USPS 6vs9 ###
    uspsdatatrain = "../data/USPS_train.txt"
    uspsdatatest = "../data/USPS_test.txt"
    alltrainx,alltrainy = load_usps(uspsdatatrain)
    alltestx,alltesty = load_usps(uspsdatatest)
    
    ### 6vs9 ###
    neg = 6
    pos = 9
    datax,datay = get_usps([neg,pos],alltrainx,alltrainy)
    testx,testy = get_usps([neg,pos],alltestx,alltesty)
    trainy_sign = np.where(datay==pos,1,-1)
    testy_sign = np.where(testy==pos,1,-1)
    
    # Apprentissage
    L = Lineaire()
    L.fit(datax, datay)
    w_opt1 = L.w
    
    # Visualisation
    show_usps(w_opt1)
    # Print score
    print("score train =", L.score(datax,trainy_sign))
    print("score test =", L.score(testx,testy_sign))
    
    
    ### 6vsALL ###
    neg = 6
    pos = [1,2,3,4,5,7,8,9]
    datax,datay = get_usps([neg,pos],alltrainx,alltrainy)
    testx,testy = get_usps([neg,pos],alltestx,alltesty)
    trainy_sign = np.where(datay==neg,-1,1)
    testy_sign = np.where(testy==neg,-1,1)
    
    # Apprentissage
    L = Lineaire()
    L.fit(datax, datay)
    w_opt2 = L.w
    
    # Visualisation
    show_usps(w_opt2)
    # Print score
    print("score train =", L.score(datax,trainy_sign))
    print("score test =", L.score(testx,testy_sign))
    
    

    
