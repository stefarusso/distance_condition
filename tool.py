#Users/stefano/anaconda3/bin/python
import pandas as pd
import numpy as np
import glob
import os

travis_log_file='travis.log'

names=[]
key=[]
with open(travis_log_file, 'r') as file:
    lines = [line for line in file if "- Molecule" in line ]
    for line in lines:
        names.append( line.split()[3] )
        key.append( int(line.split()[4].strip("("))  )
dictionary=dict(zip(names,key))

def avg_cond(file,dictionary):
    filename=file.split("/")[1]
    RM = filename.split("_")[2].strip(".csv")
    OM = filename.split("_")[3].strip(".csv")
    conditions = pd.read_csv(file, header=0, delimiter =';')
    n = (conditions.shape[1]-4)/2
    idx = 2*np.arange(n)+4
    means = conditions.iloc[:,idx].mean(axis=0)
    zero = conditions.iloc[:,1].mean(axis=0)
    zero = dictionary[RM] - zero 
    means = np.append(zero, means)
    if means[-1]>0:
        print("ERROR!!! use higher number of first neighbours in travis conditions ", n, " is not enough" )
        print(filename, " needs to be recalculated")
    else:
        weights = means.sum()
        means = sum(np.arange(n+1)*means )/weights
        return means, RM, OM


directory= [name for name in os.listdir(".") if os.path.isdir(name)]
mem = {} 
for d in directory:
    files = glob.glob(d+"/*csv",recursive=True)
    rows = []
    AVG = []
    columns = []
    for file in files:
        avg, RM, OM = avg_cond(file,dictionary)
        columns = RM
        rows.append(OM)
        AVG.append(avg)
    tmp = pd.DataFrame(data=AVG, index=rows, columns=[columns]).sort_index()
    rows= tmp.index
    mem[RM] = tmp.iloc[:,0]

mem=pd.DataFrame(mem,index=rows)
print(mem)
mem.to_csv("cond.csv")

