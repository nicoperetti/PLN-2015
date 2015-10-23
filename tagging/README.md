PLN 2015: Práctico 2
================================================


Ejercicio 1
-----------

Este ejercicio consistía en sacar estadísticas sobre el corpus.

Estadísticas básicas:

Cantidad de oraciones:    17379  
Cantidad de ocurrencias:  517268 
Vocabulario:              46482  
Vocabulario de tags:      48     

Etiquetas más frecuentes:

| tag | significado del tag    | frecuencia | %     | cinco palabras más frecuentes                         |
|-----|------------------------|------------|-------|-------------------------------------------------------|
| nc  | Nombre Común           |   92002    | 17.78 | 'años', 'presidente', 'millones', 'equipo', 'partido' |
| sp  | Adposición Preposición |   79904    | 15.44 | 'de', 'en', 'a', 'del', 'con'                         |
| da  | Determinante Artículo  |   54552    | 10.54 | 'la', 'el', 'los', 'las', 'El'                        |
| vm  | Verbo Principal        |   50609    | 9.78  | 'está', 'tiene', 'dijo', 'puede', 'hace'              |
| aq  | Adjetivo Calificativo  |   33904    | 6.55  | 'pasado', 'gran', 'mayor', 'nuevo', 'próximo'         |
| fc  | Puntuación             |   30148    | 5.82  | ','                                                   |
| np  | Nombre Propio          |   29113    | 5.62  | 'Gobierno', 'España', 'PP', 'Barcelona', 'Madrid'     |
| fp  | Puntuación             |   21157    | 4.09  | '.', '(', ')'                                         |
| rg  | Adverbio general       |   15333    | 2.96  | 'más', 'hoy', 'también', 'ayer', 'ya'                 |
| cc  | Conjunción Coordinada  |   15023    | 2.90  | 'y', 'pero', 'o', 'Pero', 'e'                         |

Niveles de ambiguedad:

| nivel de ambiguedad | cantidad de palabras | %     |
|---------------------|----------------------|-------|
|       1             |     44109            | 94.89 |
|       2             |     2194             | 4.720 |
|       3             |     153              | 0.329 |
|       4             |     19               | 0.040 |
|       5             |     4                | 0.008 |
|       6             |     3                | 0.006 |
|       7             |     0                | 0.0   |
|       8             |     0                | 0.0   |
|       9             |     0                | 0.0   |



Ejercicio 2
-----------
Implementación de Baseline Tagger, donde para cada palabra elije el tag más frecuente observado
en el entrenamiento y si la palabra es desconocida devuelvo la etiqueta más frecuente.


Ejercicio 3
-----------

Se programo un scripts train.py que permite entrenar el Baseline Tagger del
ejercicio anterior y también se programo un script eval.py que evalúa el modelo
entrenado, calculando accuracy en general, osea cuantas etiquetas se etiquetaron
bien, y también se evalúa accuracy sobre las palabras conocidas y las no conocidas.

Para entrenar:

python3 tagging/scripts/train.py -m model -n n -o file


model: Model to use base, addone, memm.
n: Order of the model,only if the model is not base.
file: Output model file.

Para evaluar:

python3 tagging/scripts/eval.py -i file

file: modelo ya entrenado


Para el modelo baseline se obtuvieron los siguientes resultados:

Accuracy: 89.02%

Accuracy sobre palabras conocidas: 95.34%

Accuracy sobre palabras desconocidas: 31.80%

Matriz de confusión(Error Analysis):

