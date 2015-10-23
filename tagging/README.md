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
También cuando corremos el script eval.py vamos a obserbar que la matriz de confusión
se grafica como un mapa de calor.

Para entrenar:

python3 tagging/scripts/train.py -m model -n n -c clf -o file


model: modelo a utilizar base, addone, memm.
n: orden del modelo, solo si model no es base.
c: clasificador a utilizar si el modelo es memm, puede ser LR, LSVC, MNB
file: Output model file.

Para evaluar:

python3 tagging/scripts/eval.py -i file

file: modelo ya entrenado


Para el modelo baseline se obtuvieron los siguientes resultados:

Accuracy: 89.03%

Accuracy sobre palabras conocidas: 95.35%

Accuracy sobre palabras desconocidas: 31.80%

Matriz de confusión(Error Analysis):

|        | aq  | vm  |  np  | cs  | nc | rg | pp | pi | nu | da |
|--------|-----|-----|------|-----|----|----|----|----|----|----|
| **aq** |     | 2.0 |      |     |19.9|    |    |    |    |    |
| **vm** | 1.3 |     |      |     |20.2|    |    |    |    |    |
| **np** |     |     |      |     |18.6|    |    |    |    |    |
| **cs** |     |     |      |     | 0.2|    |    |    |    |    |
| **nc** | 3.7 | 0.8 |      |     |    | 0.3|    |    |    |    |
| **rg** | 0.2 |     |      |     | 2.8|    |    | 0.1|    |    |
| **pp** |     |     |      |     |    | 0.2|    |    |    | 2.4|
| **pi** |     |     |      |     |    | 0.1|    |    |    |    |
| **nu** |     |     |      |     | 1.4|    |    |    |    |    |
| **da** |     |     |      |     | 1.3|    |    |    |    |    |

Tiempo de evaluación:

real-0m4.869s
user-0m4.682s
sys-0m0.136s


Nota: en la matriz de confusión se tomaron los tags con mayor error, y cada i,j en
la matriz representa el porcentaje de haber elegido erroneamete j en vez de i.


Ejercicio 4
-----------

Se implemento un Hidden Markov Model en la clase HMM de hmm.py.
Se implemento el algoritmo de Viterbi que calcula el etiquetado más probable de una oración.

Ejercicio 5
-----------

Se implemento la clase clase MLHMM en hmm.py. Cuyos parámetros se estiman usando
Maximum Likelihood sobre un corpus de oraciones con sus etiquetas. Los resultados
son los siguientes para n = 1,2,3,4:

n = 1

Accuracy: 89.01%

Accuracy sobre palabras conocidas: 95.32%

Accuracy sobre palabras desconocidas: 31.80%

Matriz de Confusión

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

Tiempo de evaluación:

real-0m16.209s
user-0m15.930s
sys-0m0.172s


n = 2

Accuracy: 92.72%

Accuracy sobre palabras conocidas: 97.61%

Accuracy sobre palabras desconocidas: 48.42%

Matriz de Confusión

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

Tiempo de evaluación:

real-0m29.936s
user-0m29.712s
sys-0m0.148s

n = 3

Accuracy: 93.17%

Accuracy sobre palabras conocidas: 97.67%

Accuracy sobre palabras desconocidas: 52.31%

Matriz de Confusión

|       | aq  |  nc |   vm |   np |   rg |   cs |   da |  pr  |  nu  |   pp |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     | 6.7 |  3.6 |  1.1 |  0.8 |      |  1.0 |  0.6 |      |      |
|**nc** | 5.2 |     |  2.2 |  4.6 |  0.6 |      |  2.4 |  0.3 |  0.1 |      |
|**vm** | 3.0 | 3.7 |      |  1.1 |  0.9 |  0.1 |  1.1 |  0.1 |      |      |
|**np** | 2.0 | 8.7 |  1.1 |      |  0.8 |  0.1 |  0.5 |  0.8 |  0.1 |  0.1 |
|**rg** | 0.6 | 0.6 |  0.3 |  0.4 |      |      |  0.3 |      |      |      |
|**cs** |     |     |      |      |  0.1 |      |      |  2.7 |      |      |
|**da** |     | 1.2 |  0.1 |  0.4 |      |      |      |      |  0.1 |  0.5 |
|**pr** |     |     |      |      |      |  2.1 |      |      |      |      |
|**nu** | 0.2 | 0.3 |      |  0.3 |      |      |  0.7 |      |      |      |
|**pp** |     |     |      |      |  0.1 |      |  0.5 |      |      |      |

