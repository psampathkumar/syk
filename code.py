#! /usr/bin/env python
import numpy as np
from tqdm import tqdm
import scipy.linalg as LA
import random
import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm

kkk=cm.gist_stern # Put the Plotting Style here
print("MAKE SURE YOU CHANGE THE FILE NAME")
input("Press enter to continue")
def herm(ww):
    if(np.allclose(ww, np.conj(ww).T)):
        return "Hermitian"
    elif(np.allclose(ww, -1* np.conj(ww).T)):
        return "Anti Hermitian"
    else:
        return "Not hermitian"

def check_sparcity(a):
    k = np.hstack(a)
    mat = np.zeros(2**N)
    for i in range(len(k)):
        if abs(k[i])>1e-5:
            mat[i] = 1
    nonzero = sum(mat)
    print(len(mat))
    return nonzero/len(k),mat


J = 1
N = 8
print(2**N,2**int(N/2))

def create_gamma():
    sig1 = np.array([[0,1],[1,0]])
    sig2 = np.array([[0 , -1j],[1j , 0]])
    sig3 = np.array([[-1 , 0j ],[0j, 1]])
    gamma = []
    gamma.append(sig1)
    gamma.append(sig2)
    for i in range(2,N-1,2):
        for l in range(i):
            gamma[l] = np.kron(gamma[l],sig3)
        iden = np.identity(2**int(i/2))
        gamma.append(np.kron(iden,sig1))
        gamma.append(np.kron(iden,sig2))
        print(" D : ",i+2," dim :", 2**int(i/2+ 1),"seems to work",gamma[0].shape)
    return gamma

def create_free_H(gamma,q=4,rand=True,g=1):
    print("Created Gamma matrices")
    H = np.zeros([2**int(N/2),2**int(N/2)])
    length =  sum(1 for _ in itertools.permutations(gamma,q))
    for i in tqdm(itertools.combinations(gamma,q),total=length,desc=str(q)+":Body Term"):
        ans = np.identity(2**int(N/2))
        if not (len(i) == q):
            print("ERROR")
            exit(0)
        for k in i:
            ans = np.matmul(ans,k)
        if(rand):
            ans = random.gauss(0,J)*ans
        else:
            ans = g*ans #Multiply by the factor of g here.!
        
        H = np.add(H,ans)
    return H

def create_H(couple=False):
    coup = 4 #Coupling term
    gamma = create_gamma()
    free_H1 = np.kron(np.array(create_free_H(gamma)),np.identity(2**int(N/2)))
    free_H2 = np.kron(np.identity(2**int(N/2)),np.array(create_free_H(gamma)))
    coup = np.zeros([2**int(N),2**int(N)])
    for k in gamma:
        coup = np.add(coup,np.kron(k,k))
    H = np.add(free_H1,free_H2)
    H = np.add(coup,H)
    return H


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
    A[:,:] = H[:,:]
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
    
    tol, maxit = E.getTolerances()
    Print("Stopping condition: tol=%.4g, maxit=%d" % (tol, maxit))
    nconv =  E.getConverged()
    ans = []
    for i in range(nconv):
        ans.append(E.getEigenvalue(i))
    return ans
    



H = create_H()
print("Hamiltonian Created")
print(herm(H))
#per,mat = check_sparcity(H)
#print(per)
#plt.imshow(np.array(mat).reshape(2**int(N/2),2**int(N/2)))
#plt.show()
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
print("Finding Eigenvalues")
eig = LA.eigvalsh(H)
print(eig)
eig = find_eigval(H)
print(eig)
'''
plt.hist(eig, 20, normed=0, histtype='step',label ='Energy')
plt.show()
#plt.savefig("Test_Coupled_SYK_q4_N12",bbox='tight')
plt.close()
'''
