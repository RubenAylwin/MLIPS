################################################################
# Implementation of different Monte Carlo sampling algorithms. #
################################################################

import numpy as np
import random
import copy
import matplotlib.pyplot as plt
import logging
from BaseModel import BaseModel
from MLPoints import *

def reflectAt(r: float, p: float):
    """Reflects given point p on reflection point r"""
    if (not (isinstance(r, (float, int)) and isinstance(p, (float, int)))):
        raise ValueError("Given values to reflectAt should be floats or ints.")
    return 2*r - p


def generateNewPerturbedSample(sample, scale):
    """
    Computes a Markov transition based on a Gaussian perturbation.
    If the new point goes out bounds (bounds are [-1, 1]),
    then it is brought back via reflection calling reflectAt.
    
    sample: Original point. Should be iterable on its dimensions.
    scale: Scale for the normal perturbation.
    """

    #Check that sample is iterable
    try:
        iter(sample)
    except Exception as e:
        print(getattr(e), "message", repr(e))

    #Check that scale is int or float.
    if (not isinstance(scale, (float, int))):
        raise ValueError("Given scale to generateNewPerturbedSample should be int or float.")

    #Placeholder for new sample
    newSample = [];

    for s in sample:
        #Check that values in sample are ints or floats
        if (not isinstance(s, (float, int))):
            raise ValueError("Given coordinates in sample given to generateNewPerturbedSample should be ints or floats.")

        #Perturbation on current dimension
        res = np.random.normal(loc=s, scale=scale);

        #While out of bounds, reflect appropriately.
        while (res > 1. or res < -1.):
            if (res > 1.):
                res = reflectAt(1, res)
            if (res < -1.):
                res = reflectAt(-1, res)
        #Save perturbation
        newSample.append(res);

    return newSample;


class MCSampler:
    """General base class for Monte Carlo samplers"""
    
    def __init__(self, model: BaseModel):
        """Initializer. Only recieves an instance of BaseModel to compute the QoI."""

        #Check that given model inherits from BaseModel
        if (not isinstance(model, BaseModel)):
            raise ValueError("Given model should inherit from BaseModel")
        
        self.model = model
        self.Dim = self.model.getParamDim();

class MonteCarlo(MCSampler):
    """Simple Monte Carlo sampler."""
    
    def getExpectation(self, cutoff, N, level):
        """
        Compute the expectation that the QoI is less than the cutoff.
        cutoff: value for which we compute Pr(QoI < cutoff).
        N: Number of samples to compute.
        level: Discretization level of the BaseModel that should be used.

        Returns dictionary with two keys:
        "P": Desired probability.
        "C": Required cost.
        """
        
        #Variables to save result and cost of computation.
        result = 0.0;
        cost = 0.0
        
        for _ in range(N):
            p = [np.random.uniform(-1.,1.) for __ in range(self.Dim)]
            solution = self.model.solveParam(p, level)
            
            try:
                cost += solution["Cost"]
            except KeyError:
                logging.error("Missing required key 'Cost' from solution to model.solveParam() when computing expectation.")
            try:
                result += int(solution["QoI"]<cutoff)
            except KeyError:
                logging.error("Missing required key 'QoI' from solution to model.solveParam() when computing expectation.")
        return {"P" : result/N, "C" : cost}

class MonteCarloAd(MonteCarlo):
    """Monte Carlo sampler with adaptive approximation of probability functional."""
    
    def getExpectation(self, cutoff, N, level):
        """
        Compute the expectation that the QoI is less than the cutoff.
        cutoff: value for which we compute Pr(QoI < cutoff).
        N: Number of samples to compute.
        level: Maximum discretization level of the BaseModel that should be used.

        Returns dictionary with two keys:
        "P": Desired probability.
        "C": Required cost.
        """

        #Variables to save result and cost of computation.
        result = 0.0;
        cost = 0.0
        
        for _ in range(N):
            p = [np.random.uniform(-1.,1.) for __ in range(self.Dim)]
            solution = self.model.solveParamAd(p, cutoff, level)
            try:
                cost += solution["Cost"]
            except KeyError:
                logging.error("Missing required key 'Cost' from solution to model.solveParam() when computing expectation.")
            try:
                result += int(solution["QoI"]<cutoff)
            except KeyError:
                logging.error("Missing required key 'QoI' from solution to model.solveParam() when computing expectation.")
        return {"P" : result/N, "C" : cost}


