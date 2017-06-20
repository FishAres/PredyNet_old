#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 19:52:06 2017

@author: ares
"""

from brian2 import *
prefs.codegen.target = 'numpy'
import sys
sys.path.append('/home/ares/Code/PredyNet/predynet')
import helpers as hp
import numpy as np
import matplotlib.pyplot as plt

start_scope()

M = 20 # Size of Patch Array
timelength = 1000
stim = np.zeros([M,M,timelength])
for ind in range(timelength):
    stim[:,:,ind] = hp.getSineWavePatternPatch(size=[M,M],mult=[1,1],orientation = 0.25*ind, sf = 4,
                    phase = 0,wave_type = 'sine',radius = [8,8],center = [10,10])
    
    
stim_reshaped = np.reshape(stim,[M**2,timelength])    
StimArray = TimedArray(stim_reshaped,dt = 10*ms)

taupre = 10*ms
taupost = 10*ms

In_eqs =  '''dv/dt = (-v + StimArray(t,i))/(10*ms) : 1 (unless refractory)
          I : 1 '''

eqs = '''dv/dt = (-v + I)/(10*ms) : 1 (unless refractory)
        I : 1 '''

stdp_eqs = '''w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             '''


StimGroup = NeuronGroup(M**2, In_eqs,
                threshold='v>1', reset='v=0',refractory = 5*ms)

Egroup = NeuronGroup(M**2, eqs, threshold = 'v > 1', 
                     reset = 'v=0',refractory = 5*ms)

Ygroup = NeuronGroup(50, eqs, threshold = 'v > 1',
                     reset = 'v=0', refractory = 5*ms)

Ygroup.v = 'rand()'

wmax = 0.5
Apre = 0.01
Apost = -1.05*Apre

S_in = Synapses(StimGroup,Egroup,on_pre = 'v_post += 1')
S_in.connect('i==j')
#S_pred = Synapses(Ygroup,Egroup,on_pre = 'v_post += 0.2')
S_pred = Synapses(Ygroup,Egroup,
             '''w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             v_post -= w
             apre += Apre
             w = clip(w+apost, -wmax, wmax)
             ''',
             on_post='''
             apost += Apost
             w = clip(w+apre, -wmax, wmax)
             ''')
S_pred.connect()
S_pred.w = 'rand()'

S_err = Synapses(Egroup,Ygroup,
             '''w : 1
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
S_err.connect()
S_err.w = 'rand()'


S_r = Synapses(Ygroup,Ygroup,
             '''w : 1
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
S_r.connect('i!=j')

Sin = SpikeMonitor(StimGroup)
Se = SpikeMonitor(Egroup)
Sy = SpikeMonitor(Ygroup)
#S_sy = StateMonitor(S_pred, ['w','apre','apost'], record=True)
Sme = StateMonitor(Ygroup,'v',record=True)
Sr = PopulationRateMonitor(Egroup)


run(500*ms)

plt.plot(Sy.t/ms,Sy.i,'.')

plt.figure()
plt.plot(Se.t/ms,Se.i,'.')