|        | di  | vm  | nc   | aq  | cc | rn | dn | rg | vs | pi | pr   | p0 | da  | cs | pp |
|--------|-----|-----|------|-----|----|----|----|----|----|----|------|----|-----|----|----|
| **aq** | .2  | 2.0 | 20.0 |     |    |    |    |    |    |    |      |    |     |    |    |
| **rg** |     |     | 2.8  | .2  | .2 | .2 |    |    |    |    |      |    |     |    |    |
| **pn** |     |     |      |     |    |    | .5 |    |    |    |      |    |     |    |    |
| **pi** | 2.6 |     |      |     |    |    |    |    |    |    |      |    |     |    |    |
| **nc** |     | .8  |      | 3.7 |    |    |    | .3 | .2 |    |      |    |     |    |    |
| **di** |     |     |      | .2  |    |    |    | .2 |    | .2 |      |    |     |    |    |
| **cs** |     |     | .2   |     |    |    |    |    |    |    | 11.2 |    |     |    |    |
| **np** |     |     | 18.6 |     |    |    |    |    |    |    |      |    |     |    |    |
| **vm** |     |     | 20.3 | 1.3 |    |    |    |    |    |    |      |    |     |    |    |
| **pp** |     |     |      |     |    |    |    | .2 |    |    |      | .5 | 2.4 |    |    |
| **sp** |     |     | .4   |     |    |    |    |    |    |    |      |    |     | .4 |    |
| **cc** |     |     |      |     |    |    |    | .4 |    |    |      |    |     |    |    |
| **dn** | .2  |     |      |     |    |    |    |    |    |    |      |    |     |    |    |
| **zp** |     |     | .5   |     |    |    |    |    |    |    |      |    |     |    |    |
| **da** |     |     | 1.3  |     |    |    |    |    |    |    |      |    |     |    |    |
| **nu** |     |     | 1.4  |     |    |    |    |    |    |    |      |    |     |    |    |
| **un** |     |     | .3   |     |    |    |    |    |    |    |      |    |     |    |    |
| **p0** |     |     |      |     |    |    |    |    |    |    |      |    |     |    | .3 |

Nota: en la matriz de confusión se omitieron los tags con error menor al 2% por motivo de espacio.

Ejercicio 4
-----------


Ejercicio 5
-----------

n=1

Accuracy: 89.01%

Accuracy sobre palabras conocidas: 95.32%

Accuracy sobre palabras desconocidas: 31.80%

Matriz de Confusion

|       | vm  | aq  | np   | cs   |   nc |  rg  | pp   |  pi  |  nu  | da   |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**vm** |     | 1.6 |      |      | 20.2 |      |      |      |      |      |
|**aq** | 1.7 |     |      |      | 19.5 |      |      |      |      |      |
|**np** |     |     |      |      | 18.5 |      |      |      |      |      |
|**cs** |     |     |      |      |  0.2 |      |      |      |      |      |
|**nc** | 0.8 | 4.5 |      |      |      |  0.3 |      |      |      |      |
|**rg** |     | 0.2 |      |  0.1 |  2.8 |      |      |  0.1 |      |      |
|**pp** |     |     |      |      |      |  0.2 |      |      |      |  2.4 |
|**pi** |     |     |      |      |      |  0.1 |      |      |      |      |
|**nu** |     |     |      |      |  1.4 |      |      |      |      |      |
|**da** |     |     |      |      |  1.4 |      |      |      |      |      |

n=2

Accuracy: 92.72%

Accuracy sobre palabras conocidas: 97.61%

Accuracy sobre palabras desconocidas: 48.42%

Matriz de Confusion

|       | nc  | aq  |   vm |   np |   rg |   cs |   da |  nu  |  pr  |   pp |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**nc** |     | 4.9 |  2.5 |  6.8 |  0.6 |      |  2.4 |      |  0.1 |      |
|**aq** | 6.0 |     |  4.3 |  2.1 |  0.7 |      |  1.4 |      |  0.3 |      |
|**vm** | 2.8 | 2.8 |      |  1.7 |  0.8 |      |  1.2 |      |  0.1 |      |
|**np** | 6.8 | 2.1 |  1.3 |      |  0.3 |      |  0.5 |      |  0.6 |      |
|**rg** | 0.4 | 0.7 |  0.6 |  0.9 |      |      |  0.3 |      |      |      |
|**cs** |     |     |      |      |      |      |      |      |  3.8 |      |
|**da** | 1.0 |     |  0.1 |  0.5 |      |      |      |      |      |  0.3 |
|**nu** | 0.2 |     |  0.1 |  0.4 |      |      |  0.7 |      |      |      |
|**pr** |     |     |      |      |      |  1.6 |      |      |      |      |
|**pp** |     |     |      |      |  0.2 |      |  0.4 |      |      |      |

