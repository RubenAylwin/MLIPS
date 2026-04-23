import numpy as np
from BaseModel import BaseModel

class Example(BaseModel):
    def __init__(self, L, base, error):
        super().__init__(L, base)
        self.setParamDim(2)
        self.setErrorSize(error)
        
    def setErrorSize(self, E):
        self.E = E
        self.setErrorConstant(E)
    
    def solveParam(self, param, level):
        gamma = 1./self.base
        
        if (level == -1):
            return {"QoI" : 0.0, "Cost" : 0.0}
        
        qoi = (0.5*param[0])**2.+(0.5*param[1])**2.+self.E*gamma**(self.q*level)*0.5*(np.sin(param[0]/(level+1))-np.cos(param[1]/(level+1)))
        cost = self.costLevel(level)
        return {"QoI" : qoi, "Cost" : cost}
    
if __name__=="__main__":
    print("hello")
    test = Example(10, 6, 0.2)
    test.setConvergenceRate(2)
    test.setWorkRate(3)
    
    
