#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 15:32:30 2017

@author: ares
"""
import random
import torch
from torch.autograd import Variable
from helpers import *
import numpy as np
from torchvision.transforms import Normalize


class DynamicNet(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        """
        In the constructor we construct three nn.Linear instances that we will use
        in the forward pass.
        """
        super(DynamicNet, self).__init__()
        self.input_linear = torch.nn.Linear(D_in, H)
        self.middle_linear = torch.nn.Linear(H, H)
        self.output_linear = torch.nn.Linear(H, D_in)

    def forward(self, x):
        """
        For the forward pass of the model, we randomly choose either 0, 1, 2, or 3
        and reuse the middle_linear Module that many times to compute hidden layer
        representations.

        Since each forward pass builds a dynamic computation graph, we can use normal
        Python control-flow operators like loops or conditional statements when
        defining the forward pass of the model.

        Here we also see that it is perfectly safe to reuse the same Module many
        times when defining a computational graph. This is a big improvement from Lua
        Torch, where each Module could be used only once.
        """
        h_relu = self.input_linear(x).clamp(min=0)
        
        for _ in range(random.randint(2, 4)):
            h_relu = self.middle_linear(h_relu).clamp(min=0)
        y_pred = self.output_linear(h_relu)
        return y_pred


# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 100, 500, 100

In = np.zeros([N,D_in])
for ind in range(N):
    In[ind,:] = getSineWavePatternPatch([10,10],orientation=20+0.1*ind,sf=8,phase=0,wave_type='sine',
                             radius=[4,4],center=[5,5]).flatten()

In = (In - np.mean(In))/np.std(In)

x = Variable(torch.from_numpy(In),requires_grad=True)
x = x.float()


# Create random Tensors to hold inputs and outputs, and wrap them in Variables
#x = Variable(torch.randn(N, D_in))
y = Variable(torch.randn(N, D_out), requires_grad=False)


er = Variable(torch.zeros([N, D_out]),requires_grad=True)

# Construct our model by instantiating the class defined above
model = DynamicNet(D_in, H, D_out)
y_pred = model(x)

# Construct our loss function and an Optimizer. Training this strange model with
# vanilla stochastic gradient descent is tough, so we use momentum
criterion = torch.nn.MSELoss(size_average=False)

def mse_loss(inp, target):
    return torch.sum((inp - target).pow(2)) / inp.data.nelement()
                     #optimizer = torch.optim.SGD(model.parameters(), lr=1e-5, momentum=0.9)
#optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
optimizer = torch.optim.Adagrad(model.parameters(), lr=1e-4)

E = []

for t in range(500):
    # Forward pass: Compute predicted y by passing x to the model
    y_pred = model(er).detach()

    # Compute and print loss
    loss = criterion(x, y_pred)
#    loss = mse_loss(x, y_pred)
#    print(t, loss.data[0])
    E.append(loss.data[0])

    # Zero gradients, perform a backward pass, and update the weights.
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    er = y_pred - x
plt.plot(E)