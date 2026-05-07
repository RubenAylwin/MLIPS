from MonteCarlo import MonteCarlo, MonteCarloIPS, MonteCarloIPSW, MonteCarloMLAd, MonteCarloML
from Example import Example
import numpy as np
import matplotlib.pyplot as plt
import argparse
pC = 0
LS=["-", (0, (2, 2)), (0, (7, 2)), (0, (6, 3, 3, 3)), (0, (6, 3, 3, 3, 3, 3))]


def runSim(MCSampler, level, cutoff, realizations):
    global pC
    Error = []
    Work = []
    for l in range(level):
        error = 0.0
        work = 0.0
        for _ in range(realizations):
            result = MCSampler.getExpectation(cutoff, l)
            error += (result['P']/(np.pi*cutoff)-1.)**2.0/realizations
            work += result["C"]/realizations
        error = np.sqrt(error)
        Error.append(error)
        Work.append(work)
    p=np.polyfit(np.log(Work[2:]), np.log(Error[2:]), 1)
    plt.loglog(Work, Error, marker = 'o', lw = 2, markersize = 8, label = MC.name)
    plt.loglog(Work, 1.2*np.exp(p[1])*Work**p[0], marker = '', lw = 1.5, color='k', label="Rate "+'%.2f' % p[0], ls = LS[pC])
    pC += 1
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='runExperiment',
                                     description='Run an experiment for convergence of required MC methods with specified parameters.')
    parser.add_argument('--ips', action='store_true', help = 'flag to turn on MLIPS')
    parser.add_argument('--ipsw', action='store_true', help = 'flag to turn on MLIPS with exponential weights.')
    parser.add_argument('--mc', action='store_true', help = 'flag to turn on MC')
    parser.add_argument('--mlmc', action='store_true', help = 'flag to turn on MLMC')
    parser.add_argument('--mlad', action='store_true', help = 'flag to turn on adaptive MLMC')
    parser.add_argument('--realizations', type = int, help = 'flag to turn on adaptive MLMC')
    parser.add_argument('-L', '--level', type = int, required = True, help = 'Max level')
    parser.add_argument('-Y', '--cutoff', type = float, required = True, help = 'Cutoff for probability (QoI < cutoff)')
    parser.add_argument('-E', '--error', type = float, required = True, help = 'Error size at level 0.')
    parser.add_argument('-r', '--work_rate', type = float, required = True, help = 'Rate to which work increases.')
    parser.add_argument('-q', '--error_rate', type = float, required = True, help = 'Rate to which error decreases.')
    parser.add_argument('-g', '--gamma', type = float, required = True, help = 'Scaling factor for error and work.')

    args = vars(parser.parse_args())

    L = args['level']
    y = args['cutoff']
    E = args['error']
    r = args['work_rate']
    q = args['error_rate']
    g = args['gamma']
    mc = args['mc']
    ips = args['ips']
    ipsw = args['ipsw']
    mlmc = args['mlmc']
    mlad = args['mlad']
    R = args['realizations']
    
    inst = Example(L, 1./g, E, q, r)

    if (mc):
        MC = MonteCarlo(inst)
        runSim(MC,L-1,y,R)

    if (mlmc):
        MC = MonteCarloML(inst)
        runSim(MC,L,y,R)

    if (mlad):
        MC = MonteCarloMLAd(inst)
        runSim(MC,L,y,R)
        
    if (ips):
        MC = MonteCarloIPS(inst)
        runSim(MC,L,y,R)

    if (ipsw):
        MC = MonteCarloIPSW(inst)
        runSim(MC,L,y,R)

    plt.legend()
    plt.show()