n =3

Accuracy: 93.17%

Accuracy sobre palabras conocidas: 97.67%

Accuracy sobre palabras desconocidas: 52.31%

Matriz de Confusion

|       | aq  |  nc |   vm |   np |   rg |   cs |   da |  pr  |  nu  |   pp |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** | 0.0 | 6.7 |  3.6 |  1.1 |  0.8 |  0.0 |  1.0 |  0.6 |  0.0 |  0.0 |
|**nc** | 5.2 | 0.0 |  2.2 |  4.6 |  0.6 |  0.0 |  2.4 |  0.3 |  0.1 |  0.0 |
|**vm** | 3.0 | 3.7 |  0.0 |  1.1 |  0.9 |  0.1 |  1.1 |  0.1 |  0.0 |  0.0 |
|**np** | 2.0 | 8.7 |  1.1 |  0.0 |  0.8 |  0.1 |  0.5 |  0.8 |  0.1 |  0.1 |
|**rg** | 0.6 | 0.6 |  0.3 |  0.4 |  0.0 |  0.0 |  0.3 |  0.0 |  0.0 |  0.0 |
|**cs** | 0.0 | 0.0 |  0.0 |  0.0 |  0.1 |  0.0 |  0.0 |  2.7 |  0.0 |  0.0 |
|**da** | 0.0 | 1.2 |  0.1 |  0.4 |  0.0 |  0.0 |  0.0 |  0.0 |  0.1 |  0.5 |
|**pr** | 0.0 | 0.0 |  0.0 |  0.0 |  0.0 |  2.1 |  0.0 |  0.0 |  0.0 |  0.0 |
|**nu** | 0.2 | 0.3 |  0.0 |  0.3 |  0.0 |  0.0 |  0.7 |  0.0 |  0.0 |  0.0 |
|**pp** | 0.0 | 0.0 |  0.0 |  0.0 |  0.1 |  0.0 |  0.5 |  0.0 |  0.0 |  0.0 |


n = 4

Accuracy: 93.14%

Accuracy sobre palabras conocidas: 97.44%

Accuracy sobre palabras desconocidas: 54.14%

Matriz de Confusion

|       | aq  | nc  |   vm |   np |   rg |   cs |   da |  pr  |  pp  |  di  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     | 7.0 |  3.9 |  0.9 |  0.9 |      |  1.0 |  0.4 |      |  0.1 |
|**nc** | 5.3 |     |  1.8 |  4.3 |  0.5 |      |  2.1 |  0.3 |      |      |
|**vm** | 2.8 | 3.7 |      |  1.0 |  0.9 | 0.2  |  1.1 |      |      |  0.1 |
|**np** | 1.9 | 7.9 |  1.3 |      |  0.6 | 0.2  |  0.6 |  0.6 |      |      |
|**rg** | 0.7 | 0.6 |  0.3 |  0.4 |      |      |  0.4 |      |      |      |
|**cs** |     |     |      |      |  0.1 |      |      |  3.2 |      |      |
|**da** |     | 1.1 |  0.1 |  0.5 |      |      |      |      |  0.4 |      |
|**pr** |     |     |      |      |      |  2.2 |      |      |      |      |
|**pp** |     |     |      |      |  0.1 |      |  0.6 |      |      |      |
|**di** | 1.1 |     |      |      |      |      |      |      |      |      |


Ejercicio 6
-----------


Ejercicio 7
-----------

Clasificador LogisticRegression

n = 1

Accuracy: 92.70%

Accuracy sobre palabras conocidas: 95.28%

Accuracy sobre palabras desconocidas: 69.32%

Matriz de Confusion

