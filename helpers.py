# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 16:34:59 2017
@author: ares
"""
#Helper functions for Predynet

import numpy as np
from matplotlib.pyplot import *
#from brian2 import *

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

from graphviz import Digraph
import re
import torch
import torch.nn.functional as F
from torch.autograd import Variable
from torch.autograd import Variable
import torchvision.models as models


def make_dot(var):
    node_attr = dict(style='filled',
                     shape='box',
                     align='left',
                     fontsize='12',
                     ranksep='0.1',
                     height='0.2')
    dot = Digraph(node_attr=node_attr, graph_attr=dict(size="12,12"))
    seen = set()

    def add_nodes(var):
        if var not in seen:
            if isinstance(var, Variable):
                value = '('+(', ').join(['%d'% v for v in var.size()])+')'
                dot.node(str(id(var)), str(value), fillcolor='lightblue')
            else:
                dot.node(str(id(var)), str(type(var).__name__))
            seen.add(var)
            if hasattr(var, 'previous_functions'):
                for u in var.previous_functions:
                    dot.edge(str(id(u[0])), str(id(var)))
                    add_nodes(u[0])
    add_nodes(var.creator)
    return dot



#
#def viewArray(inp):
#    figure()
#    for ind in range(inp.shape[2]):
#        imshow(np.squeeze(inp[:,:,1*ind]))
#        pause(0.1)
#        title(str(ind))
#
#def visualise_connectivity(S):
#    Ns = len(S.source)
#    Nt = len(S.target)
#    figure(figsize=(10, 4))
#    subplot(121)
#    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
#    plot(ones(Nt), arange(Nt), 'ok', ms=10)
#    for i, j in zip(S.i, S.j):
#        plot([0, 1], [i, j], '-k')
#    xticks([0, 1], ['Source', 'Target'])
#    ylabel('Neuron index')
#    xlim(-0.1, 1.1)
#    ylim(-1, max(Ns, Nt))
#    subplot(122)
#    plot(S.i, S.j, 'ok')
#    xlim(-1, Ns)
#    ylim(-1, Nt)
#    xlabel('Source neuron index')
#    ylabel('Target neuron index')
#
#def ca():
#    close('all')