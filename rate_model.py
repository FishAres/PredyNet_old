#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 19:49:18 2017

@author: ares
"""

import numpy as np
import helpers as hp
from scipy.stats import truncnorm


M = 40 # Size of Patch Array
timelength = 3000
stim = np.zeros([M,M,timelength])
for ind in range(timelength):
    stim[:,:,ind] = hp.getSineWavePatternPatch(size=[M,M],mult=[1,1],orientation = 0.1*ind, sf = 4,
                    phase = 0,wave_type = 'sine',radius = [20,20],center = [20,20])
    
    

Stim = np.reshape(stim,[M**2,timelength])

# Set up network

eSize = M**2
ySize = 100

W = truncnorm.rvs(0.0,0.02,size = [eSize,ySize])
V = truncnorm.rvs(0,0.02,size = [ySize,eSize])
H = truncnorm.rvs(0,0.02,size = [ySize,ySize])


eta = 0.0001
y = np.zeros([1,ySize])
E = np.zeros([1, eSize])
Y = []
for t in range(2*timelength):
    In = Stim[:,np.mod(t,timelength)]
    In = (In - np.mean(In))/np.std(In)
    E = np.tanh(In - np.dot(y,V))
    y = np.tanh(np.dot(E,W) + np.dot(y,H))
    
    Y.append(E)
    
    W += eta*np.dot(E.T,y)
    V += eta*np.dot(y.T,E)
    H += eta*np.dot(y,y.T)