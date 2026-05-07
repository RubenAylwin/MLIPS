############################################################################################################
# Implementation of routines for the computation fo samples per level for Multi level Monte Carlo methods. #
############################################################################################################

import numpy as np
import logging

def mlmcAdSamples(q: float, r: float, gamma: float, level: int):
    """
    Returns samples for adaptive MLMC method.

    q: Numerical method's convergence rate.
    r: Numerical method's work growth rate.
    gamma: growth constant (the error behaves like gamma^q and the work like gamma^(-r))
    level: max level for samples.
    """
    if (not (isinstance(r, (float, int)) and isinstance(q, (float, int)) and isinstance(gamma, (float, int)))):
        raise TypeError("q, r and gamma in mlmcAdSamples should be floats or ints.")
    if (not isinstance(level, int)):
        raise TypeError("level in mlmcAdSamples should be int.")
    if (gamma < 0. or gamma > 1.):
        raise ValueError("gamma in mlmcAdSamples should be between 0 and 1.")
    if (r < 0. or q < 0.):
        raise ValueError("r and q in mlmcAdSamples should be positive.")
    r = r - q
    samples = np.array([gamma**(-q*2*(level))*gamma**(0.5*(l)*(q+r)) for l in range(level+1)])
    samples = np.array([1+int(a-1.) for a in samples])

    return samples

def mlmcSamples(q: float, r: float, gamma: float, level: int):
    """
    Returns samples for MLMC method.

    q: Numerical method's convergence rate.
    r: Numerical method's work growth rate.
    gamma: growth constant (the error behaves like gamma^q and the work like gamma^(-r))
    level: max level for samples.
    """
    if (not (isinstance(r, (float, int)) and isinstance(q, (float, int)) and isinstance(gamma, (float, int)))):
        raise TypeError("q, r and gamma in mlmcSamples should be floats or ints.")
    if (not isinstance(level, int)):
        raise TypeError("level in mlmcSamples should be int.")
    if (gamma < 0. or gamma > 1.):
        raise ValueError("gamma in mlmcSamples should be between 0 and 1.")
    if (r < 0. or q < 0.):
        raise ValueError("r and q in mlmcSamples should be positive.")
    
    samples = np.array([gamma**(-q*2*(level))*gamma**(0.5*(l)*(q+r)) for l in range(level+1)])
    samples = np.array([1+int(a-1.) for a in samples])
    return samples

def mlmcIpsSamples(q: float, r: float, gamma: float, level: int, work=None):
    """
    Returns samples for MLMC method.

    q: Numerical method's convergence rate.
    r: Numerical method's work growth rate.
    gamma: growth constant (the error behaves like gamma^q and the work like gamma^(-r))
    level: max level for samples.
    work: if a number is given, then the samples are adjusted to achieve the target amount of computational effort.
    """

    if (not (isinstance(r, (float, int)) and isinstance(q, (float, int)) and isinstance(gamma, (float, int)))):
        raise TypeError("q, r and gamma in mlmcIpsSamples should be floats or ints.")
    if (not isinstance(level, int)):
        raise TypeError("level in mlmcIpsSamples should be int.")
    if (gamma < 0. or gamma > 1.):
        raise ValueError("gamma in mlmcIpsSamples should be between 0 and 1.")
    if (r < 0. or q < 0.):
        raise ValueError("r and q in mlmcIpsSamples should be positive.")

    samples = None
    if(not isinstance(work,(float, int))):
        if (work is not None):
            logging.warning("work field in mlmcIpsSamples is not float nor int, but is not None.")
            
        samples = np.array([(l+1)*gamma**(-q*2*(level))*gamma**(2./3.*(l)*(q+r)) for l in range(level+1)])
    else:
        samples = samples*work/self.costSamplesML(samples)
                
    samples = np.array([1+int(a-1.) for a in samples])

    return samples