Tiempo de evaluación:

real-1m51.572s
user-1m51.324s
sys-0m0.188s

n = 4

Accuracy: 93.14%

Accuracy sobre palabras conocidas: 97.44%

Accuracy sobre palabras desconocidas: 54.14%

Matriz de Confusión

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

Se implementaron features básicos que toman como parámetros una History. También
se implementaron 2 features paramétricos como lo son NPrevTags y PrevWord.

Ejercicio 7
-----------

Se implemento Maximum Entropy Markov Model con un pipeline de scikit-learn, que contiene
un Vectorizer con los features definidos en el ejercicio6 y un clasificador que puede ser
LogisticRegression, MultinomialNB o LinearSVC. El algoritmo de tagging utilizado fue
beam inference con un beam de tamaño uno. Se sigue con los resultados:

Clasificador LogisticRegression

n = 1

Accuracy: 92.70%

Accuracy sobre palabras conocidas: 95.28%

Accuracy sobre palabras desconocidas: 69.32%

Matriz de Confusión

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

n = 2

Accuracy: 91.99%

Accuracysobre palabras conocidas: 94.55%

Accuracy sobre palabras desconocidas: 68.75%

Matriz de Confusión

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


n = 3

Accuracy: 92.18%

Accuracy sobre palabras conocidas: 94.72%

Accuracy sobre palabras desconocidas: 69.20%

Matriz de Confusión

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


n = 4

Accuracy: 92.23%

Accuracy sobre palabras conocidas: 94.72%

Accuracy sobre palabras desconocidas: 69.62%

Matriz de Confusión

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

n = 1

Accuracy: 94.43%

Accuracy sobre palabras conocidas: 97.04%

Accuracy sobre palabras desconocidas: 70.82%

Matriz de Confusión

|       | aq  | nc  |   vm |   cs |   rg | np   |   pp |  pi  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     | 9.9 |  7.3 |      |  0.1 |  0.6 |      |      |      |      |
|**nc** | 7.3 |     |  6.2 |      |  0.3 |  2.1 |      |      |      |      |
|**vm** | 6.9 | 4.7 |      |      |      |  2.0 |      |      |      |      |
|**cs** | 0.1 | 0.1 |  0.3 |      |  0.1 |      |      |      |      |      |
|**rg** | 2.8 | 0.7 |  1.3 |  0.2 |      |      |      |  0.3 |      |      |
|**np** | 0.3 | 4.6 |  1.1 |      |      |      |      |      |      |      |
|**pp** |     |     |      |      |  0.4 |      |      |      |  3.6 |      |
|**pi** |     |     |      |      |  0.2 |      |      |      |      |      |
|**da** |     | 1.6 |      |      |      |      |  0.1 |      |      |  1.0 |
|**nu** | 0.2 | 1.7 |  0.3 |      |      |      |      |      |      |      |


n = 2

Accuracy: 94.29%

Accuracy sobre palabras conocidas: 96.91%

Accuracy sobre palabras desconocidas: 70.57%

Matriz de Confusión

|       | aq  | nc  |   vm |   rg |   np | cs   |   pi |  pp  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     |10.8 |  6.9 |  0.1 |  0.6 |      |      |      |      |      |
|**nc** | 8.8 |     |  6.3 |  0.2 |  2.0 |      |      |      |      |      |
|**vm** | 6.6 | 6.3 |      |      |  2.0 |      |      |      |      |      |
|**rg** | 1.7 | 1.8 |  1.3 |      |      |  0.2 |  0.2 |      |      |      |
|**np** | 0.3 | 4.5 |  1.0 |      |      |      |      |      |      |      |
|**cs** |     | 0.1 |  0.2 |  0.1 |      |      |      |      |      |      |
|**pi** | 0.1 |     |      |  0.2 |      |      |      |      |      |      |
|**pp** |     |     |      |  0.3 |      |      |      |      |  2.9 |      |
|**da** |     | 1.5 |      |      |      |      |      |  0.3 |      |  1.0 |
|**nu** | 0.1 | 1.8 |  0.3 |      |      |      |      |      |      |      |


