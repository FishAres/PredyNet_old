#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 12:13:28 2017

@author: root
"""
from brian2 import *
from numpy import *
from matplotlib.pyplot import *
from helpers import *

ca()
start_scope()

timelength = 200
x = arange(1,timelength)
#
#In = zeros([2,timelength-1])
#
#In[0,:] = 2 + sin(0.1*x) + cos(0.2*x) - 0.2*sin(0.5*x)
#In[1,:] = 2 + sin(0.2*x) - cos(0.1*x)
In = zeros([timelength])


for ind in range(timelength):
    if ind <= 100:
        In[ind] = 2/(1+exp(-0.2*ind))
    else:
        In[ind] = 2.8/(1+exp(-0.1*ind-100))

Input = TimedArray(In, dt = 2*ms)

tau = 10*ms

eqs_in = '''dv/dt = (-v + Input(t))/tau : 1 
        I : 1
        '''

eqs = '''dv/dt = (-(v) + I)/tau : 1 (unless refractory)
         I : 1 '''
         
stdp_eqs = '''w : 1
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             '''

gIn = NeuronGroup(1,eqs_in,threshold='v > 1', reset='v = 0',refractory = 2*ms)

N = NeuronGroup(10,eqs,threshold = 'v > 1', reset = 'v = 0',refractory = 2*ms)
N.v = 'rand()'

S = Synapses(gIn,N, 'w :1 ', on_pre = 'v_post += w')
S.connect()
S.w = 'rand()'
#
#R = Synapses(N,N, 'w : 1', on_pre = 'v_post -= w')
#R.connect('i!=j')
#R.w = 'rand()'
#R.delay = '1*ms'
Apre = 0.05
Apost = -1.5*Apre
wmax = 1
taupre = 10*ms
taupost = 10*ms

R = Synapses(N,N, 'w : 1', on_pre = 'v_post = clip(v_post-w,0,1)')

#R = Synapses(N,N,
#             '''w : 1
#             dapre/dt = -apre/taupre : 1 (event-driven)
#             dapost/dt = -apost/taupost : 1 (event-driven)
#             ''',
#             on_pre='''
#             v_post = clip(Apost-w,0,1)
#             apre += Apre
#             w = clip(w+apost, 0, wmax)
#             ''',
#             on_post='''
#             apost += Apost
#             w = clip(w+apre, 0, wmax)
#             ''')
R.connect()
#R.connect(p=0.2)
R.w = '0.8*rand()'
R.delay = '2*ms'


SM = StateMonitor(N,'v',record=True)
SpM = SpikeMonitor(N)

SMr = PopulationRateMonitor(N)

run(200*ms)

figure(), plot(SMr.t/ms,SMr.rate/Hz)

figure(), plot(SM.t/ms,SM.v.T)
hold(True)
plot(In.T)

figure(), plot(SpM.t/ms,SpM.i,'.')