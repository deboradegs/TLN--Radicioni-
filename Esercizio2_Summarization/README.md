# TLN--ESERCITAZIONE SUMMARIZATION-

## Individuazione del topic e creazione del contesto

Abbiamo creato il topic del testo prendendo i vettori di Nasari delle parole presenti nel titolo, nel paragrafo introduttivo e in quello conclusivo.

## Individuazione e riordinamento dei paragrafi contenenti i termini più rilevanti

Per ogni parola di ogni paragrafo abbiamo calcolato la weighted overlap rispetto al contesto, trovando così i paragrafi con maggiore overlap col contesto, per permetterci di riordinarli per rilevanza. 
Per ogni parola del paragrafo abbiamo contato solo l'overlap con la parola del contesto che avesse massimo valore. 
Per trovare la rilevanza del paragrafo abbiamo sommato tutti gli overlap così trovati per le sue parole.

## Summarization

Partendo dall'elenco di paragrafi riordinati per rilevanza abbiamo riscritto il testo prendendo il numero di paragrafi tale per cui il numero di parole del riassunto si avvicinasse maggiormente al numero di parole del testo compresso della percentuale richiesta.

## Risultati

Abbiamo calcolato la BLUE precision e la ROUGE recall per ogni documento riassunto implementando le formule e usando come golden summary i riassunti ottenuti da https://resoomer.com/en.
Per calcolare precision e recall del summarizer in generale abbiamo prima fatto la media delle precision e delle recall prima trovate e poi, come confronto, abbiamo utilizzato la classe PerlRouge di rouge_metric, calcolando lo score sia sul confronto di singole parole che di coppie di parole.

```
Evaluation on the summary of document Life-indoors.txt

BLUE precision of 10% compression
0.9587155963302753
ROUGE recall of 10% compression
0.9330357142857143

BLUE precision of 20% compression
0.851063829787234
ROUGE recall of 20% compression
0.8080808080808081

BLUE precision of 30% compression
0.8085106382978723
ROUGE recall of 30% compression
0.8685714285714285



Evaluation on the summary of document Ebola-virus-disease.txt

BLUE precision of 10% compression
0.9753954305799648
ROUGE recall of 10% compression
0.8781645569620253

BLUE precision of 20% compression
0.7936210131332082
ROUGE recall of 20% compression
0.789179104477612

BLUE precision of 30% compression
0.6923076923076923
ROUGE recall of 30% compression
0.7801268498942917



Evaluation on the summary of document Trump-wall.txt

BLUE precision of 10% compression
0.7173678532901834
ROUGE recall of 10% compression
0.9059945504087193

BLUE precision of 20% compression
0.6461716937354989
ROUGE recall of 20% compression
0.889776357827476

BLUE precision of 30% compression
0.5765661252900232
ROUGE recall of 30% compression
0.8922800718132855



Evaluation on the summary of document Andy-Warhol.txt

BLUE precision of 10% compression
0.9009009009009009
ROUGE recall of 10% compression
0.9237875288683602

BLUE precision of 20% compression
0.7487684729064039
ROUGE recall of 20% compression
0.8539325842696629

BLUE precision of 30% compression
0.6896551724137931
ROUGE recall of 30% compression
0.8433734939759037



Evaluation on the summary of document Napoleon-wiki.txt

BLUE precision of 10% compression
0.9944903581267218
ROUGE recall of 10% compression
0.9328165374677002

BLUE precision of 20% compression
0.7654320987654321
ROUGE recall of 20% compression
0.835016835016835

BLUE precision of 30% compression
0.7006172839506173
ROUGE recall of 30% compression
0.8438661710037175



Average Evaluation on all documents

Average BLUE precision: 0.7879722773210549

Average ROUGE recall: 0.8652001728615694


Using Rouge Metric library: 

Rouge-1 scores
Recall score: 0.87839
Precision score: 0.80557

Rouge-2 scores
Recall score: 0.81142
Precision score: 0.7472
```

