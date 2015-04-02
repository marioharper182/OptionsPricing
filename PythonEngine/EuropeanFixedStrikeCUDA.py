__author__ = 'HarperMain'
import numpy as np
from EuropeanGreeks import *
from scipy.stats import norm
import time
from numba import *
from numbapro import cuda
import math


@cuda.jit(argtypes=(double, double, double, double, double, double, double, double, double, double,
                    double, double, double, double))
def VectorizedMonteCarlo(spot, rate, sigma, expiry, N, M, strike, sigma2, Vbar, dt, xi, alpha, dividend, tau):

    i = cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x

    beta1 = -.88
    beta2 = -.42
    beta3 = -.0003

    sigma2 = sigma**2
    alphadt = alpha*dt
    xisdt = xi*np.sqrt(dt)
    erddt = np.exp((rate-dividend)*dt)
    egam1 = np.exp(2*(rate-dividend)*dt)
    egam2 = -2*erddt + 1
    eveg1 = np.exp(-alpha*dt)
    eveg2 = Vbar - Vbar*eveg1

    # Initialize the matrices
    newdt = float(expiry)/float(N) # Get the dt for the Weiner process
    dW = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
    W = np.cumsum(dW, axis=1) # Set up the Weiner Process as a Matrix
    time = np.linspace(0, expiry, N) # Set the discrete time space
    tempA = np.zeros((M,1)) # Create an initial zero vector for the first column

    #This is the Random aspects and the stochastic volatility
    Wnew = np.c_[tempA,W] # Append the Weiner matrix to the zeros vector
    Vt = sigma2
    Vtn = np.abs(Vt + alphadt*(Vbar - Vt) + xisdt*np.sqrt(Vt)*Wnew)
    tt = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration

    ### Calculate the lookback option ###
    assetpath1 = np.array(spot*np.exp((rate-dividend-.5*Vtn)*tt+np.sqrt(Vtn)*Wnew)) #European standard
    assetpath2 = np.array(spot*np.exp((rate-dividend-.5*Vtn)*tt+np.sqrt(Vtn)*-Wnew)) #European standard

    d1_St1 = EuroD1(assetpath1, strike, rate, dividend, sigma, tau)
    d1_St2 = EuroD1(assetpath2, strike, rate, dividend, sigma, tau)
    delta1 = (d1_St1)
    delta2 = (d1_St2)
    gamma1 = EuroGamma(d1_St1, assetpath1, sigma, tau)
    gamma2 = EuroGamma(d1_St2, assetpath2, sigma, tau)
    vega1 = EuroVega(d1_St1, tau, assetpath1)
    vega2 = EuroVega(d1_St2, tau, assetpath2)

    St1n = assetpath1
    # St1n = np.c_[assetpath1, assetpath1[:,-1]]
    St2n = assetpath2
    # St2n = np.c_[assetpath2, assetpath2[:,-1]]
    St1 = np.delete(np.c_[tempA, assetpath1],-1,1)
    St2 = np.delete(np.c_[tempA, assetpath2],-1,1)

    Vt = np.delete(np.c_[Vt+tempA, Vtn],-1,1)
    # Vtn = np.c_[Vtn, Vtn[:, -1]]

    cv1, cv2, cv3 = 0,0,0
    # for i in range(len(St1n[0])):
    cv1 = cv1 + delta1*(St1n - St1*erddt) + delta2*(St2n - St2*erddt)
    cv2 = cv2 + gamma1*((St1n-St1)**2 - St1**2 * (egam1*np.exp(Vt*dt)+egam2)) + \
          gamma2*((St2n-St2)**2 - St2**2*(egam1*np.exp(Vt*dt)+egam2))
    cv3 = cv3 + vega1*((Vtn-Vt)-(Vt*eveg1+eveg2-Vt)) + \
          vega2*((Vtn-Vt)-(Vt*eveg1+eveg2-Vt))

    max_vals1 = np.array([max(assetpath1[i]) for i in range(0 , len(assetpath1))])
    max_vals2 = np.array([max(assetpath1[i]) for i in range(0 , len(assetpath1))])
    CT = .5*((max_vals1 - strike) + (max_vals2 - strike) +
             beta1*cv1[:,-1] + beta2*cv2[:,-1] + beta3*cv3[:,-1])

    sum_CT = sum(CT)
    sum_CT2 = sum([i**2 for i in CT])

    call_value = sum_CT/M *np.exp(-rate*expiry)
    SD = np.sqrt((sum_CT2 - sum_CT*sum_CT/M)*np.exp(-2*rate*expiry)/(M-1))
    SE = SD/np.sqrt(M)
    print('This is the CV method with Stochastic Volatility: ', call_value)
    print(SD, SE)

    option_val = np.array([max(i-strike,0) for i in np.array(max_vals1)])
    call_val = np.mean(option_val)
    present_val = np.exp(-rate*expiry)*call_val
    print('This is the matrix, naive monte carlo: ',present_val)

