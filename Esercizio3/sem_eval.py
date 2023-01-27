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
    df_scores = dict.fromkeys(['Term1', 'Term2', 'average_score'])
    df_scores['Term1'] = rows[1]
    df_scores['Term2'] = rows[2]
    df_scores['average_score'] = round((int(rows[3])+int(rows[4])+int(rows[5]))/3, 2)
    terms.append(df_scores)


def calculate_cosine_sim():
    max_cosine = 0
    dicts_score_cosine = list()
    list_annotate_score = list()
    list_cosine_sim = list()
    for dizio in terms:
        if dizio['Term1'] in dict_semVal and dizio['Term2'] in dict_semVal:
            babel1 = dict_semVal[dizio['Term1']] 
            babel2 = dict_semVal[dizio['Term2']]
            for bn1 in babel1:
                if bn1 in dict_nasari.keys():
                    nasari1 = dict_nasari[bn1]
                    for bn2 in babel2:
                        if bn2 in dict_nasari.keys():
                            nasari2 = dict_nasari[bn2]
                            cosine_sim = (np.dot(nasari1, nasari2)) / (np.linalg.norm(nasari1) * np.linalg.norm(nasari2))
                            if cosine_sim > max_cosine:
                                max_cosine = cosine_sim
                                max_babel1 = bn1
                                max_babel2 = bn2
            dizio['cosine_sim'] = max_cosine
            dizio['bn1'] = max_babel1
            dizio['bn2'] = max_babel2
            list_annotate_score.append(dizio['average_score'])
            list_cosine_sim.append(max_cosine)
            dicts_score_cosine.append(dizio)
    df = pd.DataFrame(list(zip(list_annotate_score,list_cosine_sim)), columns = ['Average_Score_Annotate','Cosine_Sim'])
    return dicts_score_cosine, df

dicts_score_cosine = calculate_cosine_sim()[0]
df_calculate_scores = calculate_cosine_sim()[1]


pearson_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='pearson')
spearman_valutation = df_calculate_scores['Average_Score_Annotate'].corr(df_calculate_scores['Cosine_Sim'], method='spearman')

print(pearson_valutation)
print(spearman_valutation)