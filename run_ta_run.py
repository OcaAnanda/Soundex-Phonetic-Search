import soundex as sd
import secondtry as st
import numpy as np
import pandas as pd

column=['Kode']
sdx = pd.read_csv("C:\Users\Hasan Wirasno\OneDrive\Documents\TA OCA\soundexquran.txt",header=None,names=column,delimiter="\n")

kode = []

for i in xrange(len(sdx)):
    kode.append(sdx.at[i,'Kode'])

query = sd.do_query()

dataset = sd.loadTextFile('Alquran')

size_x=1
size_y=len(sdx)
distance=[]
sorted_dist=np.zeros((size_y,size_x+1))

#dataframe untuk menampung hasil
result= pd.DataFrame(columns=['Ayat','Kode','Jarak'])
    
for line in xrange(len(sdx)):
    distance.append(st.LD(sdx.at[line,'Kode'],query))


for i in xrange(len(dataset)):
    #masukkan semua hasil ke dataframe
    
#urutkan jarak secara ascending
result = result.sort_values(['Jarak'])
    

    
            

