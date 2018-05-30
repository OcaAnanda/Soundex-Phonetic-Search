
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
    size_x = len(query) + 1
    size_y = len(dataset) + 1
    matrix = np.zeros ((size_x, size_y))
    #jarak dari matrix substring dataset dan substring query
    for x in xrange(size_x):
        matrix [x, 0] = x
    for y in xrange(size_y):
        matrix [0, y] = y

    for x in xrange(1, size_x):
        for y in xrange(1, size_y):
            if query[x-1] == dataset[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    print (matrix)
    return (matrix.item(size_x - 1, size_y - 1))