|       | aq  | nc  |   vm |   rg |   cs |   np |   pp |  pi  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     | 9.7 |  7.8 |      |      |  0.6 |      |      |      |      |
|**nc** | 7.7 |     |  7.1 |  0.2 |      |  1.6 |      |      |      |  0.3 |
|**vm** | 7.1 | 5.6 |      |      |      |  2.4 |      |      |      |  0.1 |
|**rg** | 4.2 | 0.6 |  2.9 |      |  0.1 |  0.4 |      |  0.2 |      |      |
|**cs** | 0.2 |     |  0.4 |  0.1 |      |      |      |      |      |      |
|**np** | 0.3 | 3.4 |  1.2 |      |      |      |      |      |      |      |
|**pp** |     |     |      |  0.3 |      |      |      |      |  2.4 |      |
|**pi** |     |     |      |  0.1 |      |      |      |      |      |      |
|**da** |     | 1.7 |      |      |      |      |  0.2 |      |      |  0.9 |
|**nu** | 0.4 | 1.2 |  0.4 |      |      |      |      |      |      |      |

n=2

Accuracy: 91.99%

Accuracysobre palabras conocidas: 94.55%

Accuracy sobre palabras desconocidas: 68.75%

Matriz de Confusion

|       | aq  | nc  |   vm |   rg |   cs |   np |   pi |  pp  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     |12.0 |  7.0 |      |      |  0.5 |      |      |      |      |
|**nc** | 9.3 |     |  7.1 |  0.1 |      |  1.5 |      |      |      |  0.2 |
|**vm** | 7.4 | 7.0 |      |      |      |  2.2 |      |      |      |  0.1 |
|**rg** | 2.3 | 2.1 |  2.6 |      |  0.1 |  0.4 |  0.2 |      |      |      |
|**cs** | 0.1 | 0.1 |  0.4 |      |      |      |      |      |      |      |
|**np** | 0.2 | 3.2 |  1.1 |      |      |      |      |      |      |      |
|**pi** | 0.1 |     |      |  0.1 |      |      |      |      |      |      |
|**pp** |     | 0.1 |      |  0.3 |      |      |      |      |  2.0 |      |
|**da** |     | 1.5 |      |      |      |      |      |  0.4 |      |  0.8 |
|**nu** | 0.2 | 1.3 |  0.4 |      |      |      |      |      |      |      |


n=3

Accuracy: 92.18%

Accuracy_known: 94.72%

Accuracy_unknown: 69.20%

Matriz de Confusion

|       | aq  | nc  |   vm |   rg |   np | cs   |   pi |  pp  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     |11.7 |  7.0 |      |  0.5 |      |      |      |      |      |
|**nc** | 9.3 |     |  6.8 |  0.1 |  1.5 |      |      |      |      |  0.1 |
|**vm** | 7.1 | 7.0 |      |      |  2.2 |      |      |      |      |      |
|**rg** | 2.4 | 1.5 |  3.4 |      |  0.4 |  0.1 |  0.2 |      |      |      |
|**np** | 0.2 | 3.4 |  1.0 |      |      |      |      |      |      |      |
|**cs** | 0.1 | 0.1 |  0.4 |      |      |      |      |      |      |      |
|**pi** |     |     |      |  0.1 |      |      |      |      |      |      |
|**pp** |     | 0.1 |      |  0.3 |      |      |      |      |  2.0 |      |
|**da** |     | 1.6 |      |      |      |      |      |  0.4 |      |  0.9 |
|**nu** | 0.2 | 1.2 |  0.5 |      |      |      |      |      |      |      |


n=4

Accuracy: 92.23%

Accuracy_known: 94.72%

Accuracy_unknown: 69.62%

Matriz de Confusion

