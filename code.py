#! /usr/bin/env python
import numpy as np
import scipy.linalg as LA
import random
import itertools
import pickle
import h5py
import argparse
#print("MAKE SURE YOU CHANGE THE FILE NAME")
#input("Press enter to continue")

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

parser = argparse.ArgumentParser()
parser.add_argument("-N","--number",help="Number of Particles in Each SYK",type=int)
parser.add_argument("-g","--coupling",help="Coupling COnstant",type=float)
args = parser.parse_args()

J = 1
N = args.number
g = args.coupling
print("Number:",N)
print("Coupling:",g)
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

    #import tqdm as tqdm
    #for i in tqdm.tqdm(itertools.combinations(gamma,q)):

    for i in itertools.combinations(gamma,q):
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

def create_H(g,couple=False):
    coup = 4 #Coupling term
    gamma = create_gamma()
    print("Created Gamma matrices")
    free_H1 = np.kron(np.array(create_free_H(gamma)),np.identity(2**int(N/2)))
    free_H2 = np.kron(np.identity(2**int(N/2)),np.array(create_free_H(gamma)))
    coup = np.zeros([2**int(N),2**int(N)])
    for k in gamma:
        coup = np.add(coup,np.kron(k,k))
    H = np.add(free_H1,free_H2)
    H = np.add(g*coup,H)
    return H




print("Creating with coupling:",g)
H = create_H(g)
#H = create_free_H(create_gamma())
with h5py.File('hamiltonian_coup_'+str(g),'w') as fp:
  fp.create_dataset('data',data=H)
#with open('hamiltonian_coup_'+str(g),'wb') as fp:
  #pickle.dump(H,fp)
print("Hamiltonian Created")
print(herm(H))
