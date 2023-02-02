# TLN--ESERCITAZIONE SUMMARIZATION-

##Individuazione del topic e creazione del contesto

Abbiamo creato il topic del testo prendendo i vettori di Nasari delle parole presenti nel titolo, nel paragrafo introduttivo e in quello conclusivo.

##Individuazione e riordinamento dei paragrafi contenenti i termini più rilevanti

Per ogni parola di ogni paragrafo abbiamo calcolato la weighted overlap rispetto al contesto, trovando così i paragrafi con maggiore overlap col contesto, 
per permetterci di riordinarli per rilevanza. 
Per ogni parola del paragrafo abbiamo contato solo l'overlap con la parola del contesto che avesse massimo valore. 
Per trovare la rilevanza del paragrafo abbiamo sommato tutti gli overlap così trovati per le sue parole.

##Summarization

Partendo dall'elenco di paragrafi riordinati per rilevanza abbiamo riscritto il testo prendendo il numero di paragrafi tale per cui il numero di parole del riassunto
si avvicinasse maggiormente al numero di parole del testo compresso della percentuale richiesta.

## Risultati

Abbiamo calcolato la BLUE precision e la ROUGE recall per ogni documento riassunto implementando le formule e usando come golden summary i riassunti ottenuti da https://resoomer.com/en.
Per calcolare precision e recall del summarizer in generale abbiamo prima fatto la media delle precision e delle recall prima trovate e poi, come confronto, abbiamo utilizzato
la classe PerlRouge di rouge_metric, calcolando lo score sia sul confronto di singole parole che di coppie di parole.

```
Similarity results
           Word 1    Word 2  Human (mean)  wu_palmer_similarity  shortest_path_similarity  leakcock_chodorow_similarity
0            love       sex          6.77              0.909091                        39                      3.020425
1           tiger       cat          7.35              0.962963                        39                      3.020425
2           tiger     tiger         10.00              1.000000                        40                      3.713572
3            book     paper          7.46              0.857143                        38                      2.614960
4        computer  keyboard          7.62              0.800000                        37                      2.327278
..            ...       ...           ...                   ...                       ...                           ...
348        shower     flood          6.03              0.533333                        36                      2.104134
349       weather  forecast          8.34              0.000000                        27                      1.074515
350      disaster      area          6.25              0.428571                        32                      1.516347
351      governor    office          6.34              0.470588                        31                      1.410987
352  architecture   century          3.78              0.181818                        31                      1.410987

[353 rows x 6 columns]


Wu & Palmer Pearson correlation coefficient
--------------------------------------------------------
0.26705872312041734

Wu & Palmer Spearman's rank correlation coefficient
--------------------------------------------------------
0.3071210105989976


Shortest Path Pearson correlation coefficient
--------------------------------------------------------
0.06668933450180664

Shortest Path Spearman's rank correlation coefficient
--------------------------------------------------------
0.2707195125455104


Leeckock & Chodorow Pearson correlation coefficient
--------------------------------------------------------
0.27191049386567595

Leeckock & Chodorow Spearman's rank correlation coefficient
--------------------------------------------------------
0.2707195125455104
```