|       | aq  | nc  |   vm |   rg |   np | cs   |   pi |  pp  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     |11.9 |  6.7 |      |  0.5 |      |      |      |      |      |
|**nc** | 9.5 |     |  6.0 |  0.1 |  1.5 |      |      |      |      |  0.1 |
|**vm** | 7.3 | 7.5 |      |      |  2.3 |      |      |      |      |      |
|**rg** | 2.6 | 1.6 |  3.3 |      |  0.4 |  0.1 |  0.2 |      |      |      |
|**np** | 0.2 | 3.5 |  1.0 |      |      |      |      |      |      |      |
|**cs** | 0.1 | 0.1 |  0.4 |      |      |      |      |      |      |      |
|**pi** |     |     |      |  0.1 |      |      |      |      |      |      |
|**pp** |     | 0.1 |      |  0.3 |      |      |      |      |  2.0 |      |
|**da** |     | 1.6 |      |      |      |      |      |  0.4 |      |  0.9 |
|**nu** | 0.2 | 1.3 |  0.5 |      |      |      |      |      |      |      |


Clasificador LinearSVC

n=1

Accuracy: 94.43%

Accuracy_known: 97.04%

Accuracy_unknown: 70.82%

Matriz de Confusion

|       | aq  | nc  |   vm |   rg |   np | cs   |   pi |  pp  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     |11.9 |  6.7 |      |  0.5 |      |      |      |      |      |
|**nc** | 9.5 |     |  6.0 |  0.1 |  1.5 |      |      |      |      |  0.1 |
|**vm** | 7.3 | 7.5 |      |      |  2.3 |      |      |      |      |      |
|**rg** | 2.6 | 1.6 |  3.3 |      |  0.4 |  0.1 |  0.2 |      |      |      |
|**np** | 0.2 | 3.5 |  1.0 |      |      |      |      |      |      |      |
|**cs** | 0.1 | 0.1 |  0.4 |      |      |      |      |      |      |      |
|**pi** |     |     |      |  0.1 |      |      |      |      |      |      |
|**pp** |     | 0.1 |      |  0.3 |      |      |      |      |  2.0 |      |
|**da** |     | 1.6 |      |      |      |      |      |  0.4 |      |  0.9 |
|**nu** | 0.2 | 1.3 |  0.5 |      |      |      |      |      |      |      |


           aq    nc    vm    cs    rg    np    pp    pi    da    nu     

    aq    0.0   9.9   7.3   0.0   0.1   0.6   0.0   0.0   0.0   0.0
    nc    7.3   0.0   6.2   0.0   0.3   2.1   0.0   0.0   0.0   0.0
    vm    6.9   4.7   0.0   0.0   0.0   2.0   0.0   0.0   0.0   0.0
    cs    0.1   0.1   0.3   0.0   0.1   0.0   0.0   0.0   0.0   0.0
    rg    2.8   0.7   1.3   0.2   0.0   0.0   0.0   0.3   0.0   0.0
    np    0.3   4.6   1.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0
    pp    0.0   0.0   0.0   0.0   0.4   0.0   0.0   0.0   3.6   0.0
    pi    0.0   0.0   0.0   0.0   0.2   0.0   0.0   0.0   0.0   0.0
    da    0.0   1.6   0.0   0.0   0.0   0.0   0.1   0.0   0.0   1.0
    nu    0.2   1.7   0.3   0.0   0.0   0.0   0.0   0.0   0.0   0.0

n=2

Accuracy: 94.29%

Accuracy_known: 96.91%

Accuracy_unknown: 70.57%
       aq    nc    vm    rg    np    cs    pi    pp    da    nu     

aq    0.0   10.8   6.9   0.1   0.6   0.0   0.0   0.0   0.0   0.0
nc    8.8   0.0   6.3   0.2   2.0   0.0   0.0   0.0   0.0   0.0
vm    6.6   6.3   0.0   0.0   2.0   0.0   0.0   0.0   0.0   0.0
rg    1.7   1.8   1.3   0.0   0.0   0.2   0.2   0.0   0.0   0.0
np    0.3   4.5   1.0   0.0   0.0   0.0   0.0   0.0   0.0   0.0
cs    0.0   0.1   0.2   0.1   0.0   0.0   0.0   0.0   0.0   0.0
pi    0.1   0.0   0.0   0.2   0.0   0.0   0.0   0.0   0.0   0.0
pp    0.0   0.0   0.0   0.3   0.0   0.0   0.0   0.0   2.9   0.0
da    0.0   1.5   0.0   0.0   0.0   0.0   0.0   0.3   0.0   1.0
nu    0.1   1.8   0.3   0.0   0.0   0.0   0.0   0.0   0.0   0.0

