# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 16:34:59 2017
@author: ares
"""
#Helper functions for Predynet

import numpy as np


def _sineArray(size,mult,orientation,sf,phase,wave_type):
    xx,yy = np.meshgrid(np.linspace(0,mult[0]*2*np.pi,size[0]),np.linspace(0,mult[1]*2*np.pi,size[1]),indexing='ij');
    ramp = np.cos(orientation)*xx+np.sin(orientation)*yy;
    sinusoid = np.sin(sf*ramp+phase);
    
    sins = (sinusoid+1)/2
    if wave_type == 'square':
        sins = np.round(sins)
    sins = sins*255
    sins = np.array(sins,dtype = np.uint8)
    return np.dstack([sins,sins,sins])
    
    

def _gauss_kern(radius, size,center=[100,100]):
    """ Returns a normalized 2D gauss kernel array for convolutions """
    
    xx, yy = np.meshgrid(range(size[0]),range(size[1]))
    g = np.exp(-((xx-center[0])**2/float(radius[0])**2+(yy-center[1])**2/float(radius[1])**2))
    g = g/g.max()
    g[g<0.05]=0    
    return g
				

def getSineWavePatternPatch(size = [256,256],mult=[1,1],orientation = 0,sf = 4, phase = 0,wave_type = 'sine',radius = [20,20],center = [126,126]):
    
    pic = _sineArray(size,mult,orientation,sf,phase,wave_type)
    pic = np.array(pic[:,:,1],dtype=np.double)
    mask = _gauss_kern(radius,size,center)
    pic = np.multiply(mask,pic)
#    pic = np.dstack([pic,pic,pic])
    pic = np.array(pic,dtype = np.uint8)
    return pic



