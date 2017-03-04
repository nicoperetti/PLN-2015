PLN 2015: Práctico 4
================================================

Para entrenar:

python tagging/scripts/train.py -o file

python tagging/scripts/split_data.py -o file

python tagging/scripts/train_nn.py

file: Output model file (Lexicon).


Para evaluar:

python tagging/scripts/eval_nn.py -i file

file: modelo ya entrenado (Lexicon)


Resultados:

Accuracy: 94.01%

Accuracy sobre palabras conocidas: 96.18%

Accuracy sobre palabras desconocidas: 52.85%

Matriz de confusión(Error Analysis):

|        | aq  | np  |  nc  | vm  | rg | cs | da | sp | nu | pr |
|--------|-----|-----|------|-----|----|----|----|----|----|----|
| **aq** |     | 1.8 |  9.3 | 7.9 |0.1 |    |    |    |    |    |
| **np** | 3.3 |     |  9.8 | 3.8 |    |    |    | 0.1|    |    |
| **nc** | 6.2 | 2.0 |      | 4.5 |0.2 |    | 0.1|    |    |    |
| **vm** | 4.4 | 0.9 |  4.7 |     | 0.2|    |    | 0.1|    |    |
| **rg** | 1.4 | 0.2 |  1.8 | 0.9 |    |    |    | 0.5|    |    |
| **cs** |     |     |      | 0.3 | 0.1|    |    | 0.6|    | 4.8|
| **da** | 0.2 | 1.1 |  2.1 | 0.3 |    |    |    |    | 0.2|    |
| **sp** | 0.3 |     |  0.3 | 1.8 | 0.2| 0.2|    |    |    |    |
| **nu** | 0.2 | 0.5 |  0.7 | 0.6 |    |    | 0.2|    |    |    |
| **pr** |     |     |      |     |    | 2.4|    |    |    |    |



Nota: en la matriz de confusión se tomaron los tags con mayor error, y cada i,j en
la matriz representa el porcentaje de haber elegido erroneamete j en vez de i.
