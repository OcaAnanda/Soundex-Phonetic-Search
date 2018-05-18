import pandas as pd
import numpy as np

def loadTextFile(filename):
    column=['No. Surat','Nama Surat','Ayat','Isi Ayat']
    open = pd.read_csv("C:\Users\Hasan Wirasno\OneDrive\TA OCA\Alquran.txt",header=None,names=column,delimiter=",")
    dataset = open.iloc[:,3].values
    ds = []
    for word in dataset :
        ds += str(word).split(' ')
        
    return ds

def encode(string):
    s=string.lower()
    soundexcode = ""
    for line in range(0,len(s)):
        if s[line] in ('a','e','i','o','u','h','y'):
            soundexcode += "/"
        elif s[line] in ('b','p'):
            soundexcode += "0"
        elif s[line] in ('c','j','s','x','z'):
            soundexcode += "1"
        elif s[line] in ('d'):
            soundexcode += "2"
        elif s[line] in ('f','v'):
            soundexcode += "3"
        elif s[line] in ('g','k','q'):
            soundexcode += "4"
        elif s[line] in ('l'):
            soundexcode += "5"
        elif s[line] in ('m'):
           soundexcode += "6"
        elif s[line] in ('n'):
            soundexcode += "7"
        elif s[line] in ('r'):
            soundexcode += "8"
        elif s[line] in ('t'):
            soundexcode += "9"
        elif s[line] in ('w'):
            soundexcode += "10"
    return soundexcode


def deleterepeats(string):
    temp = ""
    temp += string[0]
    if len(string) > 1:
        for i in range(0,(len(string)-1)):
            if string[i] != string[i+1]:
                temp += string[i+1]
        return temp
    else:
        return string


def dosoundexind(name):
    encodedname = encode(name)
    norepeats = deleterepeats(encodedname)
    str = name[0].lower()+norepeats[1:] #menggabungkan huruf awal query ditambah kode soundex
    str1 = (str.replace("/","")+"***")
    strcut = str1[0:4]
    return strcut 
    
def normalize(text):
    text = text.lower()
    text = text.replace("\\b'([^aiu])","k$1")
    text = text.replace("\\b`([^aiu])","k$1")
    text = text.replace("\\bal`", "")
    text = text.replace("\"", "")
    text = text.replace("'", "")#penghilangan petik
    text = text.replace("`", "")#penghilangan petik

    text = text.replace("\\b(a)l([t,s,d,z,r,d,l,n])", "$1$2")#alif lam syamsiah
    text = text.replace("\\b([^aiu][aiu])l([t,s,d,z,r,d,l,n])", "$1$2")
    #text = text.replace("\\b(a)[^aiu]", "$1")#penghilangan al tasdid,doubel alrr,alshsh

    text = text.replace("\\biyy", "i")
    text = text.replace("kh","h")
    text = text.replace("sh", "s") #referensi Tabel 3 paper IPB dan
    text = text.replace("ts", "s")#pemadanan aksara latin arab-indo kemenag
    text = text.replace("sy", "s")
    text = text.replace("dz", "z")
    text = text.replace("zh", "z")
    text = text.replace("dh", "d")
    text = text.replace("th", "t")
    text = text.replace("q", "k")
    text = text.replace("aw", "au")
    text = text.replace("ay", "ai")

    text = text.replace("v","f")
    text = text.replace("p","f")
    text = text.replace("j","z")

    text = text.replace("ng", "n")#ikhfa
    text = text.replace("nb", "mb")#iqlab
    text = text.replace("ny", "y")#idgham
    text = text.replace("nw", "w")#idgham
    text = text.replace("nm", "m")#idgham
    text = text.replace("nn", "n")#idgham
    text = text.replace("nl", "l")#idgham
    text = text.replace("nr", "r")#idgham
    textStr=str(text)
    return textStr


def idf (query,dataset):
    N=len(dataset)
    result = pd.DataFrame(columns=['word','idf'])
    #untuk df
    dft=[]
    for idx,value in enumerate(dataset):
        if (query in value):
            dft.append(1)
    
    #menghitung idf dengan add+1 smoothing
    df_val=sum(dft)
    idft = np.log10(N/(df_val+1))
    
    #Tambahkan idf untuk kata yang diinputkan pada dataframe
    result = result.append(pd.Series([query,idft],index=['word','idf']),ignore_index=True)
    #return variabel result
    return result
    
def tf (query,dataset):
    #Buat dataFrame kosong untuk menampung TF
    result = pd.DataFrame()
    #hitung frequensi query pada setiap line di dataset
    ft = np.add([s.count(query) for s in dataset],0)
    #TF log normalization
    ftd = 1 + np.log10(ft)
    #tambahkan hasil ftd kedalam dataframe
    result = result.append(pd.Series(ftd),ignore_index=True)
    result = result.replace(-np.inf, 0)
    #return variabel result
    return result

def tfIDF(tf,idf):
    #Dataframe untuk menampung tfIDF
    result = pd.DataFrame()
    #untuk setiap tf
    for i in tf:
        #tf idf untuk document term weighting tf*idf
        tfIdf=(tf[i]*idf['idf'])
        #tambahkan hasil perhitungan tf idf kedalam dataframe
        result = result.append(pd.Series(tfIdf),ignore_index=True)
    return result

def cosine_sim(idf,tf_idf):
   #menghitung perkalian skalar query & dataset
   q = idf.iloc[:,1].values
   d = tf_idf.iloc[:,0].values
   skalar = []
   cosim=[]
   
   #mendapatkan perkalian skalar
   for i in range(len(tf_idf)):
       skalar.append(q[0]*d[i])
       cosim.append((skalar[i])/np.sqrt(skalar[i]))
   return cosim

def run():
    ds = loadTextFile('Alquran')
    query = input ('Masukkan query : ')
    
    qnormal = normalize(query)
    print ("Normalisasi : ",qnormal)
    s1=dosoundexind(qnormal)
    print ("Kode fonetis :",s1)
    
    words = []
    s2=[]
    for line in range(0,len(ds)):
        ds[line] = ds[line].replace(ds[line],normalize(ds[line]))
        s2.append(dosoundexind(ds[line]))
    
    idf_val = idf(s1,s2)
    tf_val = tf(s1,s2)
    tf_idf = tfIDF(tf_val,idf_val)
    cos_sim = cosine_sim(idf_val,tf_idf)
    
    return (words,s2,idf_val,tf_val,tf_idf,cos_sim)