n = 3

Accuracy: 94.40%

Accuracy sobre palabras conocidas: 96.94%

Accuracy sobre palabras desconocidas: 71.38%

Matriz de Confusión

|       | aq  | nc  |   vm |   rg |   np | cs   |   pi |  pp  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     |10.7 |  6.5 |  0.1 |  0.6 |      |      |      |      |      |
|**nc** | 9.2 |     |  6.0 |  0.2 |  1.9 |      |      |      |      |      |
|**vm** | 6.9 | 6.0 |      |      |  2.1 |      |      |      |      |      |
|**rg** | 1.8 | 1.4 |  1.7 |      |      |  0.2 |  0.3 |      |      |      |
|**np** | 0.3 | 4.5 |  1.1 |      |      |      |      |      |      |      |
|**cs** | 0.1 | 0.1 |  0.3 |      |      |      |      |      |      |      |
|**pi** |     |     |      |  0.2 |      |      |      |      |      |      |
|**pp** |     |     |      |  0.4 |      |      |      |      |  2.9 |      |
|**da** |     | 1.6 |      |      |      |      |      |  0.4 |      |  1.0 |
|**nu** | 0.1 | 1.7 |  0.4 |      |      |      |      |      |      |      |


n = 4

Accuracy: 94.46%

Accuracy sobre palabras conocidas: 96.96%

Accuracy sobre palabras desconocidas: 71.81%

Matriz de Confusión

|       | aq  | nc  |   vm |   rg |   np | cs   |   pi |  pp  |  da  |  nu  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     |11.0 |  6.5 |  0.1 |  0.6 |      |      |      |      |      |
|**nc** | 9.3 |     |  5.2 |  0.2 |  2.0 |      |      |      |      |      |
|**vm** | 6.7 | 6.6 |      |      |  2.1 |      |      |      |      |      |
|**rg** | 1.8 | 1.4 |  1.8 |      |      |  0.2 |  0.3 |      |      |      |
|**np** | 0.3 | 4.6 |  1.1 |      |      |      |      |      |      |      |
|**cs** |     | 0.1 |  0.3 |      |      |      |      |      |      |      |
|**pi** |     |     |      |  0.2 |      |      |      |      |      |      |
|**pp** |     |     |      |  0.4 |      |      |      |      |  2.9 |      |
|**da** |     | 1.6 |      |      |      |      |      |  0.5 |      |  1.0 |
|**nu** | 0.1 | 1.7 |  0.4 |      |      |      |      |      |      |      |


Clasificador MultinomialNB

n = 1

Accuracy: 82.18%

Accuracy sobre palabras conocidas: 85.85%

Accuracy sobre palabras desconocidas: 48.89%

Matriz de Confusión

|       | aq  | vm  |  rg  |   pp |   np | nc   |  fg  |  pr  |  dd  |  pi  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     | 1.7 |      |      |  0.1 | 7.8  |      |      |      |      |
|**vm** | 0.4 |     |      |      |  0.1 | 2.8  |      |      |      |      |
|**rg** | 0.6 | 0.9 |      |      |      | 1.5  |      |      |      |      |
|**pp** |     | 1.8 |      |      |  0.1 | 0.5  |      |      |      |      |
|**np** |     | 0.1 |      |      |      | 2.0  |      |      |      |      |
|**nc** | 0.4 | 0.5 |      |      |  0.6 |      |      |      |      |      |
|**fg** | 0.2 | 0.3 |      |      |      | 1.5  |      |      |      |      |
|**pr** |     |     |      |      |      | 0.2  |      |      |      |      |
|**dd** |     | 0.3 |      |      |  0.1 | 1.4  |      |      |      |      |
|**pi** |     | 0.3 |  0.1 |      |      | 0.6  |      |      |      |      |


