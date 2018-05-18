
import numpy as np

##Exact String Matching dg Boyer Moore
def bmstringmatch(query,dataset):
    j = len(query)-1
    i = len(query)-1
    for m in range(0,len(dataset)-1):
        if query[j] in (dataset[i]):
            if j == 0:
                print i
            else:
                i -= 1
                j -= 1
        else:
            #last() char returns -1 if not found
            i = i + m - np.minimum(j,1+dataset[i].find(dataset[i][-1:]))
            j = m - 1

#Morris-Pratt
def preMP(dataset):
    mpNext = [None]*len(dataset)
    m = len(dataset)
    j = mpNext[0] = -1
    i = 0
    while (i<m):
        while ((j > -1) and (dataset[i] != dataset[j])):
            j = mpNext[j]
        i += 1
        j += 1
        if (dataset[i] is dataset[j]):
            mpNext[i] = mpNext[j]
        else:
            mpNext[i] = j
                     
    return mpNext

def MP(dataset,query):
    i = 0
    n = len(query)
    m = len(dataset)
    ketemu = [None]*(m-1)
    mpNext = [None]*len(dataset)
    
    #preprocess
    preMP(dataset)
    
    #Searching
    while (i<=m-n):
        j = 0
        while (j<n and dataset[i+j] == query[j]):
            j+=1
            
        if(j >= n):
            ketemu[i]=True
            
        next = j - mpNext[j]
        i = i+next


def LD(dataset, query):
    if dataset == "":
        return len(query)
    if query == "":
        return len(dataset)
    if dataset[-1] == query[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD(dataset[:-1], query)+1,
               LD(dataset, query[:-1])+1, 
               LD(dataset[:-1], query[:-1]) + cost])
    return res