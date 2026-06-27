from MonteCarlo import MonteCarlo, MonteCarloIPS, MonteCarloIPSW, MonteCarloMLAd, MonteCarloML
from Example import ExampleDim
import numpy as np
from scipy.special import gamma as gammaFun
import matplotlib.pyplot as plt
import argparse
pC = 0
modelCounter = 0
LS=["-", (0, (3, 3)), (0, (7, 2)), (0, (6, 3, 3, 3)), (0, (6, 3, 3, 3, 3, 3))]

def rateComp(X,Y):
    p=np.polyfit(X, Y, 1)
    rates = (Y[1:] - Y[:-1])/(X[1:] - X[:-1])
    # p1 = np.percentile(rates, 75)
    # p2 = np.percentile(rates, 25)
    # d = p1-p2
    # q1 = np.average(rates)+1.5*d
    # q2 = np.average(rates)-1.5*d
    # rates = rates[(rates < p1) & (rates > p2)]
    print(rates)
    return np.average(rates), p[1]

def runSim(MCSampler, level, cutoff, realizations, ok, mult = 1):
    global pC
    global modelCounter
    modelCounter+=1
    Error = []
    Work = []
    print("=============================================")
    print("Working on "+MC.name)
    for l in range(level):
        error = 0.0
        work = 0.0
        for r in range(realizations):
            print(">    Working on level "+str(l)+" - progress: "+str(r)+"/"+str(realizations),end='\r')
            result = MCSampler.getExpectation(cutoff, l, mult)
            error += (result['P']/(ok)-1.)**2.0/realizations
            work += result["C"]/realizations
            #print("",end='')
        error = np.sqrt(error)
        Error.append(error)
        Work.append(work)
        print(100*' ', end='\r')
        print(">    Done with level "+str(l))
    print("=============================================")
    p=rateComp(np.log(Work), np.log(Error))
    #p=np.polyfit(np.log(Work[-5:-1]), np.log(Error[-5:-1]), 1)
    plt.loglog(Work, Error, marker = 'o', lw = 2, markersize = 8, label = MC.name)
    plt.loglog(Work, Error[-1]*(np.array(Work)/Work[-1])**p[0], marker = '', lw = 1.5, color='k', label="Rate "+'%.2f' % p[0], ls = LS[pC])
    pC += 1
    
if __name__=='__main__':
    dim = 2
    parser = argparse.ArgumentParser(prog='runExperiment',
                                     description='Run an experiment for convergence of required MC methods with specified parameters.')
    parser.add_argument('--ips', action='store_true', help = 'flag to turn on MLIPS')
    parser.add_argument('--ipsw', action='store_true', help = 'flag to turn on MLIPS with exponential weights.')
    parser.add_argument('--mc', action='store_true', help = 'flag to turn on MC')
    parser.add_argument('--mlmc', action='store_true', help = 'flag to turn on MLMC')
    parser.add_argument('--mlad', action='store_true', help = 'flag to turn on adaptive MLMC')
    parser.add_argument('--realizations', type = int, required = True, help = 'flag to turn on adaptive MLMC')
    parser.add_argument('-f', '--file_name', type = str, help = 'name to save figure')
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
    fn = args['file_name']
    inst = ExampleDim(L, 1./g, E, q, r, dim)

    spaceSize = 2.**dim
    sphereSize = np.pi**(dim/2.)*(4.*y)**(dim/2.)/gammaFun(dim/2.0+1.)
    ok = sphereSize/spaceSize
    print(ok)

    if (mc):
        MC = MonteCarlo(inst)
        runSim(MC,int((L+1.)/2.),y,R, ok)

    if (mlmc):
        MC = MonteCarloML(inst)
        runSim(MC,L,y,R, ok)

    if (mlad):
        MC = MonteCarloMLAd(inst)
        runSim(MC,L,y,R, ok)
        
    if (ips):
        MC = MonteCarloIPS(inst)
        runSim(MC,L-1,y,R, ok)
        MC.plotSamples(np.sqrt(4*y))
    if (ipsw):
        MC = MonteCarloIPSW(inst)
        runSim(MC,L-1,y,R, ok)
        
    plt.xlabel("Work", fontsize=15)
    plt.ylabel("Relative Error", fontsize=15)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend(fontsize=11, ncol=modelCounter, loc='upper right')
    plt.grid()
    plt.gcf().set_size_inches(7, 5)
    if (fn is not None):
        plt.savefig(fn+".pdf", format='pdf')
    else:
        plt.show()
