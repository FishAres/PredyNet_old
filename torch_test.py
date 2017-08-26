#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:59:22 2017

@author: ares
"""

import sys
sys.path.append('~/home/ares/Code/PredyNet/predynet')

from helpers import *
import torch
from torch.autograd import Variable
import numpy as np


M = 20 # Size of Patch Array
ySize = 120
timelength = 1000
stim = np.zeros([M,M,timelength])
for ind in range(timelength):
    stim[:,:,ind] = getSineWavePatternPatch(size=[M,M],mult=[1,1],orientation = 0.25*ind, sf = 4,
                phase = 0,wave_type = 'sine',radius = [8,8],center = [M/2,M/2])







