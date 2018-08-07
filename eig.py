#!/usr/bin/env python

import numpy as np
#from tqdm import tqdm
import scipy.linalg as LA
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pickle
H=[]
try:
  with open ('hamiltonian_coupled_22', 'rb') as fp:
    H = pickle.load(fp)
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
print("Finding Eigenvalues")
eig = LA.eigvalsh(H)
print(eig)
#eig = find_eigval(H)
#print(eig)
plt.hist(eig, 20, normed=0, histtype='step',label ='Energy')
plt.savefig("Test_SYK_q4_N30",bbox='tight')
plt.close()
plt.hlines(eig,0,5)
plt.savefig("Test_SYK_q4_N30_lines",bbox='tight')
plt.close()