n=3

Accuracy: 94.40%

Accuracysobre palabras conocidas: 96.94%

Accuracy sobre palabras desconocidas: 71.38%

       aq    nc    vm    rg    np    cs    pi    pp    da    nu     

aq    0.0   10.7   6.5   0.1   0.6   0.0   0.0   0.0   0.0   0.0
nc    9.2   0.0   6.0   0.2   1.9   0.0   0.0   0.0   0.0   0.0
vm    6.9   6.0   0.0   0.0   2.1   0.0   0.0   0.0   0.0   0.0
rg    1.8   1.4   1.7   0.0   0.0   0.2   0.3   0.0   0.0   0.0
np    0.3   4.5   1.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0
cs    0.1   0.1   0.3   0.0   0.0   0.0   0.0   0.0   0.0   0.0
pi    0.0   0.0   0.0   0.2   0.0   0.0   0.0   0.0   0.0   0.0
pp    0.0   0.0   0.0   0.4   0.0   0.0   0.0   0.0   2.9   0.0
da    0.0   1.6   0.0   0.0   0.0   0.0   0.0   0.4   0.0   1.0
nu    0.1   1.7   0.4   0.0   0.0   0.0   0.0   0.0   0.0   0.0

n=4

Accuracy: 94.46%

Accuracy sobre palabras conocidas: 96.96%

Accuracy sobre palabras desconocidas: 71.81%
       aq    nc    vm    rg    np    cs    pi    pp    da    nu     

aq    0.0   11.0   6.5   0.1   0.6   0.0   0.0   0.0   0.0   0.0
nc    9.3   0.0   5.2   0.2   2.0   0.0   0.0   0.0   0.0   0.0
vm    6.7   6.6   0.0   0.0   2.1   0.0   0.0   0.0   0.0   0.0
rg    1.8   1.4   1.8   0.0   0.0   0.2   0.3   0.0   0.0   0.0
np    0.3   4.6   1.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0
cs    0.0   0.1   0.3   0.0   0.0   0.0   0.0   0.0   0.0   0.0
pi    0.0   0.0   0.0   0.2   0.0   0.0   0.0   0.0   0.0   0.0
pp    0.0   0.0   0.0   0.4   0.0   0.0   0.0   0.0   2.9   0.0
da    0.0   1.6   0.0   0.0   0.0   0.0   0.0   0.5   0.0   1.0
nu    0.1   1.7   0.4   0.0   0.0   0.0   0.0   0.0   0.0   0.0

Clasificador MultinomialNB

n=1

Accuracy: 82.18%

Accuracy_known: 85.85%

Accuracy_unknown: 48.89%
       aq    vm    rg    pp    np    nc    fg    pr    dd    pi     

aq    0.0   1.7   0.0   0.0   0.1   7.8   0.0   0.0   0.0   0.0
vm    0.4   0.0   0.0   0.0   0.1   2.8   0.0   0.0   0.0   0.0
rg    0.6   0.9   0.0   0.0   0.0   1.5   0.0   0.0   0.0   0.0
pp    0.0   1.8   0.0   0.0   0.1   0.5   0.0   0.0   0.0   0.0
np    0.0   0.1   0.0   0.0   0.0   2.0   0.0   0.0   0.0   0.0
nc    0.4   0.5   0.0   0.0   0.6   0.0   0.0   0.0   0.0   0.0
fg    0.2   0.3   0.0   0.0   0.0   1.5   0.0   0.0   0.0   0.0
pr    0.0   0.0   0.0   0.0   0.0   0.2   0.0   0.0   0.0   0.0
dd    0.0   0.3   0.0   0.0   0.1   1.4   0.0   0.0   0.0   0.0
pi    0.0   0.3   0.1   0.0   0.0   0.6   0.0   0.0   0.0   0.0

