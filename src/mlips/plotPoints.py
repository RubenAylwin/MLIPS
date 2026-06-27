from MonteCarlo import MonteCarlo, MonteCarloIPS, MonteCarloIPSW, MonteCarloMLAd, MonteCarloML
from Example import ExampleDim
import numpy as np
from scipy.special import gamma as gammaFun
import matplotlib.pyplot as plt

inst = ExampleDim(5, 2., 0.001, 1, 3, 2)
y = 0.1
pointsIPS = np.zeros(5)
pointsAd = np.zeros(5)
cIPS = 0.
cAd = 0.
L = 10
for _ in range(L):
    MCA = MonteCarloMLAd(inst)
    cAd += MCA.getExpectation(y,4,3750)["C"]
    pointsAd+=MCA.plotSamples(np.sqrt(4*y), "SamplesAd")
    print("dAd")
    MC = MonteCarloIPS(inst)
    cIPS += MC.getExpectation(y,4,50*2)["C"]
    pointsIPS+=MC.plotSamples(np.sqrt(4*y), "SamplesIPS")
    print("dIPS")
print(cAd/L, cIPS/L)
for p in pointsAd:
    print(str(p/L)+" & ", end='')
print("----")
for p in pointsIPS:
    print(str(p/L)+" & ", end='')
print(pointsAd/L, pointsIPS/L)
