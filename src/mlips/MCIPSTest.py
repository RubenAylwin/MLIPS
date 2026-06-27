from MonteCarlo import MonteCarloIPS, MonteCarloIPSW, MonteCarloMLAd
from Example import Example
import numpy as np
import matplotlib.pyplot as plt
q = 2
r = 3
y = 0.1
error = 0.1

inst = Example(10, 2, error, q, r)

MCI = MonteCarloIPSW(inst)
MC = MonteCarloMLAd(inst)
Lev = 0
NO = 2
S = 50
R=[]
W=[]

R1=[]
W1=[]
#MC.getExpectation(4,1)

Range = 5
ErrPerLev = [[] for _ in range(Range)]
fig = plt.figure()
ax = plt.gca()
for l in range(Range):
    res = 0.0
    cost = 0.0
    for s in range(S):
        E = MCI.getExpectation(y, l, 4)
        current = (E["P"]-np.pi*y)**2.0/((y*np.pi)**2.0)
        ErrPerLev[l].append(np.sqrt(current))
        res += current
        cost += E["C"]

    
    ax.scatter([cost/S for _ in range(S)],ErrPerLev[l])
    res = np.sqrt(res/S)
    R.append(res)
    W.append(cost/S)
ax.set_yscale("log")
ax.set_xscale("log")
ax.plot(W, R)
ax.plot(W, 2.5*R[1]*(np.array(W)/W[1])**(-.5))
plt.show()
    
for l in range(Range):
    res = 0.0
    cost = 0.0
    for s in range(S):
        E = MCI.getExpectation(y, l, 1)
        current = (E["P"]-np.pi*y)**2.0/(S*(y*np.pi)**2.0)
        res += current
        cost += E["C"]
    res = np.sqrt(res)/(y*np.pi)
    R1.append(res)
    W1.append(cost/S)


plt.plot(W, np.array(R), marker="s", color = "blue")
plt.loglog(W1, np.array(R1)*R[0]/R1[0], marker="o", color = "red")

# plt.loglog(W, R[0]*(np.array(W)/W[0])**(-.3))
# plt.loglog(W, R[0]*(np.array(W)/W[0])**(-.4))
plt.loglog(W, 2.5*R[1]*(np.array(W)/W[1])**(-.5))
plt.show()
