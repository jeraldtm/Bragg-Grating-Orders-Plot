'''
Created on 8 Feb 2018

@author: jerald
'''
import numpy as np
import math
import matplotlib.pyplot as plt

plt.close()

def setpara(grating, wavelength, n_i, n_w, n_s, theta_i):
    """
        Sets parameters
        Parameter: grating : grating period in microns : float
                 : wavelength : wavelength of incident light in microns : float
                 : n_i : refractive index of superstrate : float
                 : n_w : refractive index of waveguide : float
                 : n_s : refractive index of substrate : float                 
                 : theta_i : incident angle in degrees : float
    """
    para = [grating, wavelength, n_i, n_w, n_s, theta_i]
    return para

def braggorder(para, l):
    """
        Calculates number of orders
        Parameter: para : simulation parameters : list
                 : l : layer : string
    """  
    if l == 'sup':
        q_u = (para[0]/para[1])*((para[2]*np.sin(np.radians(para[5]))) + para[2])
        q_l = (para[0]/para[1])*((para[2]*np.sin(np.radians(para[5]))) - para[2])
        orders = np.arange(math.ceil(q_l), math.floor(q_u) + 1, 1.)
        
    elif  l == 'wav':
        q_u = (para[0]/para[1])*((para[2]*np.sin(np.radians(para[5]))) + para[3])
        q_l = (para[0]/para[1])*((para[2]*np.sin(np.radians(para[5]))) - para[3])
        orders = np.arange(math.ceil(q_l), math.floor(q_u) + 1, 1.)
    
    elif  l == 'sub':
        q_u = (para[0]/para[1])*((para[2]*np.sin(np.radians(para[5]))) + para[4])
        q_l = (para[0]/para[1])*((para[2]*np.sin(np.radians(para[5]))) - para[4])
        orders = np.arange(math.ceil(q_l), math.floor(q_u) + 1, 1.)
    return orders

def angle(para, q, l):
    """
        Calculates output angle
        Parameter: para : simulation parameters : list
                 : q : order : float
    """
    if l == 'sup':
        angle = np.degrees(np.arcsin((para[2]*np.sin(np.radians(para[5])) - \
                q*para[1]/para[0])/para[2]))

    elif l == 'wav':
        angle = np.degrees(np.arcsin((para[2]*np.sin(np.radians(para[5])) - \
                q*para[1]/para[0])/para[3]))

    elif l == 'sub':
        angle = np.degrees(np.arcsin((para[2]*np.sin(np.radians(para[5])) - \
                q*para[1]/para[0])/para[4]))

    return angle
        
def plotray(angle, l, q, c, ax):
    """
        Plots a single ray
        Parameter: angle : float
                 : d : direction : string
                 : q : order : float
                 : c : colour : string
                 : ax : figure
    """
    if math.isnan(angle):
        return
    
    x = [0,]
    y = [0,]
    if l == 'sup':
        x.append(np.sin(np.radians(angle)))
        y.append(np.cos(np.radians(angle)))
    elif l == 'wav':
        x.append(np.sin(np.radians(angle)))
        y.append(-np.cos(np.radians(angle)))
    
    elif l == 'sub':
        x.append(np.sin(np.radians(angle)))
        y.append(-np.cos(np.radians(angle)))
    
    elif l == 'inc':
        x.append(-np.sin(np.radians(angle)))
        y.append(np.cos(np.radians(angle)))
        
    ax.plot(x, y, c, label = l + '%1.0f %4.3f' %(q,angle))
    
def setaxis(ax):
    x = [-1., 1.]
    zero = [0.,0.]
    ax.plot(x,zero, 'k')
    ax.axis([-1,1, -1, 1])

def plotrays(para):
    """
        Plots input and output rays through grating
        Parameter: lambdag : grating period in microns : float
                 : lambdaw : wavelength of incident light in microns : float
                 : n_i : refractive index of superstrate : float
                 : n_t : refractive index of transmission medium
                 : theta_i : incident angle in degrees : float
    """
    #color = ['r', 'g', 'b', 'c', 'm', 'y']    
    
    fig, ax = plt.subplots()
    setaxis(ax)
    
    orders_sup = braggorder(para, 'sup')
    orders_wav = braggorder(para, 'wav')
    orders_sub = braggorder(para, 'sub')
    
    plotray(para[5], 'inc', 0, 'k', ax) 
    
    for i in range(len(orders_sup)):
        theta = angle(para, orders_sup[i], 'sup')
        plotray(theta, 'sup', orders_sup[i], 'b', ax)
    
    for i in range(len(orders_wav)):
        theta = angle(para, orders_wav[i], 'wav')
        plotray(theta, 'wav', orders_wav[i], 'r', ax)
    
    for i in range(len(orders_sub)):
        theta = angle(para, orders_sub[i], 'sub')
        plotray(theta, 'sub', orders_sub[i], 'g', ax)
     
    ax.legend()
    plt.show()
    
def findoptimumwidth(para):
    lambdamax = np.abs(2*para[1]/(para[2]*np.sin(np.radians(para[5]))-para[3]))
    lambdamin = np.abs(para[1]/(para[2]*np.sin(np.radians(para[5]))-para[3]))
    lambdasub = np.abs(para[1]/(para[2]*np.sin(np.radians(para[5]))-para[4]))
    
    print 'G < %1.1f, %1.1f < G < %1.1f' %(lambdamax, lambdamin, lambdasub)