class MonteCarloML(MonteCarlo):
    """Multi level Monte Carlo sampler."""

    def getExpectation(self, cutoff, level, mult=1):
        """
        Compute the expectation that the QoI is less than the cutoff.
        cutoff: value for which we compute Pr(QoI < cutoff).
        level: Maximum discretization level of the BaseModel that should be used in the ML estimator.
        mult: factor to increase samples (optional).
        
        Returns dictionary with two keys:
        "P": Desired probability.
        "C": Required cost.
        """

        #Variables to save result and cost of computation.
        cost = 0.0
        result = 0.0

        #Samples per level.
        Samples = mlmcSamples(self.model.getConvergenceRate(), self.model.getWorkRate(), 1./self.model.getBase(), level)*mult
        
        for l in range(len(Samples)):
            N = Samples[l]
            levelResult = 0.0
            for _ in range(N):
                p = [np.random.uniform(-1.,1.) for __ in range(self.Dim)]

                #Solution at level l and l-1.
                res_l_1 = self.model.solveParam(p, l-1)
                res_l = self.model.solveParam(p,l)

                #Add cost of both solutions.
                cost += res_l["Cost"] + res_l_1["Cost"]

                #Check where solutions fall.
                yl_1 = int(res_l_1["QoI"]<cutoff and l>0)
                yl = int(res_l["QoI"]<cutoff)

                #Add result at current sample.
                levelResult += yl-yl_1
                
            #Add results at current level.
            result += levelResult/N
            
        return {"P" : result, "C" : cost}


class MonteCarloMLAd(MonteCarlo):
    """Multi level Monte Carlo sampler with adaptive solver."""
    
    def getExpectation(self, cutoff, level, mult=1):
        """
        Compute the expectation that the QoI is less than the cutoff.
        cutoff: value for which we compute Pr(QoI < cutoff).
        level: Maximum discretization level of the BaseModel that should be used in the ML estimator.
        mult: factor to increase samples (optional).
        
        Returns dictionary with two keys:
        "P": Desired probability.
        "C": Required cost.
        """
        
        #Variables to save result and cost of computation.
        cost = 0.0
        result = 0.0

        #Samples per level.
        Samples = mlmcAdSamples(self.model.getConvergenceRate(), self.model.getWorkRate(), 1./self.model.getBase(), level)*mult

        for l in range(len(Samples)):
            N = Samples[l]
            levelResult = 0.0
            for _ in range(N):
                p = [np.random.uniform(-1.,1.) for __ in range(self.Dim)]

                #Solution at level l-1 and cost.
                res_l_1 = self.model.solveParamAd(p, cutoff, l-1)
                cost += res_l_1["Cost"]

                #If previous solution was solved exactly, then
                #there is no need to solve the next level.
                if (res_l_1["Exact"]):
                    continue

                #Solution at level l and cost.
                res_l = self.model.solveParam(p,l)
                cost += res_l["Cost"]

                #Check where solutions fall.
                yl_1 = int(res_l_1["QoI"]<cutoff and l>0)
                yl = int(res_l["QoI"]<cutoff)

                #Add result at current sample.
                levelResult += yl-yl_1

            #Add result at current level.
            result += levelResult/N

        return {"P" : result, "C" : cost}


    