n = 2

Accuracy: 76.46%

Accuracy sobre palabras conocidas: 80.41%

Accuracy sobre palabras desconocidas: 40.68%

Matriz de Confusión

|       | aq  | vm  |  nc  |  rg  |  np  | pp   |  fg  |  vs  |  cs  |  cc  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     | 1.6 |  4.9 |      |      |      |      |      |      |      |
|**vm** | 0.7 |     |  2.3 |      |  0.1 |      |      |      |      |      |
|**nc** | 0.8 | 1.2 |      |      |  0.5 |      |      |      |      |      |
|**rg** | 0.5 | 0.9 |  1.1 |      |      |      |      |      |      |      |
|**np** |     | 0.1 |  1.4 |      |      |      |      |      |      |      |
|**pp** |     | 1.4 |  0.2 |      |      |      |      |      |      |      |
|**fg** | 0.1 | 0.2 |  1.1 |      |      |      |      |      |      |      |
|**vs** | 0.1 | 1.4 |  0.6 |      |      |      |      |      |      |      |
|**cs** |     | 0.1 |  0.1 |      |      |      |      |      |      |      |
|**cc** |     |     |  0.2 | 0.2  |  0.4 |      |      |      |      |      |


n = 3

Accuracy: 71.47%

Accuracy sobre palabras conocidas: 75.09%

Accuracy sobre palabras desconocidas: 38.59%

Matriz de Confusión

|       | aq  | vm  |  nc  |  rg  |  np  |  vs  |  fg  |  pp  |  cs  |  sp  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**aq** |     | 1.3 |  4.6 |      |      |      |      |      |      | 4.7  |
|**vm** | 1.0 |     |  2.8 |      |  0.1 |      |      |      |      | 4.0  |
|**nc** | 1.8 | 1.2 |      |      |  0.4 |      |      |      |      | 4.0  |
|**rg** | 0.8 | 0.8 |  1.2 |      |      |      |      |      |      | 1.8  |
|**np** |     | 0.2 |  1.4 |      |      |      |      |      |      | 1.1  |
|**vs** | 0.3 | 1.3 |  0.5 |      |      |      |      |      |      | 1.1  |
|**fg** | 0.2 | 0.1 |  0.9 |      |      |      |      |      |      | 1.0  |
|**pp** | 0.1 | 1.0 |  0.3 |      |  0.1 |      |      |      |      | 0.4  |
|**cs** |     | 0.1 |  0.2 |      |      |      |      |      |      | 0.7  |
|**sp** |     | 0.1 |  0.5 |      |  0.1 |      |      |      | 0.1  |      |


n = 4

Accuracy: 68.20%

Accuracy sobre palabras conocidas: 71.31%

Accuracy sobre palabras desconocidas: 40.01%

Matriz de Confusión

|       | vm  | aq  |  nc  |  rg  |  np  |  vs  |  cs  |  fg  |  pp  |  di  |
|-------|-----|-----|------|------|------|------|------|------|------|------|
|**vm** |     | 1.4 |  3.1 |      |  0.2 |      |      |      |      |      |
|**aq** | 0.8 |     |  4.1 |      |  0.1 |      |      |      |      |      |
|**nc** | 0.9 | 2.5 |      |      |  0.6 |      |      |      |      |      |
|**rg** | 0.8 | 1.1 |  1.2 |      |  0.1 |      |      |      |      |      |
|**np** | 0.2 |     |  1.3 |      |      |      |      |      |      |      |
|**vs** | 1.1 | 0.5 |  0.5 |      |  0.1 |      |      |      |      |      |
|**cs** | 0.1 | 0.1 |  0.4 |      |      |      |      |      |      |      |
|**fg** | 0.1 | 0.4 |  0.8 |      |  0.1 |      |      |      |      |      |
|**pp** | 0.7 | 0.2 |  0.3 |      |  0.1 |      |      |      |      |      |
|**di** | 0.2 | 0.4 |  1.1 |      |  0.1 |      |      |      |      |      |

