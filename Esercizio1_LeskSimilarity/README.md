#### TLN--ESERCITAZIONE LESK SIMILARITY-

### Consegna 1

Abbiamo estratto le coppie di termini da analizzare dal file *WordSim353.csv* inserendole in un DataFrame.
Per calcolare la similarity tra queste coppie con i 3 metodi, abbiamo dovuto ovviare al problema di avere dei termini invece che dei sensi, come richiesti dalle formule. Abbiamo quindi estrapolato i sensi per ogni termine da WordNet. Per ogni coppia di termini abbiamo preso tutte le combinazioni di sensi e abbiamo richiamato i metodi per calcolare le tre similarità. Per ognuna di queste abbiamo trovato la coppia di sensi con similarità massima e abbiamo restituito il valore di quest'ultima.
Per farlo abbiamo creato i metodi sulla singola coppia di sensi e poi in *terms_similarity* abbiamo calcolato il massimo tra la similarità di tutte le combinazioni delle coppie di sensi per due parole.


# Wu & Palmer

Per calcolare "depth(LCS)" abbiamo innanzitutto dovuto trovare il primo antenato comune. Per farlo abbiamo preso la lista del primo livello di iperonimi per entrambi i sensi e abbiamo verificato se ci fosse un'intersezione, in caso contrario significava che l'antenato comune non fosse a quel livello di iperonimia. Quindi abbiamo proceduto a ripetere la verifica sull'intersezione tra le liste di iperonimi estendendole con i livelli via via superiori fino a trovare un'intersezione. Per calcolare poi la profondità di questo antenato abbiamo calcolato la distanza tra il root degli iperonimi e l'iperonimo trovato, implementandolo in *get_depth(s)*, che poi abbiamo usato per trovare anche "depth(s1)" e "depth(s2)".


# Shortest Path

Per calcolare "len(s1,s2)" abbiamo pensato che il cammino minimo tra i due sensi fosse quello che passa dal primo antenato in comune. Abbiamo quindi calcolato quest'ultimo con l'ausilio del metodo *lcs(s1,s2)* utilizzato anche per calcolare la similarità di Wu & Palmer. In assenza di un antenato comune abbiamo considerato la distanza come massima, quindi 2*depthMax, altrimenti, abbiamo restituito la somma tra la distanza tra s1 e l'antenato comune e la distanza tra s2 e l'antenato comune.

# Leacock & Chodorow

Abbiamo utilizzato i metodi precedentemente descritti per implementare la formula di similarità.

# Correlazioni di Spearman e Pearson

Abbiamo utilizzato il metodo *Pandas.DataFrame.corr(serie, method)* per calcolare entrambi le correlazioni, cambiando il parametro "method".

# Risultati

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


### Consegna 2

# Implementazione di Lesk 

Abbiamo tradotto lo pseudo-codice di Lesk fornitoci, per costruire il contesto abbiamo pulito la frase, gli esempi e la definizione dalle stop words con *stem_lem(text)*.

# Disambiguazione utilizzando Lesk

