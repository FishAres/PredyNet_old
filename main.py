#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 19:52:06 2017

@author: ares
"""

from brian2 import *
prefs.codegen.target = 'numpy'
import sys
sys.path.append('/home/ares/Code/PredyNet')
import helpers as hp
import numpy as np

M = 20 # Size of Patch Array
timelength = 1000
stim = np.zeros([M,M,timelength])
for ind in range(timelength):
    stim[:,:,ind] = hp.getSineWavePatternPatch(size=[M,M],mult=[1,1],orientation = 0.1*ind, sf = 4,
                    phase = 0,wave_type = 'sine',radius = [8,8],center = [10,10])
    
    
stim_reshaped = np.reshape(stim,[M**2,timelength])    
StimArray = TimedArray(stim_reshaped,dt = 20*ms)


taupre = taupost = 20*ms


StimGroup = NeuronGroup(M**2, 'dv/dt = (-v + stimulus(t))/(10*ms) : 1',
                threshold='v>1', reset='v=0',refractory = 5*ms)

Egroup = NeuronGroup(M**s,'dv/dt = (-v + I)/taupre : 1', threshold = 'v > 1', 
                     reset = 'v=0',refractory = 5*ms)

Ygroup = NeuronGroup(50,'dv/dt = (-v + I)/taupost : 1', threshold = 'v > 1',
                     reset = 'v=0', refractory = 5*ms)

wmax = 0.01
Apre = 0.01

S_in = Synapses(StimGroup,Egroup,on_pre )

S = Synapses(G, G,
             '''
             w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             v_post += w
             apre += Apre
             w = clip(w+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost
             w = clip(w+apre, 0, wmax)
             ''')