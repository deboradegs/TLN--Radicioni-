from nltk.corpus import wordnet as wn
from nltk.corpus import semcor, stopwords
from nltk.corpus.reader import Lemma
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
import string
import numpy as np
import random

lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
string_punctuation = string.punctuation + '``'+'\'\''

def stem_lem(text):
    words = list()
    for word in word_tokenize(str(text).lower()):
        lemma = lemmatizer.lemmatize(word)
        if lemma not in stop_words and lemma not in string_punctuation:
            words.append(lemma)
    return words

def get_context(sentence):
    context = stem_lem(sentence)
    return context

def get_signature(syn):
    signature = []
    for ex in syn.examples():
        signature.extend(stem_lem(ex))
    signature.extend(stem_lem(syn.definition()))
    return signature

def get_overlap(signature, context):
    intersection = list(set(signature) & set(context))
    return len(intersection)

def lesk_algorithm(word, sentence):
    best_sense = wn.synsets(word)[0]
    max_overlap = 0
    context = get_context(sentence) #tutte le parole di sentence
    for syn in wn.synsets(word):
        signature = get_signature(syn) #Esempi più glossario (definizioni e descrizioni)
        overlap = get_overlap(signature, context) #overlap tra il nostro contesto polisemico e la signature
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = syn
    return best_sense


##########################


print('Loading semcor sentences . . .')
semcor_sents = semcor.sents()
tagged_semcor_sents = semcor.tagged_sents(tag='both')
semcor_sents_length = len(semcor_sents)
print('Semcore sentences successfully loaded')

def clear(lista):
    cleaned_list = []
    for i in range(0, len(lista)):
        if str(lista[i]).lower() not in stop_words and lista[i] not in string_punctuation:
            cleaned_list.append(lemmatizer.lemmatize(str(lista[i]).lower()))
    return cleaned_list

def funzione():
    random_list = random.sample(range(semcor_sents_length), 50)
    fifty_sents = []
    sen = str
    punteggio = 0
    for i in random_list:
        nouns_sents = []
        sen = ' '.join(clear(semcor_sents[i]))
        for tree in tagged_semcor_sents[i]:
            if 'Lemma' in str(tree.label()) and ('NN' == str(tree.pos()[0][1]) or  str(tree.pos()[0][1]) == 'NNS') and len(wn.synsets(tree.pos()[0][0]))>0 :
                nouns_sents.append(tree)
        if len(nouns_sents)>0:
            noun=random.choice(nouns_sents)
            fifty_sents.append(clear(semcor_sents[i]))
            syns_dis_lesk = lesk_algorithm(noun.pos()[0][0], sen).lemmas()
            for syn in syns_dis_lesk:
                if(str(noun.label()) == str(syn)):
                    punteggio += 1

    return punteggio/len(fifty_sents)*100


risultati = 0 
for i in range(0,10):
    print("------------------------------------")
    print("Accuratezza esecuzione numero" + " " + str(i+1))
    res = funzione()
    risultati += res
    print(str(res)+"%")

print("------------------------------------")
print()
print()
print("Accuratezza media dell'algoritmo su 10 esecuzioni del programma: ")
print()
print(str(risultati/10)+"%")

