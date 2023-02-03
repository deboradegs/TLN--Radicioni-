### Esercitazione Semantic Evaluation

## Consegna 1

# Annotazione e valutazione

Abbiamo estratto le coppie di termini utilizzando il cognome Chierchiello, qui di seguito riportiamo gli agreement tra le nostre annotazioni.

```
Agreement between annotations
Pearson coefficient:  0.8097492411122477
Spearman coefficient:  0.8093217601655284

```
Abbiamo in seguito calcolato tramite massimizzazione della cosine similarity la somiglianza tra le coppie di parole. Per farlo abbiamo estratto l'elenco di babelnetID associati ad ogni termine della coppia da confrontare (dal file *"SemEval17_IT_senses2synsets.txt"*); abbiamo preso i vettori di Nasari per ogni babelnetID disponibile e abbiamo preso la massima cosine similarity tra tutte le combinazioni di vettori così trovati.
Abbiamo confrontato il risultato con la media delle nostre annotazioni. Qui di seguito riportiamo i coefficienti di correlazione.

```
Correlation between human and machine
Pearson coefficient:  0.8219260058924709
Spearman coefficient:  0.8330601814907646

```

## Consegna 2

# Annotazione e Valutazione

Abbiamo annotato i sensi coerentemente rispetto ai valori di similarità precendentemente dati alle coppie di termini. Ne abbiamo calcolato poi l'agreement tramite la Kappa di Cohen. Di seguito la media tra gli agreement delle coppie di annotatori.

```
Agreement between annotations with Cohen similarity:
Cohen similarity:  0.8116896512591011

```

Abbiamo poi valutato l'accuratezza delle nostre annotazioni trovando la coppia di babelnetID che massimizzasse la similarità, semplicemente salvando e riportando la coppia che corrispondeva a massima cosine similarity nella *Consegna 1*.
La valutazione è stata fatta sia sui singoli significati per ogni annotatore che sulle coppie di significati per ogni annotatore.

```

Accuracy for single word (Chierchiello): 0.45
Accuracy for single word (Damonte): 0.46
Accuracy for single word (De Gaetano): 0.43

Accuracy for pair word (Chierchiello): 0.24
Accuracy for pair word (Damonte): 0.2
Accuracy for pair word (De Gaetano): 0.2

```
