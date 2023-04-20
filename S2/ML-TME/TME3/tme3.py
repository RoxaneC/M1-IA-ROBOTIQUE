import numpy as np
import matplotlib.pyplot as plt

from mltools import plot_data, plot_frontiere, make_grid, gen_arti

def mse(w,x,y):
    # a implémenter
    y = y.reshape(-1,1)
    w = w.reshape(-1,1)
    x = x.reshape(y.shape[0],w.shape[0])
    
    cost = (x@w - y)**2
    return cost

def mse_grad(w,x,y):
    # a implémenter
    y = y.reshape(-1,1)
    w = w.reshape(-1,1)
    x = x.reshape(y.shape[0],w.shape[0])
    
    grad = 2*np.multiply(x, x@w - y)
    return grad

def reglog(w,x,y):
    #a implémenter
    y = y.reshape(-1,1)
    w = w.reshape(-1,1)
    x = x.reshape(y.shape[0],w.shape[0])
    
    cost = np.log(1+ np.exp(- np.multiply(y, x@w)))
    return cost

def reglog_grad(w,x,y):
    #a implémenter
    y = y.reshape(-1,1)
    w = w.reshape(-1,1)
    x = x.reshape(y.shape[0],w.shape[0])
    
    grad = - np.divide(np.multiply(y,x) , np.exp(np.multiply(y, x@w)) +1)
    return grad

def descente_gradient(datax,datay,f_loss,f_grad,eps,iter):
    w = np.random.randn(datax.shape[1],1)
    w_list = []
    cost_list = []

    for _ in range(iter):
        grad = f_grad(w,datax,datay)
        w = w - eps * grad.mean(axis=0).reshape(-1,1)
        w_list.append(w)
        
        cost = f_loss(w,datax,datay)
        cost_list.append(cost.mean())
        
    return w, np.array(w_list), np.array(cost_list)


def check_fonctions():
    ## On fixe la seed de l'aléatoire pour vérifier les fonctions
    np.random.seed(0)
    datax, datay = gen_arti(epsilon=0.1)
    wrandom = np.random.randn(datax.shape[1],1)
    assert(np.isclose(mse(wrandom,datax,datay).mean(),0.54731,rtol=1e-4))
    assert(np.isclose(reglog(wrandom,datax,datay).mean(), 0.57053,rtol=1e-4))
    assert(np.isclose(mse_grad(wrandom,datax,datay).mean(),-1.43120,rtol=1e-4))
    assert(np.isclose(reglog_grad(wrandom,datax,datay).mean(),-0.42714,rtol=1e-4))
    np.random.seed()


if __name__=="__main__":
    check_fonctions()
    
    
    # Hyper paramètres pour génération du jeu et apprentissage
    # (à modifier pour les différents tests)
    DATA_TYPE = 0       # 0 pour 2 gaussiennes; 1 pour 4 gaussiennes; 2 pour échiquier
    BRUIT = 0.1         # bruit des tirage (faible pour séparable; fort pour non séparable)
    EPS = 0.001         # pas du gradient
    ITER = 2000         # nombre d'itération du gradient
    
    
    ## Tirage d'un jeu de données aléatoire avec un bruit de 0.1
    datax, datay =  gen_arti(nbex=1000,data_type=DATA_TYPE,epsilon=BRUIT)
    ## Fabrication d'une grille de discrétisation pour la visualisation de la fonction de coût
    grid, x_grid, y_grid = make_grid(xmin=-2, xmax=2, ymin=-2, ymax=2, step=100)
    
    
    # Apprentissage par Descente de Gradient
    w_opt_mse, w_list_mse, cost_list_mse = descente_gradient(datax,datay,mse,mse_grad,EPS,ITER)
    w_opt_log, w_list_log, cost_list_log = descente_gradient(datax,datay,reglog,reglog_grad,EPS,ITER)
    
    
    ## Visualisation des données et de la frontière de décision pour un vecteur de poids w
    plt.figure()            # Linéaire
    plot_frontiere(datax,lambda x : np.sign(x.dot(w_opt_mse)),step=100)
    plot_data(datax,datay)
    
    plt.figure()            # Logistique
    plot_frontiere(datax,lambda x : np.sign(x.dot(w_opt_log)),step=100)
    plot_data(datax,datay)
    
    
    # Visualisation du coût par itérations
    plt.figure()
    plt.plot(np.linspace(0, ITER-1, ITER), cost_list_mse, label="cost MSE")
    plt.plot(np.linspace(0, ITER-1, ITER), cost_list_log, label="cost RegLog")
    plt.legend()
    plt.show()

    
    ## Visualisation de la fonction de coût en 2D
    plt.figure()            # Linéaire
    plt.contourf(x_grid,y_grid,np.array([mse(w,datax,datay).mean() for w in grid]).reshape(x_grid.shape),levels=20)
    
    plt.figure()            # Logistique
    plt.contourf(x_grid,y_grid,np.array([reglog(w,datax,datay).mean() for w in grid]).reshape(x_grid.shape),levels=20)
    
    