class MonteCarloIPS(MonteCarlo):
    """Multi level Monte Carlo sampler with interacting particle system"""
    
    def getExpectation(self, cutoff, level, mult=1):
        """
        Compute the expectation that the QoI is less than the cutoff.
        cutoff: value for which we compute Pr(QoI < cutoff).
        level: Maximum discretization level of the BaseModel that should be used in the ML estimator.
        mult: factor to increase samples (optional).
        
        Returns dictionary with two keys:
        "P": Desired probability.
        "C": Required cost.
        """

        #Variables to save result and cost of computation.
        cost = 0.0
        result = 0.0

        #Samples per level.
        Samples = mlmkSamples(self.model.getConvergenceRate(), self.model.getWorkRate(), 1./self.model.getBase(), level)*mult

        #Numerical method's convergence rate and initial size for Markov transition
        q = self.model.getConvergenceRate()
        mk = 1.0
        
        #Samples for the first level. Computed beforehand
        #and saved in a dictionary to keep additional information.
        #'Point': evaluation point.
        #'QoI': QoI computed on this point with level l-1
        #'Diff': abs(Qoi-cutoff)
        #'Weight': Weight of current point in computation of expectation.
        # Weight is Fixed to 1 since this implementation considers indicator
        # functions for the FK-Measures.
        samplePoints = np.array([{"Point" : [np.random.uniform(-1., 1.) for _ in range(self.Dim)], "QoI" : 0.0, "Diff" : 0.0, "Weight" : 1.0} for _ in range(Samples[0])])

        #Keep track of conditional probabilities (FK normalization in general)
        prob = 1.0
        
        for l in range(len(Samples)):
            #Limit for definition of sampling sets
            limit = self.model.getLimit(l)

            #List to keep all points which will be used as seeds for
            #the generation of samples on the next level.
            seeds = []

            #List to keep information of all point evaluaions on the current level.
            cPoints = []

            #Variable to compute the contribution of the current level.
            levelResult = 0.0

            #Variable for computation of conditional probability
            condProb = 0.0

            #List to save weights for choice of seeds in measure evolution.
            Ws = []

            #Iterate on points
            for p in samplePoints:
                #Solve on current level. Solution on l-1 is saved on points.
                #Also, add the cost.
                res_l = self.model.solveParamBase(p["Point"],l)
                cost += res_l["Cost"]

                #Check where solutions fall.
                #Notice that the solution to l-1 is read from the point.
                yl_1 = int(p["QoI"] < cutoff and l > 0)
                yl = int(res_l["QoI"] < cutoff)

                #Compute distance to cutoff.
                diff = np.abs(res_l["QoI"]-cutoff)

                #Add result at current sample
                levelResult += yl-yl_1

                #Save point.
                cPoints.append({"Point": p["Point"], "QoI": res_l["QoI"], "Diff" : diff, "Weight" : p["Weight"]})

                #If distance to cutoff is small enough, then save the point as a seed,
                #save weight (1.0) and add contribution to conditional probability.
                if (diff<limit):
                    seeds.append({"Point": p["Point"], "QoI": res_l["QoI"], "Diff" : diff, "Weight" : p["Weight"]})
                    Ws.append(1.0)
                    condProb += 1.0

            #Compute conditional probability and add up this level's contribution.
            condProb /= len(samplePoints)
            levelResult /= len(samplePoints)
            
            result += prob*levelResult

            if (l == len(Samples) - 1):
                break


            #Update FK normalization constant
            prob *= condProb

            #If prob==0.0, then no points fell on the next set and we have no seeds
            #to continue the IPS. Stop the simulation and return (early exit).
            if (prob==0.0):
                break

            #Update the sample points by choosing randomly from the seeds with
            #corresponding weights (1.0 in this case).
            samplePoints = random.choices(seeds, weights=Ws,k=Samples[l+1])

            #Since there may be repetiton, perform a deepcopy of each point
            for i in range(len(samplePoints)):
                samplePoints[i]=copy.deepcopy(samplePoints[i])

            #Compute Markov transition on each point. This loop controls how many
            #evaluations of the transition we compute per point. More evaluations
            #yields higher independence and smaller error, but higher cost.
            for j in range(1):
                #Keep track of how many points are accepted
                accepted = 0.0
                for i in range(len(samplePoints)):
                    #Compute perturbation
                    p = generateNewPerturbedSample(samplePoints[i]["Point"], mk/(2**(q*l)))

                    #Compute QoI at point, add up cost and check distance to cutoff
                    res_l = self.model.solveParam(p, l)
                    cost += res_l["Cost"]
                    diff = np.abs(res_l["QoI"]-cutoff)

                    #If distance is still under limit, accept point
                    if (diff<limit):
                        samplePoints[i]["Point"] = p
                        samplePoints[i]["QoI"]=res_l["QoI"]
                        samplePoints[i]["Diff"]=diff
                        accepted += 1
                        
                accepted /= len(samplePoints)
                #if accepted points fall below a certain threshold, decrease size.
                if (accepted < 0.3):
                    mk /= 2.
                #if accepted points fall above a certain threshold, increase size.
                if (accepted > 0.9):
                    mk *= 2.
                
        return {"P" : result, "C" : cost}


def expWeight(value, bound):
    """
    Exponential weight for IPS.
    For this to work, the probability that value < bound
    should be small.
    """
    return np.exp(-value/bound)

