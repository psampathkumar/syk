### NOTE: Read the Log too. Current progress and other issues are adderssed there 
### NOTE: The code is much faster with all pssible combinations instead fo all possible permutations. 
###        Feel free to download and play around for various values
# The SYK Model
The SYK model is given by the Hamiltonian
![](https://latex.codecogs.com/gif.latex?H%20%3D%20%5Csum%5Climit_%7Bi_1%2Ci_2%2C%20...%20i_q%7D%20J_%7Bi_1%2Ci_2%2Ci_3%20....%20i_q%7D%20%5Cpsi_%7Bi_1%7D%5Cpsi_%7Bi_2%7D%5Cpsi_%7Bi_3%7D...%5Cpsi_%7Bi_q%7D)

where the J's are Random numbers picked from a gaussian distribution, with mean = 0 and std_dev = J
For all the below distributions J = 1
# Single Free SYK for N=16 , q = 2
![](./Single_SYK_q2.png)
# Single Free SYK for N=16 , q = 4
![](./Single_SYK_q4.png)
# Single Free SYK for N=14 , q = 6
![](./Single_SYK_q6.png)
# Single Free SYK for N=12 , q = 8
q = 8 is pretty weird, but this is a result of using low, N. 
It had similar structure for q=4 too for N=12. 
![](./Single_SYK_q8.png)

# Coupled SYK N=8  
![](./Coupled_SYK_q4.png)

