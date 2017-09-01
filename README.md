# PredyNet
Predictive coding-inspired neural network models

The spirit of this project is to experiment with neural network implementations of predictive coding (Rao & Ballard, 1999). Predictive coding is an influential theory in cognitive neuroscience, but at the moment remains relatively unexplored at the level of systems neuroscience. T

## Predictive Coding

In essence, predictive coding is just control theory (albeit also generalized to non-sensorimotor domains): 

<img src="control_loop.png" alt="Drawing" width="60%" height="60%" />

#####  Adapted from Keller & Hahnloser, 2009


This isn't just to explore some other neuroscience-drawn idea in artificial neural networks. The appeal of predictive coding lies in that it allows neural networks to perform Bayesian inference and fast adjustements based on their prediction errors at all levels. Furthermore, it allows for this inference to be mapped down to a subtraction. Neurons are really good at performing "subtraction". Multiplication and division not so much (though there are models that hypothesize operations like divisive normalization). 

This simple subtraction is: Predicted input - Actual input, 

where we can treat the prediction as a Bayesian prior and the error as basically any deviation of the Likelihood from being uniform. 


The underlying idea here points to a simple generative model: a "latent variable" layer, let's call it Y, tries to predict the state of the world X via a reconstruction matrix V. The layer receives as input its own prediction error in an online manner. These two-way dynamics mean that even without weight updates, Y can follow its input. This renders the architecture related to Kalman filters and similar Bayesian methods. 

However, the ultimate goal here isn't just to follow an arbitrarily complex input - it is to predict it. We can easily find a learning rule that reflects the statistics of the environment that Y wants to predict (also please tolerate this until I do the equations in Latex):

Global error = (Input - YV)^2

Therefore:

dError/dV = -2(Input -YV)Y, and the weights are updated as:

V --> V + h(Input-YV)Y, where h is the learning rate

Our architecture is designed such that the error is used as input to the Y layer. As such, the term (Input -YV) can be abbreviated to a term E. Our learning rule is therefore Hebbian (i.e. it depends only on the activities of pre-and post-synaptic neurons): V --> V + hEV

Ok, so what, when our model converges we learn a number of basic functions to reconstruct some images using a simple learning. This isn't even new (Olshausen & Field, 1997). In fact, in many ways that wasn't even new at the time: the basic scheme is an autoencoder, it just looks funny because we didn't "unfold it" and we assume symmetry in the weights (i.e. the feed-forward weights are just the transpose of the matrix V).

Of course, this isn't our goal. Our goal is for our network to learn an internal model of the world.

The idea is that at all levels our interaction with the world is a closed loop: every action we take influences our environment, and it in turn influences our sensory input. We can use this feedback in order to learn better motor strategies and to quickly react to unexpected perturbations. Now, of course, for this scheme to make any sense there must be a prediction involved. In these 
