__author__ = 'Mario'
import numpy as np

###### Initialize Parameters ######
K = 100
t = 1
S = 105
sig = .3
r = .03
div = 0
# Alpha apparently measures performance compared to the projected performance
alpha = .69
## Variables that I have no clue what they mean ##
Vbar = 0
xi = 0
# Steps in time
N = 10
#Number of simulations
M = 100

## TODO: Figure out what to set dt to
dt = 1

sig2 = sig**2
alphadt = alpha*dt
xisdt = xi*np.sqrt(dt)
erddt = np.exp((r-div)*dt)
egam1 = np.exp(2*(r-div)*dt)
egam2 = -2*erddt + 1
eveg1 = np.exp(-alpha*dt)
eveg2 = Vbar - Vbar*eveg1

sum_CT = 0
sum_CT2 = 0

beta1 = -.88
beta2 = -.42
beta3 = -.0003

for j in range(1,M):
    St1 = []
    St2 = []
    St1.append(S)
    St2.append(S)
    Vt = sig2

    MaxSt1 = max(St1)
    MaxSt2 = max(St2)