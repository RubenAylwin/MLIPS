##########################################################################################
# Base class for numerical methods for the approximation of probabilities involving QoIs #
##########################################################################################

import numpy as np

class BaseModel:
    def __init__(self, L, base):
        self.L = L
        self.base = base
        self.Levels = L+1
        self.samples = [0 for i in range(self.Levels)]

    def getBase(self):
        return self.base
    
    def setErrorConstant(self, Cg):
        self.Cg = Cg

    def getErrorConstant(self):
        return self.Cg
        
    def setConvergenceRate(self, q):
        self.q = q

    def getConvergenceRate(self):
        return self.q

    def setWorkRate(self, r):
        self.r = r

    def getWorkRate(self):
        return self.r

    def setParamDim(self, dim):
        self.paramDim = dim

    def getParamDim(self):
        return self.paramDim
    
    def getLimit(self, level):
        gamma=1./self.base**(self.q)
        return self.Cg*gamma**(level)*(1.+gamma)/(1.-gamma)
        
    def costLevel(self, level):
        if (level == -1):
            return 0.

        return self.base**(self.r*(level))
    
    def costSamples(self, samples):
        work = 0.;

        for l in range(len(samples)):
            work += samples[l]*self.costLevel(l)

        return work

    def costSamplesML(self, samples):
        return self.costSamples(samples)+self.costSamples(samples[1:])

    def getNumLevels(self):
        return self.Levels

    def report(self):
        print(self.samples)
    
    def solveParamBase(self, param, level):
        solution = self.solveParam(param, level)
        return solution
    
    def solveParamAd(self, param, cutoff, level):
        qoi = 0.0
        cost = 0.0
        test = 0.0
        if (level == -1):
            return {"QoI" : 0.0, "Diff" : 0.0, "Cost" : 0.0, "Exact" : False}

        for l in range(level+1):
            res = self.solveParamBase(param, l)
            qoi = res["QoI"]
            cost += res["Cost"]
            test = np.abs(qoi-cutoff)

            if (test>self.Cg*(1./self.base)**(self.q*l)):
                return {"QoI" : qoi, "Diff" : test, "Cost" : cost, "Exact" : True}

        return {"QoI" : qoi, "Diff" : test, "Cost" : cost, "Exact" : False}
    
if __name__=="__main__":
    base = BaseModel(10, 2)
    base.setConvergenceRate(2)
    base.setWorkRate(1)
    print(base.costSamples(base.mlmkSamples("W",1000000)))
