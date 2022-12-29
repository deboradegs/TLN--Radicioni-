import pandas as pd
from nltk.corpus import wordnet
from itertools import product
import math

df = pd.read_csv("WordSim353/WordSim353.csv")
#print(df.iloc[3][0], df.iloc[3][1])


#word1 = df.iloc[4][0]
#word2 = df.iloc[4][1]

#print(len(df))



def Similarity(w1, w2):
    res = w1.lowest_common_hypernyms(w2)
    depth  = 0
    
    if len(res) != 0:
        result = res[0]
        next_hyper = result
        while(next_hyper != result.root_hypernyms()[0]):
            depth += 1
            next_hyper = next_hyper.hypernyms()[0]

    
    depth1 = 0
    next_hyper1 = w1
    #print(next_hyper1.hypernyms())
    while(next_hyper1 != w1.root_hypernyms()[0] and len(next_hyper1.hypernyms())!=0):
        depth1 += 1
        next_hyper1 = next_hyper1.hypernyms()[0]

    depth2 = 0
    next_hyper2 = w2
    while(next_hyper2 != w2.root_hypernyms()[0] and len(next_hyper2.hypernyms())!=0):
        depth2 += 1
        next_hyper2 = next_hyper2.hypernyms()[0]

    if depth1 != 0 and depth2 != 0:
        similarity = 2*depth/(depth1+depth2)
    else:
        similarity=0
    
    return similarity


def WuAndPalmer(w1, w2):
    syn1 = wordnet.synsets(w1)
    syn2 = wordnet.synsets(w2)
    max = 0
    sim = 0
    for syn in syn1:
        for sy in syn2:
            sim = Similarity(syn, sy)
            if sim>max:
                max = sim
    return max
    

wu_palmer = []
for i in range(len(df)):
    wu_palmer.append(WuAndPalmer(df.iloc[i][0],df.iloc[i][1]))

df['Wu_Palmer similarity'] = wu_palmer

print(df)

#print(WuAndPalmer(word1, word2))

pears = df['Human (mean)'].corr(df['Wu_Palmer similarity'], method='pearson')

print(pears)