def cudait(spot, rate, dividend, sigma, strike, tau, expiry, N, M, Vbar, Wnew, tempA, Vt, Vtn, tt):
    ### Calculate the lookback option ###
    alpha = .69
    xi = .025
    dt = expiry/N
    beta1 = -.88
    beta2 = -.42
    beta3 = -.0003

    sigma2 = sigma**2
    alphadt = alpha*dt
    xisdt = xi*np.sqrt(dt)
    erddt = np.exp((rate-dividend)*dt)
    egam1 = np.exp(2*(rate-dividend)*dt)
    egam2 = -2*erddt + 1
    eveg1 = np.exp(-alpha*dt)
    eveg2 = Vbar - Vbar*eveg1
    assetpath1 = np.array(spot*np.exp((rate-dividend-.5*Vtn)*tt+np.sqrt(Vtn)*Wnew)) #European standard
    assetpath2 = np.array(spot*np.exp((rate-dividend-.5*Vtn)*tt+np.sqrt(Vtn)*-Wnew)) #European standard

    d1_St1 = EuroD1(assetpath1, strike, rate, dividend, sigma, tau)
    d1_St2 = EuroD1(assetpath2, strike, rate, dividend, sigma, tau)
    delta1 = (d1_St1)
    delta2 = (d1_St2)
    gamma1 = EuroGamma(d1_St1, assetpath1, sigma, tau)
    gamma2 = EuroGamma(d1_St2, assetpath2, sigma, tau)
    vega1 = EuroVega(d1_St1, tau, assetpath1)
    vega2 = EuroVega(d1_St2, tau, assetpath2)

    St1n = assetpath1
    # St1n = np.c_[assetpath1, assetpath1[:,-1]]
    St2n = assetpath2
    # St2n = np.c_[assetpath2, assetpath2[:,-1]]
    St1 = np.delete(np.c_[tempA, assetpath1],-1,1)
    St2 = np.delete(np.c_[tempA, assetpath2],-1,1)

    Vt = np.delete(np.c_[Vt+tempA, Vtn],-1,1)
    # Vtn = np.c_[Vtn, Vtn[:, -1]]

    cv1, cv2, cv3 = 0,0,0
    # for i in range(len(St1n[0])):
    cv1 = cv1 + delta1*(St1n - St1*erddt) + delta2*(St2n - St2*erddt)
    cv2 = cv2 + gamma1*((St1n-St1)**2 - St1**2 * (egam1*np.exp(Vt*dt)+egam2)) + \
          gamma2*((St2n-St2)**2 - St2**2*(egam1*np.exp(Vt*dt)+egam2))
    cv3 = cv3 + vega1*((Vtn-Vt)-(Vt*eveg1+eveg2-Vt)) + \
          vega2*((Vtn-Vt)-(Vt*eveg1+eveg2-Vt))

    max_vals1 = np.array([max(assetpath1[i]) for i in range(0 , len(assetpath1))])
    max_vals2 = np.array([max(assetpath1[i]) for i in range(0 , len(assetpath1))])
    CT = .5*((max_vals1 - strike) + (max_vals2 - strike) +
             beta1*cv1[:,-1] + beta2*cv2[:,-1] + beta3*cv3[:,-1])

    sum_CT = sum(CT)
    sum_CT2 = sum([i**2 for i in CT])

    call_value = sum_CT/M *np.exp(-rate*expiry)
    SD = np.sqrt((sum_CT2 - sum_CT*sum_CT/M)*np.exp(-2*rate*expiry)/(M-1))
    SE = SD/np.sqrt(M)

def main():
    timeintial = time.time()
    OPT_N = 4000000
    blockdim = 1024, 1
    griddim = int(math.ceil(float(OPT_N)/blockdim[0])), 1
    stream = cuda.stream()

    ###### Initialize Parameters ######
    strike = 80
    t = 1
    expiry = 10
    spot = 105
    sigma = .3
    rate = .03
    dividend = 0
    # Alpha apparently measures performance compared to the projected performance
    alpha = .69

    # Steps in time
    N = 10
    #Number of simulations
    M = 100

    ## TODO: Figure out what to set dt to
    dt = 1
    Vbar = 0.02
    xi = xi = .025

    N = 100
    M = 2000

    beta1 = -.88
    beta2 = -.42
    beta3 = -.0003

    sigma2 = sigma**2
    alphadt = alpha*dt
    xisdt = xi*np.sqrt(dt)
    erddt = np.exp((rate-dividend)*dt)
    egam1 = np.exp(2*(rate-dividend)*dt)
    egam2 = -2*erddt + 1
    eveg1 = np.exp(-alpha*dt)
    eveg2 = Vbar - Vbar*eveg1

    tau = expiry-t


    VectorizedMonteCarlo[griddim, blockdim, stream](spot, rate, sigma, expiry, N, M, strike, sigma2, Vbar, dt, xi, alpha, dividend, tau)
    stream.synchronize()

if __name__ == '__main__':
    main()