class MonteCarloIPSW(MonteCarlo):
    """
    Multi level Monte Carlo sampler with interacting particle system.
    This version uses a general exponential weight instead of just indicators.
    Because of this, it  does not need that the samples have any property, every sample
    is a possible seed and the chance that they are used is given by the exponential weight.
    """

    def getExpectation(self, cutoff, level, mult=1, desiredCost=0.):
        """
        Compute the expectation that the QoI is less than the cutoff.
        cutoff: value for which we compute Pr(QoI < cutoff).
        level: Maximum discretization level of the BaseModel that should be used in the ML estimator.
        mult: factor to increase samples (optional).
        desiredCost: if non-zero, number of samples is chosen so that the computation has a cost close to the desired cost.
        
        Returns dictionary with two keys:
        "P": Desired probability.
        "C": Required cost.
        """
        #Variables to save result and cost of computation.
        cost = 0.0
        result = 0.0
        

        #Samples per level.
        #If desiredCost>0, then choose samples so that total cost is close to desired cost.
        Samples = None
        if (desiredCost>0.):
            Samples = mlmkSamples(self.model.getConvergenceRate(), self.model.getWorkRate(), 1./self.model.getBase(), level, costT)
        else:
            Samples = mlmkSamples(self.model.getConvergenceRate(), self.model.getWorkRate(), 1./self.model.getBase(), level)*mult
            

        #Numerical method's convergence rate and initial size for Markov transition
        q = self.model.getConvergenceRate()
        mk = 1.0
            
        #Samples for the first level. Computed beforehand
        #and saved in a dictionary to keep additional information.
        #'Point': evaluation point.
        #'QoI': QoI computed on this point with level l-1
        #'Diff': abs(Qoi-cutoff)
        #'Weight': Weight of current point in computation of expectation.
        # Weight is chosen according to an exponential.
        samplePoints = np.array([{"Point" : [np.random.uniform(-1., 1.) for _ in range(self.Dim)], "QoI" : 0.0, "Diff" : 0.0, "Weight" : 1.0} for _ in range(Samples[0])])
        
        #FK normalization
        prob = 1.0
        
        for l in range(len(Samples)):
            #Limit=bound for exponential weight.
            limit = self.model.getLimit(l)

            #List to keep information of all point evaluaions on the current level.
            #In this variants, all points are seeds.
            cPoints = []

            #Variable to compute the contribution of the current level.
            levelResult = 0.0

            #Auxiliar variable to compute FK weight
            condProb = 0.0

            #List to save weights for choice of seeds in measure evolution
            Wc = []

            #Iterate on points
            for p in samplePoints:
                #Solve on current level. Solution on l-1 is saved on points.
                #Also, add the cost.
                res_l = self.model.solveParam(p["Point"],l)
                cost += res_l["Cost"]

                #Check where solutions fall
                #Notice that the solution to l-1 is read from the point.
                yl_1 = int(p["QoI"] < cutoff and l > 0)
                yl = int(res_l["QoI"] < cutoff)

                #Compute distance to cutoff.
                diff = np.abs(res_l["QoI"]-cutoff)

                #Add result to current sample and current contribution to FK normalization
                levelResult += (yl-yl_1)/p["Weight"]
                condProb += expWeight(diff, limit)

                #Save weight and point to sample points for the next level
                Wc.append(expWeight(diff, limit));
                cPoints.append({"Point": p["Point"], "QoI": res_l["QoI"], "Diff" : diff, "Weight" : p["Weight"]})

            #Compute conditional probability and add up this level's contribution.
            condProb /= len(samplePoints)
            levelResult /= len(samplePoints)
            
            result += prob*levelResult

            #If we are on the final level, break.
            if (l == len(Samples) - 1):
                break;

            #Update FK normalization
            prob *= condProb

            #Update the sample points by choosing randomly from the seeds with
            #corresponding weights (1.0 in this case).
            samplePoints = random.choices(cPoints, weights=Wc, k=Samples[l+1])
            
            #Since there may be repetiton, perform a deepcopy of each point
            for i in range(len(samplePoints)):
                samplePoints[i]=copy.deepcopy(samplePoints[i])

            #Compute Markov transition on each point. This loop controls how many
            #evaluations of the transition we compute per point. More evaluations
            #yields higher independence and smaller error, but higher cost.
            for j in range(1):
                #Keep track of how many points are accepted
                accepted = 0.0
                for i in range(len(samplePoints)):
                    #Compute perturbation
                    p = generateNewPerturbedSample(samplePoints[i]["Point"], mk/2**(q*l))

                    #Compute QoI at point, add up cost and check distance to cutoff.
                    res_l = self.model.solveParam(p, l)
                    cost += res_l["Cost"]
                    diff = np.abs(res_l["QoI"]-cutoff)

                    #Accept point with probability G_l (weight)
                    u = np.random.uniform(0,1)
                    if (u < expWeight(diff, limit)):
                        samplePoints[i]["Point"]=p
                        samplePoints[i]["QoI"]=res_l["QoI"]
                        samplePoints[i]["Diff"]=diff
                    samplePoints[i]["Weight"]*=expWeight(samplePoints[i]["Diff"], limit)

                accepted /= len(samplePoints)

                #if accepted points fall below a certain threshold, decrease size.
                if (accepted < 0.3):
                    mk /= 2.
                #if accepted points fall above a certain threshold, increase size.
                if (accepted > 0.9):
                    mk *= 2.

        return {"P" : result, "C" : cost}
