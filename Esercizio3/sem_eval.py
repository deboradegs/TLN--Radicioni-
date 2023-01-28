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

df_scores = pd.read_csv('Esercizio3/chierchiello.csv', sep=',', header=None)


pearson_agreement = (df_scores[2].corr(df_scores[3], method='pearson')+ \
            df_scores[2].corr(df_scores[4], method='pearson')+ \
            df_scores[3].corr(df_scores[4], method='pearson'))/3
spearman_agreement = (df_scores[2].corr(df_scores[3], method='spearman')+\
            df_scores[2].corr(df_scores[4], method='spearman')+\
            df_scores[3].corr(df_scores[4], method='spearman'))/3

terms = list()
for rows in df_scores.itertuples():
    #print(rows)
    dict_scores = dict.fromkeys(['Term1', 'Term2', 'average_score'])
    dict_scores['Term1'] = rows[1]
    dict_scores['Term2'] = rows[2]
    dict_scores['average_score'] = round((int(rows[3])+int(rows[4])+int(rows[5]))/3, 3)
    terms.append(dict_scores)

#print(terms)


def calculate_cosine_sim():
    dicts_score_cosine = list()
    list_annotate_score = list()
    list_cosine_sim = list()
    for dizio in terms:
        max_cosine_total = 0
        if dizio['Term1'] in dict_semVal.keys() and dizio['Term2'] in dict_semVal.keys():
            babel1 = dict_semVal[dizio['Term1']] 
            babel2 = dict_semVal[dizio['Term2']]
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
        
            dizio['cosine_sim'] = max_cosine_total
            dizio['bn1'] = max_babel1
            dizio['bn2'] = max_babel2
            #print(dizio)
            list_annotate_score.append(dizio['average_score'])
            list_cosine_sim.append(max_cosine_total)
            dicts_score_cosine.append(dizio)
    df = pd.DataFrame(list(zip(list_annotate_score,list_cosine_sim)), columns = ['Average_Score_Annotate','Cosine_Sim'])
    return dicts_score_cosine, df

dicts_score_cosine = calculate_cosine_sim()[0]
df_calculate_scores = calculate_cosine_sim()[1]

pearson_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='pearson')
spearman_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='spearman')

print(pearson_valutation)
print(spearman_valutation)

#print(dicts_score_cosine)
# list1= [('bn:123456n','bn:124565n'),('bn:567888n','bn:000234n'),('bn:000111n', 'bn:111222n')]
# list2 = [('bn:349445n', 'bn:124564n'), ('bn:123565n','bn:123665n'), ('bn:128565n','bn:163665n')]
# df_prova= pd.DataFrame(list(zip(list1,list2)), columns = ['lista1','lista2'])

# pearson_valutation_prova= df_prova['lista1'].corr(df_prova['lista2'], method='pearson')
# spearman_valutation_prova = df_prova['lista1'].corr(df_prova['lista2'], method='spearman')
# print('pearson_prova')
# print(pearson_valutation_prova)

df_damonte = pd.read_csv('Esercizio3/damonte_senses.csv', sep=',', header=None, names=['Term1', 'Term2', 'bn1','bn2'])
df_degaetano = pd.read_csv('Esercizio3/deGaetano_senses.csv', sep=',', header=None, names=['Term1', 'Term2', 'bn1','bn2'])


kappa_damonte_degaetano = sklearn.metrics.cohen_kappa_score(np.array(df_damonte['bn1']), np.array(df_degaetano['bn1']))
print(kappa_damonte_degaetano)

