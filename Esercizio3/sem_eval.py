import pandas as pd
import re
import numpy as np
import sklearn.metrics

dict_nasari = dict()
dict_semVal = dict()

def create_dicts():
    doc_nasari = open('Esercizio3/utils/mini_NASARI.tsv', 'r')
    for line in doc_nasari:
        l = line.split("\t")
        babelnet_id = l[0].split("__")[0]
        dict_nasari[babelnet_id] = list(map(float, l[1:]))
    doc_semVal = open('Esercizio3/utils/SemEval17_IT_senses2synsets.txt', 'r')
    for line in doc_semVal:
        if line.startswith('#'):
            babel_list = list()
            word = re.sub('[#]', '', line).strip()
            dict_semVal[word] = list()
        else:
            babel_list.append(line.strip())
        dict_semVal[word] = babel_list

create_dicts()

df_scores = pd.read_csv('Esercizio3/words_from_Chierchiello.csv', sep=',', header=None)
df_damonte = pd.read_csv('Esercizio3/damonte_senses.csv', sep=',', header=None)
df_degaetano = pd.read_csv('Esercizio3/deGaetano_senses.csv', sep=',', header=None)
df_chierchiello = pd.read_csv('Esercizio3/chierchiello_senses.csv', sep=',', header=None)

pearson_agreement = (df_scores[2].corr(df_scores[3], method='pearson')+ \
            df_scores[2].corr(df_scores[4], method='pearson')+ \
            df_scores[3].corr(df_scores[4], method='pearson'))/3
spearman_agreement = (df_scores[2].corr(df_scores[3], method='spearman')+\
            df_scores[2].corr(df_scores[4], method='spearman')+\
            df_scores[3].corr(df_scores[4], method='spearman'))/3

dict_for_accuracy = dict()

def calculate_cosine_sim():
    list_annotate_score = list()
    list_cosine_sim = list()
    #i=0
    for row in df_scores.itertuples():
        max_cosine_total = 0
        if row[1] in dict_semVal.keys() and row[2] in dict_semVal.keys():
            babel1 = dict_semVal[row[1]] 
            babel2 = dict_semVal[row[2]]
            for bn1 in babel1:
                max_cosine_inter = 0
                if bn1 in dict_nasari.keys():
                    nasari1 = dict_nasari[bn1]
                    for bn2 in babel2:
                        if bn2 in dict_nasari.keys():
                            nasari2 = dict_nasari[bn2]
                            cosine_sim = (np.dot(nasari1, nasari2)) / (np.linalg.norm(nasari1) * np.linalg.norm(nasari2))
                            if cosine_sim > max_cosine_inter:
                                max_cosine_inter = cosine_sim
                                max_babel2 = bn2
                if max_cosine_inter > max_cosine_total:
                    max_cosine_total = max_cosine_inter 
                    max_babel1 = bn1
            average_scores = round((int(row[3])+int(row[4])+int(row[5]))/3, 3)
            list_annotate_score.append(average_scores)
            list_cosine_sim.append(max_cosine_total)
            dict_for_accuracy[(row[1], row[2])] = [(max_babel1, max_babel2)]#, (df_chierchiello['bn1'][i], df_chierchiello['bn2'][i])]
        #i+=1
    df = pd.DataFrame(list(zip(list_annotate_score,list_cosine_sim)), columns = ['Average_Score_Annotate','Cosine_Sim'])
    return df

df_calculate_scores = calculate_cosine_sim()

pearson_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='pearson')
spearman_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='spearman')


#Consegna 1:
print()
print('Consegna 1:')
print("----------------------------------------------------------")
print("Agreement between annotations")
print("Pearson coefficient: ", str(pearson_agreement))
print("Spearman coefficient: ", str(spearman_agreement))
print()
print("----------------------------------------------------------")
print("Correlation between human and machine")
print("Pearson coefficient: ", str(pearson_valutation))
print("Spearman coefficient: ", str(spearman_valutation))
print()


def evaluation(person):
    evaluation_couple_words = 0
    count_match = 0
    count_couple_match = 0
    i=0
    lista_babel = list()
    for tuple in dict_for_accuracy:
        #dict_for_accuracy[tuple].append((person['bn1'][i], person['bn2'][i]))
        if dict_for_accuracy[tuple][0] == (person[2][i], person[3][i]):
            count_couple_match+=1
        if dict_for_accuracy[tuple][0][0] == person[2][i]:
            count_match+=1
        if dict_for_accuracy[tuple][0][1] == person[3][i]:
            count_match+=1
        #dict_for_accuracy[tuple].remove((person['bn1'][i], person['bn2'][i]))
        lista_babel.append((person[2][i], person[3][i]))
        i+=1
    evaluation_single_word = count_match/(len(dict_for_accuracy)*2)
    evaluation_couple_words = count_couple_match/len(dict_for_accuracy)
    return evaluation_single_word, evaluation_couple_words, lista_babel
    

kappa_damonte_degaetano = sklearn.metrics.cohen_kappa_score(np.reshape(evaluation(df_damonte)[2], -1), np.reshape(evaluation(df_degaetano)[2], -1))
kappa_damonte_chierchiello = sklearn.metrics.cohen_kappa_score(np.reshape(evaluation(df_damonte)[2], -1), np.reshape(evaluation(df_chierchiello)[2], -1))
kappa_deGaetano_chierchiello = sklearn.metrics.cohen_kappa_score(np.reshape(evaluation(df_degaetano)[2], -1), np.reshape(evaluation(df_chierchiello)[2], -1))


#Consegna 2:
print()
print('Consegna 2:')
print("----------------------------------------------------------")
print("Agreement between annotations with Cohen similarity:")
print("Cohen similarity: ", str((kappa_damonte_degaetano+kappa_damonte_chierchiello+kappa_deGaetano_chierchiello)/3))
print()
print("----------------------------------------------------------")
print("Accuracy for single word (Chierchiello): {}".format(evaluation(df_chierchiello)[0]))
print("Accuracy for single word (Damonte): {}".format(evaluation(df_damonte)[0]))
print("Accuracy for single word (De Gaetano): {}".format(evaluation(df_degaetano)[0]))

print("\nAccuracy for pair word (Chierchiello): {}".format(evaluation(df_chierchiello)[1]))
print("Accuracy for pair word (Damonte): {}".format(evaluation(df_damonte)[1]))
print("Accuracy for pair word (De Gaetano): {}".format(evaluation(df_degaetano)[1]))
print()