import numpy as np
from BaseModel import BaseModel

class Example(BaseModel):
    def __init__(self, L, base, error, q, r):
        super().__init__(L, base)
        self._BaseModel__setParamDim(2)
        self.__setErrorSize(error)
        self._BaseModel__setConvergenceRate(q)
        self._BaseModel__setWorkRate(r)
        
    def __setErrorSize(self, E):
        self.E = E
        self._BaseModel__setErrorConstant(E)
    
    def solveParam(self, param, level):
        gamma = 1./self.base
        
        if (level == -1):
            return {"QoI" : 0.0, "Cost" : 0.0}
        
        qoi = (0.5*param[0])**2.+(0.5*param[1])**2.+self.E*gamma**(self.q*level)*0.5*(np.sin(param[0]/(level+1))-np.cos(param[1]/(level+1)))
        cost = self.costLevel(level)
        return {"QoI" : qoi, "Cost" : cost}    
    
