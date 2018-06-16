#! /usr/bin/env python
import numpy as np
from tqdm import tqdm
import scipy.linalg as LA
import random
import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
kkk=cm.gist_stern # Put the Plotting Style here
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
N = 20
print(2**N,2**int(N/2))
q = 4
if(q>N):
    print("q should be less than N")
    exit(0)

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


def create_H():
    gamma = create_gamma()
    print("Created Gamma matrices")
    H = np.zeros([2**int(N/2),2**int(N/2)])
    length =  sum(1 for _ in itertools.permutations(gamma,q))
    for i in tqdm(itertools.permutations(gamma,q),total=length):
        ans = np.identity(2**int(N/2))
        if not (len(i) == q):
            print("ERROR")
            exit(0)
        for k in i:
            ans = np.matmul(ans,k)
        ans = random.gauss(0,J)*ans
        H = np.add(H,ans)
    return H

H = create_H()
per,mat = check_sparcity(H)
print(per)
plt.imshow(np.array(mat).reshape(2**int(N/2),2**int(N/2)))
plt.show()
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

'''
print(H.shape)
print("Starting Eigenvalue Computation")
eig = LA.eigvalsh(H)
print(eig)
plt.hist(eig, 20, normed=0, histtype='step',label ='Energy')
plt.show()
