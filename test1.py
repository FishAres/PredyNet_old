#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 18:53:54 2017

@author: root
"""

from brian2 import *
from numpy import *
from matplotlib.pyplot import *
from helpers import *
ca()

timelength = 200
Sig = zeros([timelength])

for ind in range(timelength):
    if ind > 30:
        Sig[ind] = 1.1
    else:
        Sig[ind] = 0
        

start_scope()

Npred = 10 # latent variable neurons
NEe = 16 # excitatory error layer neurons
NEi = 4 # inhibitory error layer neurons

tau = 10*ms

sig = TimedArray(Sig,dt = 2*ms)

eqsE = ''' dv/dt = (-v + sig(t) + I)/tau : 1 (unless refractory)
          I : 1 '''
          
eqs = ''' dv/dt = (-v + I)/tau : 1 (unless refractory)
         I : 1 '''
          
E = NeuronGroup(NEe+NEi, eqsE, threshold = 'v > 1', reset = 'v = 0', refractory = 5*ms)

Ee = E[:NEe]
Ei = E[NEe:]

Y = NeuronGroup(Npred, eqs, threshold = 'v > 1', reset = 'v = 0', refractory = 5*ms)

SynIE = Synapses(Ei,Ee,'w : 1',on_pre = 'v_post -= 0.3')
SynIE.connect(p=0.2)
SynIE.w = 'rand()'

SynYE = Synapses(Y,Ei, 'w : 1', on_pre = 'v_post += 0.5')
SynYE.connect(p=0.2)
SynYE.w = 'rand()'

SynEY = Synapses(Ee,Y, 'w : 1',on_pre = 'v_post += 0.5')
SynEY.connect(p=0.2)
SynEY.w = 'rand()'

SmE = SpikeMonitor(E)
SmY = SpikeMonitor(Y)

run(400*ms)

figure(), plot(SmE.t/ms,SmE.i,'.')

figure(), plot(SmY.t/ms,SmY.i,'.')

