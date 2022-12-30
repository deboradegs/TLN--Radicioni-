import pandas as pd
from nltk.corpus import wordnet
from itertools import product
import math

depthMax = 20

df = pd.read_csv("WordSim353/WordSim353.csv")
word1 = df.iloc[0][0]
word2 = df.iloc[0][1]

# def get_hyperonyms2(synset):
#     hyperonyms=[]
#     for hyperonym in synset.hypernyms():
#         hyperonyms.append(hyperonym)
#     return hyperonyms

def get_hyperonyms(synset_list):
    hyperonyms=[]
    for synset in synset_list:
        for hyperonym in synset.hypernyms():
            hyperonyms.append(hyperonym)
    return hyperonyms

def get_depth(w):
    depth = 0
    next_hyper = w
    while(next_hyper != w.root_hypernyms()[0] and len(next_hyper.hypernyms())!=0):
        depth += 1
        next_hyper = next_hyper.hypernyms()[0]
    return depth

# def lcs2(syns1, syns2):
#     hypers1 = [syns1]
#     hypers2 = [syns2]
#     intersection = list(set(hypers1) & set(hypers2))
#     #print(intersection)
#     supp_list1=[syns1]
#     supp_list2=[syns2]
#     while len(intersection)==0:
#         for syn1 in supp_list1:
#             supp_list1 = get_hyperonyms2(syn1)
#             hypers1.extend(supp_list1)
#         #print(hypers1)
#         for syn2 in supp_list2:
#             supp_list2= get_hyperonyms2(syn2)
#             hypers2.extend(supp_list2)
#         #print(hypers2)
#         intersection = list(set(hypers1) & set(hypers2))
#         if len(supp_list1)==0 and len(supp_list2) == 0 and len(intersection) == 0:
#             break
#     return intersection

def lcs(syns1, syns2):
    hypers1 = [syns1]
    hypers2 = [syns2]
    intersection = list(set(hypers1) & set(hypers2))
    #print(intersection)
    supp_list1=[syns1]
    supp_list2=[syns2]
    while len(intersection)==0:
        if len(supp_list1)>0:
            supp_list1 = get_hyperonyms(supp_list1)
        #print(hypers1)
        if len(supp_list2)>0:
            supp_list2 = get_hyperonyms(supp_list2)
        #print(hypers2)
        hypers1.extend(supp_list1)
        hypers2.extend(supp_list2)
        intersection = list(set(hypers1) & set(hypers2))
        if len(supp_list1)==0 and len(supp_list2) == 0 and len(intersection) == 0:
            break
    return intersection
    

def Similarity(w1, w2):
    #res = w1.lowest_common_hypernyms(w2)
    res = lcs(w1, w2)
    #print()
    #print()
    #print(res2)
    #print(res)
    depth  = 0
    if len(res) != 0:
        result = res[0]
        depth = get_depth(result)

    depth1 = get_depth(w1)
    depth2 = get_depth(w2)

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
    

#Leeckock -> deb


#Shortest Path = 2*depthMax - length(s1,s1)
#length(s1,s2) = length(s1,lcs) + length(s2, lcs)
#lcs tra s1 e s2

def get_length_lcs(s, lcs_s1_s2):
    length =0
    next_hyper = s
    while(next_hyper != lcs_s1_s2[0] and len(next_hyper.hypernyms())!=0):
        length += 1
        next_hyper = next_hyper.hypernyms()[0]
    return length

def get_length(s1, s2):
    lcs_s1_s2 = lcs(s1, s2)
    if len(lcs_s1_s2)==0:
        #print("bohhhh")
        return 2*depthMax
    else:
        #print(lcs_s1_s2[0])
        return get_length_lcs(s1, lcs_s1_s2) + get_length_lcs(s2, lcs_s1_s2) 

def shorterst_path_similarity(s1,s2):
    length=get_length(s1, s2)
    simpath=2*depthMax-length
    return simpath

def shorterst_path(w1,w2):
    syn1 = wordnet.synsets(w1)
    syn2 = wordnet.synsets(w2)
    max = 0
    sim = 0
    for syn in syn1:
        for sy in syn2:
            sim = shorterst_path_similarity(syn, sy)
            if sim>max:
                max = sim
    return max



#print(WuAndPalmer(word1, word2))
#print(shorterst_path(word1, word2))

wu_palmer = []
short_path = []
for i in range(len(df)):
    wu_palmer.append(WuAndPalmer(df.iloc[i][0],df.iloc[i][1]))
    short_path.append(shorterst_path(df.iloc[i][0],df.iloc[i][1]))

df['Wu_Palmer'] = wu_palmer
df['shortPath'] = short_path

print(df)


#Pearson and Sperman

pearson = df['Human (mean)'].corr(df['Wu_Palmer'], method='pearson')
spearman = df['Human (mean)'].corr(df['Wu_Palmer'], method='spearman')



#print(pearson)
#print(spearman)
