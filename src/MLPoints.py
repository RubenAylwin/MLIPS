############################################################################################################
# Implementation of routines for the computation fo samples per level for Multi level Monte Carlo methods. #
############################################################################################################

import numpy as np

def mlmcAdSamples(q, r, gamma, level):
    samples = np.array([gamma**(-q*2*(level))*gamma**(0.5*(l)*(q+r)) for l in range(level+1)])
    samples = np.array([1+int(a-1.) for a in samples])

    return samples

def mlmcSamples(q, r, gamma, level, flag=""):
    samples = np.array([gamma**(-q*2*(level))*gamma**(0.5*(l)*(q+r)) for l in range(level+1)])
    samples = np.array([1+int(a-1.) for a in samples])

    return samples

def mlmkSamples(q, r, gamma, level, work=None):
    samples = None
    
    if(not isinstance(work,(float, int))):
        samples = np.array([(l+1)*gamma**(-q*2*(level))*gamma**(2./3.*(l)*(q+r)) for l in range(level+1)])
    else:
        samples = samples*work/self.costSamplesML(samples)
                
    samples = np.array([1+int(a-1.) for a in samples])

    return samples
