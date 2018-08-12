#!/usr/bin/env python

import numpy as np
#from tqdm import tqdm
import scipy.linalg as LA
import random
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.cm as cm
import pickle
import h5py
import argparse
H=[]

def herm(ww):
  if(np.allclose(ww, np.conj(ww).T)):
    return "Hermitian"
  elif(np.allclose(ww, -1* np.conj(ww).T)):
    return "Anti Hermitian"
  else:
    return "Not hermitian"
      
parser = argparse.ArgumentParser()
parser.add_argument("-N","--number",help="Number of Particles in Each SYK",type=int)
parser.add_argument("-g","--coupling",help="Coupling COnstant",type=float)
args = parser.parse_args()

J = 1
N = args.number
g = args.coupling

try:
  with h5py.File('hamiltonian_coup_'+str(g),'r') as fp:
    H = fp['data'][:]
  #with open ('hamiltonian_coupled_22', 'rb') as fp:
    #H = pickle.load(fp)
except FileNotFoundError:
  print("File Not Found. Check the Name")
  exit()
print("Hamiltonian Read")
print(herm(H))
'''
gamma = create_gamma()
kk = 0
for H in gamma:
    per,mat = check_sparcity(H)
    print(per)
    plt.title(str(kk))
    kk = kk + 1
    plt.imshow(np.array(mat).reshape(2**int(N/2),2**int(N/2)))
    plt.show()

print(H.shape)
print("Starting Eigenvalue Computation")
eig = LA.eigvalsh(H)
print(eig)
plt.hist(eig, 20, normed=0, histtype='step',label ='Energy')
plt.show()
#plt.savefig("Test_Coupled_SYK_q4_N12",bbox='tight')
plt.close()

'''

def find_eigval(H):
    print("Importing Stuff")
    import sys, slepc4py
    from petsc4py import PETSc
    from slepc4py import SLEPc
    import numpy
    A = PETSc.Mat().create()
    print(H.shape)
    A.setSizes(H.shape)
    A.setFromOptions()
    A.setUp()
    A[:,:] = np.array(H,dtype=np.complex64)[:,:]
    A.assemble()
    E = SLEPc.EPS()
    E.create()
    E.setOperators(A)
    E.setProblemType(SLEPc.EPS.ProblemType.HEP)
    E.setDimensions(nev = H.shape[0])
    E.setTolerances(1e-8,1000)
    E.setFromOptions()
    E.solve()
    Print = PETSc.Sys.Print
    Print()
    Print("******************************")
    Print("*** SLEPc Solution Results ***")
    Print("******************************")
    Print()
    
    its = E.getIterationNumber()
    Print("Number of iterations of the method: %d" % its)
    
    eps_type = E.getType()
    Print("Solution method: %s" % eps_type)
    
    nev, ncv, mpd = E.getDimensions()
    Print("Number of requested eigenvalues: %d" % nev)
    Print(" the maximum dimension of the subspace to be used by the solver: %d " % ncv)
    Print(" the maximum dimension allowed for the projected problem: %d" % mpd)
    
    #tol, maxit = E.getTolerances()
    #Print("Stopping condition: tol=%.4g, maxit=%d" % (tol, maxit))
    nconv =  E.getConverged()
    ans = []
    for i in range(nconv):
        ans.append(E.getEigenvalue(i))
    return ans
    
print("Finding Eigenvalues")
#eig = LA.eigvalsh(H)
#print(eig)
eig = find_eigval(H)
print(eig)
plt.hist(eig, 20, normed=0, histtype='step',label ='Energy')
plt.savefig("SYK_Coupled"+str(N)+"_"+str(g)+"_histo",bbox='tight')
plt.close()
plt.hlines(eig,0,5)
plt.savefig("SYK_Coupled"+str(N)+"_"+str(g)+"_lines",bbox='tight')
plt.close()
