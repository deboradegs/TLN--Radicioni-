import pandas as pd

df_nasari = pd.read_csv('Esercizio2_Summarization/nasari/dd-small-nasari-15.txt', sep=';', header=None)


def read_and_split(doc):
    paragraphs = list()
    document = open(doc, 'r')
    for line in document:
        if len(line) > 1:
            paragraphs.extend(line.split('\n'))
    document.close()


read_and_split('Esercizio2_Summarization/utils/Andy-Warhol.txt')