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

Para entrenar: python3 tagging/scripts/train.py [-m <model>] [-n <n>] -o <file>

<model>: Model to use [default: base]:
                  base: Baseline
                  addone: Addone
                  memm: MEMM
<n>: Order of the model[only if the model is not base]
<file>: Output model file.

Para evaluar: python3 tagging/scripts/eval.py -i <file>

<file>: modelo ya entrenado


Para el modelo baseline se obtuvieron los siguientes resultados:

Accuracy: 89.02%

Accuracy sobre palabras conocidas: 95.34%

Accuracy sobre palabras desconocidas: 31.80%

Matriz de confusión(Error Analysis):



Ejercicio 4
-----------

Se implemento la clase AddOneNGram, la cual hereda de la clase NGram y agraga en su init el calculo de la longitud
del vocabulario y se modifica el método cond_prob para que calcule la probabilidad condicional utilizando
suavizado addone.
Se modifico train.py para que acepte el modelo addone

entrenar: python scripts/train.py -n <n> [-m <model>] -o <file> 

n: orden del modelo

m: modelo

o: archivo que contiene el modelo


Ejercicio 5
-----------

Se implementaron los métodos de log-probability, cross-entropy y perplejidad en la clase NGram.
Se escribió un scripts eval.py en el cual se carga un modelo entrenado con el 90% del corpus y 
lo evalua con el 10% restante. 
A menor perplejidad mejor es el modelo.

evaluar: python scripts/eval.py -i <file>

i: modelo entrenado

evaluacion del modelo de suavizado addone

| n | Perplejidad |
|---|-------------|
| 1 | 1212        |
| 2 | 3106        |
| 3 | 15121       |
| 4 | 22118       |


Ejercicio 6
-----------

Se implemento la clase InterpolatedNGram. si el parametro gamma de esta clase no es dado se calcula utilizando
datos held-out. Utiliza addone para los unigramas.

evaluacion del modelo de suavizado por interpolacion

| n | Perplejidad |
|---|-------------|
| 1 | 1221        |
| 2 | 394         |
| 3 | 375         |
| 4 | 386         |

Ejercicio 7
-----------
Se implemento la clase BackOffNGram. Si el parametro de discounting beta no es dado se estima el mejor beta.

evaluacion del modelo de suavizado backoff con discounting

| n | Perplejidad |
|---|-------------|
| 1 | 1212        |
| 2 | 302         |
| 3 | 285         |
| 4 | 293         |

