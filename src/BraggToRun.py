'''
Created on 8 Feb 2018

@author: jerald
'''
import BraggCalculator3
from BraggCalculator3 import *

plt.close()

bgp = 0.6 #bragg grating period in microns
w = 1.55 #light wavelength in microns
n1 = 1. #incident medium refractive index
nw = 3.075 #waveguide refractive index
ns = 1.5 #substrate refractive index
theta_i = 10. #incident angle

para = setpara(bgp, w, n1, nw, ns, theta_i)

bgp_min = 0.5 
bgp_max = 1.5
step = 0.01

plotrays(para)
findoptimumwidth(para)