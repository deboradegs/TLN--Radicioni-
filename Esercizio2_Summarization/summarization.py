import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.corpus import semcor, stopwords
from nltk.corpus.reader import Lemma
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from rouge_score import rouge_scorer
import string
import numpy as np
import py_babelnet as bn
import random
import re
import os
from rouge_metric import PerlRouge


dict_nasari = dict()
df_nasari = pd.read_csv('Esercizio2_Summarization/nasari/dd-small-nasari-15.txt', sep=';', header=None)


for rows in df_nasari.itertuples():
    if rows[2] in dict_nasari.keys():  
        dict_nasari[str(rows[2]).lower()].extend(list(rows[3:16]))
    else:
        dict_nasari[str(rows[2]).lower()]= list(rows[3:16])
    
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
string_punctuation = string.punctuation + '``'+'\'\'' + '’' + '“'+ '”'+'‘' 

def stem_lem(text):
    words = list()
    for word in word_tokenize(str(text).lower()):
        lemma = lemmatizer.lemmatize(word)
        if lemma not in stop_words and lemma not in string_punctuation:
            words.append(lemma)
    return words


def read_and_split(doc):
    paragraphs = list()
    document = open(doc, 'r')
    for line in document:
        if len(line) > 1 and not line.startswith('#'):
            paragraphs.append(line.replace('\n', ""))
    document.close()
    return paragraphs


def extract_context(doc):
    kw = stem_lem(doc[1])
    kw.extend(stem_lem (doc[2]))
    kw.extend(stem_lem(doc[len(doc)-1]))
    kw= list(dict.fromkeys(kw))
    nasaris = list()
    for k in kw:
        if str(k) in dict_nasari.keys():
            nasaris.extend(dict_nasari[k])
    context = list()
    for n in nasaris:
        n = str(n).split('_')[0]
        context.append(n)
        
    return context        
    

def weighted_overlap(v1,v2):
    v1_cleaned = list()
    v2_cleaned = list()
    numerator = 0
    denominator = 0    
    for w in v1:
        w = str(w).split('_')[0]
        v1_cleaned.append(w)
    for w in v2:
        w = str(w).split('_')[0]
        v2_cleaned.append(w)
    wo = 0
    intersection_v1_v2 = set(v1_cleaned).intersection(set(v2_cleaned))
    if len(intersection_v1_v2) > 0:
        counter = 1
        for v in intersection_v1_v2:
            numerator += pow((v1_cleaned.index(v)+1)+(v2_cleaned.index(v)+1), -1)
            denominator += pow(2*counter, -1)
            counter+=1
        wo = numerator/denominator
    return wo


def rerank_paragraphs(context, doc):
    ranked_paragraphs = list()
    for paragraph in doc:
        paragraph_wo = dict.fromkeys(['index', 'paragraph', 'rank_score'])        
        list_words = stem_lem(paragraph)
        sum_overlap = 0
        for word in list_words:
            max = 0
            nasari_word = list()
            if word in dict_nasari.keys():
                nasari_word = dict_nasari[word] 
            for c in context:
                nasari_c = list()
                if c in dict_nasari.keys():
                    nasari_c = dict_nasari[c]
                    wo = weighted_overlap(nasari_word, nasari_c)
                    if wo > max:
                        max = wo
            sum_overlap+=max        
        if len(list_words) > 0:
            paragraph_wo['index'] = doc.index(paragraph)
            paragraph_wo['paragraph'] = paragraph
            paragraph_wo['rank_score'] = sum_overlap/len(list_words)
            ranked_paragraphs.append(paragraph_wo)
            #paragraph_wo[doc.index(paragraph)] = sum_overlap/len(list_words)
    #return sorted(paragraph_wo.items(), key=lambda x:x[1], reverse= True)
    return sorted(ranked_paragraphs, key=lambda x:x['rank_score'], reverse= True)


def summarize(ranked_paragraphs, percentage, splitted_doc):
    summarization = ' '
    #print(ranked_paragraphs)
    #number_of_paragraphs = round(percentage/100*paragraph_len)
    #final_paragraphs = ranked_paragraphs[:number_of_paragraphs]
    #final_paragraphs = sorted(final_paragraphs)
    #print(final_paragraphs)
    #for tuple in final_paragraphs:
    #    summarization = str(summarization) + " " + splitted_doc[tuple[0]]

    doc_num_words = len(str(splitted_doc[1:]).split(' '))
    doc_sum_num_words = (doc_num_words * percentage)/100
    num_write_words = 0
    save_num_write_words = 0

    index_new_paragraphs_list = list()

    index = 0
    while num_write_words < doc_sum_num_words:
        index_new_paragraphs_list.append(ranked_paragraphs[index]['index'])
        num_write_words += len(str(ranked_paragraphs[index]['paragraph']).split(' '))
        save_num_write_words = num_write_words - len(str(ranked_paragraphs[index]['paragraph']).split(' '))
        index+=1

    if (num_write_words - doc_sum_num_words) > (doc_sum_num_words - save_num_write_words):
        index_new_paragraphs_list.pop()

    ranked_paragraphs = sorted(ranked_paragraphs, key=lambda x:x['index'], reverse= False)

    for i in range(0, len(ranked_paragraphs)):
        if ranked_paragraphs[i]['index'] in index_new_paragraphs_list:
            summarization = str(summarization) + " " + ranked_paragraphs[i]['paragraph']

    print('numero parole testo originale')
    print(doc_num_words)
    print('numero parole che dovrebbe avere la summarization')
    print(doc_sum_num_words)
    print('numero parole che ha il testo riassunto')
    print(len(str(summarization).split(' ')))
    print()    

    return summarization

documents = os.listdir('Esercizio2_Summarization/texts')
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

for doc in documents:
    splitted_doc = read_and_split('Esercizio2_Summarization/texts/'+doc)
    paragraph_len = len(splitted_doc)
    context = extract_context(splitted_doc)
    par = rerank_paragraphs(context, splitted_doc)
    print(doc)
    summary90 = summarize(par, 90, splitted_doc)
    summary80 = summarize(par, 80, splitted_doc)
    summary70 = summarize(par, 70, splitted_doc)
    outF = open('Esercizio2_Summarization/summaries/90_'+ doc, "w")
    outF.write(str(summary90))
    outF.close()
    outF = open('Esercizio2_Summarization/summaries/80_'+ doc, "w")
    outF.write(str(summary80))
    outF.close()
    outF = open('Esercizio2_Summarization/summaries/70_'+ doc, "w")
    outF.write(str(summary70))
    outF.close()


scores = PerlRouge().evaluate_from_files('Esercizio2_Summarization/summaries', 'Esercizio2_Summarization/automatic_summaries')

rouge_1 = scores['rouge-1']
rouge_2 = scores['rouge-2']

print('Rouge-1 scores')
print('Recall score: {}'.format(rouge_1['r']))
print('Precision score: {}'.format(rouge_1['p']))
print()
print('Rouge-2 scores')
print('Recall score: {}'.format(rouge_2['r']))
print('Precision score: {}'.format(rouge_2['p']))
