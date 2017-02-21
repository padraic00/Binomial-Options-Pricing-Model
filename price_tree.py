
# coding: utf-8

# # Binary Options Pricing
# By Padraic McAtee
#     
# My notation here is based on the original Cox, Ross and Rubinstein paper.

# In[4]:

import numpy as np
import math as m
import timeit

def bop(n,t,S,v):
    dt = t/n
    u = m.exp(v*m.sqrt(dt))
    d = 1/u
    Pm = np.zeros((n+1, n+1))
    for j in range(n+1):
        for i in range(j+1):
            Pm[i,j] = S*m.pow(d,i) * m.pow(u,j-i)
    return Pm


# I generated the pricing tree for a few n values...

# In[5]:

n = 5
t = 200/365
S = 100
v = .3
x = bop(n,t,S,v)
n = 17
z = bop(n,t,S,v)

print('n = 5:\n',np.matrix(x.astype(int)))
print('n = 17:\n',np.matrix(z.astype(int)))


# After noticing the recursive pattern in the tree, I generated the set of all unique numbers in the matrix as an ordered 1d array and looped through the elements of the pricing matrix calling values from the unique set. 

# In[6]:

def better_bop(n,t,S,v):
    dt = t/n
    u = m.exp(v*m.sqrt(dt))
    d = 1/u
    ups = np.zeros(n+1)
    dwns = np.zeros(n+1)
    tot = np.zeros(2*n+1)
    Pm = np.zeros((n+1, n+1))
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
    return Pm
trial = better_bop(n,t,S,v)
print('n = 17:\n',np.matrix(trial.astype(int)))


# Testing for consistency and timing...

# In[7]:

get_ipython().run_cell_magic('timeit', '', 'method1 = bop(n,t,S,v)')


# In[8]:

get_ipython().run_cell_magic('timeit', '', 'method2 = better_bop(n,t,S,v)')


# In[9]:

method1 = bop(n,t,S,v)
method2 = better_bop(n,t,S,v)
print('\nConsistent entries?: ' , np.allclose(method1,method2)) #tests if the matrices are equal


