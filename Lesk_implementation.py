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
    #context = []
    #pos ? -> il lemmatize si aspetta un pos_tag
    context = stem_lem(sentence)
    # for w in sentence:
    #     if w!=word:
    #         context.append(w)
    return context

def get_signature(syn):
    signature = []
    for ex in syn.examples():
        signature.extend(stem_lem(ex))
    signature.extend(stem_lem(syn.definition()))
    return signature

def get_overlap(signature, context):
    #signature = 0
    intersection = list(set(signature) & set(context))
    return len(intersection)

def lesk_algorithm(word, sentence):
    best_sense = wn.synsets(word)[0]
    max_overlap = 0
    context = get_context(sentence) #tutte le parole di sentence meno word
    #print(context)
    for syn in wn.synsets(word):
        signature = get_signature(syn) #Esempi più glossario (descrizioni)
        #print(signature)
        overlap = get_overlap(signature, context) #overlap tra il nostro contesto polisemico e la signature
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = syn
    #print(best_sense)
    #print(best_sense.lemmas())
    return best_sense


lesk_algorithm('cat', 'the cat is on the table')


##########################


print('Loading semcor sentences . . .')
semcor_sents = semcor.sents()
tagged_semcor_sents = semcor.tagged_sents(tag='both')
semcor_sents_length = len(semcor_sents)
print('Semcore sentences successfully loaded')

#print(semcor_sents)
#print(tagged_semcor_sents)
#print(semcor_sents_length)

def clear(lista):
    cleaned_list = []
    for i in range(0, len(lista)):
        if str(lista[i]).lower() not in stop_words and lista[i] not in string_punctuation:
            cleaned_list.append(lemmatizer.lemmatize(str(lista[i]).lower()))
    return cleaned_list


random_list = random.sample(range(semcor_sents_length), 50)
fifty_sents = []
for i in random_list:
    nouns_sents = []
    fifty_sents.append(clear(semcor_sents[i]))
    for tree in tagged_semcor_sents[0]:
        if 'Lemma' in str(tree.label()) and tree[0].label() == 'NN':
            nouns_sents.append(tree)
        print()
        print(tree)
        print(tree.label())
        print(tree[0])
        #print(tree[0].label()) ???????????????
        print(type(tree))
      
    print(nouns_sents)


#print(fifty_sents)