n=2
Accuracy: 76.46%

Accuracy_known: 80.41%

Accuracy_unknown: 40.68%
       aq    vm    nc    rg    np    pp    fg    vs    cs    cc     

aq    0.0   1.6   4.9   0.0   0.0   0.0   0.0   0.0   0.0   0.0
vm    0.7   0.0   2.3   0.0   0.1   0.0   0.0   0.0   0.0   0.0
nc    0.8   1.2   0.0   0.0   0.5   0.0   0.0   0.0   0.0   0.0
rg    0.5   0.9   1.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0
np    0.0   0.1   1.4   0.0   0.0   0.0   0.0   0.0   0.0   0.0
pp    0.0   1.4   0.2   0.0   0.0   0.0   0.0   0.0   0.0   0.0
fg    0.1   0.2   1.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0
vs    0.1   1.4   0.6   0.0   0.0   0.0   0.0   0.0   0.0   0.0
cs    0.0   0.1   0.1   0.0   0.0   0.0   0.0   0.0   0.0   0.0
cc    0.0   0.0   0.2   0.2   0.4   0.0   0.0   0.0   0.0   0.0


n=3
Accuracy: 71.47%

Accuracy_known: 75.09%

Accuracy_unknown: 38.59%
       aq    vm    nc    rg    np    vs    fg    pp    cs    sp     

aq    0.0   1.3   4.6   0.0   0.0   0.0   0.0   0.0   0.0   4.7
vm    1.0   0.0   2.8   0.0   0.1   0.0   0.0   0.0   0.0   4.0
nc    1.8   1.2   0.0   0.0   0.4   0.0   0.0   0.0   0.0   4.0
rg    0.8   0.8   1.2   0.0   0.0   0.0   0.0   0.0   0.0   1.8
np    0.0   0.2   1.4   0.0   0.0   0.0   0.0   0.0   0.0   1.1
vs    0.3   1.3   0.5   0.0   0.0   0.0   0.0   0.0   0.0   1.1
fg    0.2   0.1   0.9   0.0   0.0   0.0   0.0   0.0   0.0   1.0
pp    0.1   1.0   0.3   0.0   0.1   0.0   0.0   0.0   0.0   0.4
cs    0.0   0.1   0.2   0.0   0.0   0.0   0.0   0.0   0.0   0.7
sp    0.0   0.1   0.5   0.0   0.1   0.0   0.0   0.0   0.1   0.0

n=4

Accuracy: 68.20%

Accuracy_known: 71.31%

Accuracy_unknown: 40.01%
       vm    aq    nc    rg    np    vs    cs    fg    pp    di     

vm    0.0   1.4   3.1   0.0   0.2   0.0   0.0   0.0   0.0   0.0
aq    0.8   0.0   4.1   0.0   0.1   0.0   0.0   0.0   0.0   0.0
nc    0.9   2.5   0.0   0.0   0.6   0.0   0.0   0.0   0.0   0.0
rg    0.8   1.1   1.2   0.0   0.1   0.0   0.0   0.0   0.0   0.0
np    0.2   0.0   1.3   0.0   0.0   0.0   0.0   0.0   0.0   0.0
vs    1.1   0.5   0.5   0.0   0.1   0.0   0.0   0.0   0.0   0.0
cs    0.1   0.1   0.4   0.0   0.0   0.0   0.0   0.0   0.0   0.0
fg    0.1   0.4   0.8   0.0   0.1   0.0   0.0   0.0   0.0   0.0
pp    0.7   0.2   0.3   0.0   0.1   0.0   0.0   0.0   0.0   0.0
di    0.2   0.4   1.1   0.0   0.1   0.0   0.0   0.0   0.0   0.0
