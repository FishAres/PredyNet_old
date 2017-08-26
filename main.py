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
from helpers import *
import numpy as np
from matplotlib.pyplot import *
close('all')

start_scope()

M = 20 # Size of Patch Array
ySize = 120
timelength = 1000
stim = np.zeros([M,M,timelength])
for ind in range(timelength):
    if ind < 200:
        stim[:,:,ind] = getSineWavePatternPatch(size=[M,M],mult=[1,1],orientation = 0.25*ind, sf = 4,
                    phase = 0,wave_type = 'sine',radius = [8,8],center = [M/2,M/2])
    else:
        stim[:,:,ind] = getSineWavePatternPatch(size=[M,M],mult=[1,1],orientation = 0.25*ind, sf = np.mod(0.1*ind,6),
                    phase = 0,wave_type = 'sine',radius = [8,8],center = [M/2,M/2])
        stim[:,:,ind] = np.zeros([M,M])
    
stim_reshaped = np.reshape(stim,[M**2,timelength])    
StimArray = TimedArray(stim_reshaped,dt = 0.5*ms)

taupre = 20*ms
taupost = 20*ms

In_eqs =  '''dv/dt = (-v + StimArray(t,i))/(10*ms) : 1 (unless refractory)
          I : 1 '''

eqs = '''dv/dt = (-v + I)/(10*ms) : 1 (unless refractory)
        I : 1 '''

stdp_eqs = '''w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             '''


StimGroup = NeuronGroup(M**2, In_eqs,
                threshold='v>1', reset='v=0',refractory = 2*ms)

Egroup = NeuronGroup(M**2, eqs, threshold = 'v > 1', 
                     reset = 'v=0',refractory = 2*ms)

Ygroup = NeuronGroup(ySize, eqs, threshold = 'v > 1',
                     reset = 'v=0', refractory = 2*ms)

Ygroup.v = 'rand()'

wmax = 20
Apre = 0.015
Apost = 1.05*Apre

WinSize = 8
WinScale = M**2/ySize

S_in = Synapses(StimGroup,Egroup,on_pre = 'v_post += 1')
S_in.connect('i==j')

# Feedback synapses (prediction)
S_pred = Synapses(Ygroup,Egroup,
             '''w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             v_post = clip(v_post-w,0,2)
             apre += Apre
             w = clip(w+apost, -wmax, wmax)
             ''',
             on_post='''
             apost += Apost
             w = clip(w+apre, -wmax, wmax)
             ''')
#S_pred.connect('(j/WinScale) == i')
S_pred.connect('abs(WinScale*i-j)<=WinSize')
S_pred.w = 'rand()'

# Feed-forward synapses (error)
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
S_err.connect('abs(WinScale*j-i)<=WinSize')
S_err.w = 'rand()'

# Recurrent synapses on Y layer

S_r = Synapses(Ygroup,Ygroup,
             '''w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             v_post = clip(v_post+w,0,2)
             apre -= Apre
             w = clip(w+apost, -wmax, wmax)
             ''',
             on_post='''
             apost += Apost
             w = clip(w+apre, -wmax, wmax)
             ''')
#S_r.connect('i!=j')
#S_r.connect('abs(i-j) >= 20')s
S_r.connect(p=0.2)


Sin = SpikeMonitor(StimGroup)
Se = SpikeMonitor(Egroup)
Sy = SpikeMonitor(Ygroup)
#S_sy = StateMonitor(S_pred, ['w','apre','apost'], record=True)
#Smy = StateMonitor(Ygroup,'v',record=True)
Smy = PopulationRateMonitor(Ygroup)
#Sme = StateMonitor(Egroup,'v',record=True)
Sme = PopulationRateMonitor(Egroup)
Smw = StateMonitor(S_pred,'w',record=True)


run(400*ms)

figure()
plot(Sy.t/ms,Sy.i,'.')

figure()
plot(Se.t/ms,Se.i,'.')

#figure()
#plot(Sin.t/ms,Sin.i,'.')
