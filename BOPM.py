# Binomial Options Pricing
# By Padraic McAtee
#     
# My notation here is based on the original Cox, Ross and Rubinstein paper.
import numpy as np
import math as m

def OptionsVal(n, S, K, r, v, T, PC):
    dt = T/n                    
    u = m.exp(v*m.sqrt(dt)) 
    d = 1/u                     
    p = (m.exp(r*dt)-d)/(u-d)   
    Pm = np.zeros((n+1, n+1))   
    Cm = np.zeros((n+1, n+1))
    tmp = np.zeros((2,n+1))
    for j in range(n+1):
        tmp[0,j] = S*m.pow(d,j)
        tmp[1,j] = S*m.pow(u,j)
    tot = np.unique(tmp)
    c = n
    for i in range(c+1):
        for j in range(c+1):
            Pm[i,j-c-1] = tot[(n-i)+j]
        c=c-1
    for j in range(n+1, 0, -1):
        for i in range(j):
            if (PC == 1):                               
                if(j == n+1):
                    Cm[i,j-1] = max(K-Pm[i,j-1], 0)     
                else:
                    Cm[i,j-1] = m.exp(-.05*dt) * (p*Cm[i,j] + (1-p)*Cm[i+1,j]) 
            if (PC == 0):                               
                if (j == n + 1):
                    Cm[i,j-1] = max(Pm[i,j-1]-K, 0)     
                else:
                    Cm[i,j-1] = m.exp(-.05*dt) * (p*Cm[i,j] + (1-p)*Cm[i+1,j])  
    return [Pm,Cm] 


#Enter initial conditions:

S = 100
k = 100
r = .05
v = .3
T = 20/36
n = 17
PC = 0  # 0 for call, 1 for put
Pm,Cm = OptionsVal(n,S,k,r,v,T,PC)
print('Pricing:\n',np.matrix(Pm.astype(int)))
print('Option Values:\n',np.matrix(Cm.astype(int)))




