import pandas as pd
import re
import numpy as np

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

print(df_calculate_scores)

pearson_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='pearson')
spearman_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='spearman')

print(pearson_valutation)
print(spearman_valutation)