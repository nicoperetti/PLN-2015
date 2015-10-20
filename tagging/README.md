PLN 2015: Práctico 2
================================================


Ejercicio 1
-----------

Este ejercicio consistia en sacar estadísticas sobre el corpus.

Estadísticas básicas:

| cantidad de oraciones   | 17379  |
| cantidad de ocurrencias | 517268 |
| vocabulario             | 46482  |
| vocabulario de tags     | 48     |

Etiquetas más frecuentes:

| tag | frecuencia | %     | cinco palabras más frecuentes                         |
|-----|------------|-------|-------------------------------------------------------|
| nc  |   92002    | 17.78 | 'años', 'presidente', 'millones', 'equipo', 'partido' |
| sp  |   79904    | 15.44 | 'de', 'en', 'a', 'del', 'con'                         |
| da  |   54552    | 10.54 | 'la', 'el', 'los', 'las', 'El'                        |
| vm  |   50609    | 9.78  | 'está', 'tiene', 'dijo', 'puede', 'hace'              |
| aq  |   33904    | 6.55  | 'pasado', 'gran', 'mayor', 'nuevo', 'próximo'         |
| fc  |   30148    | 5.82  | ','                                                   |
| np  |   29113    | 5.62  | 'Gobierno', 'España', 'PP', 'Barcelona', 'Madrid'     |
| fp  |   21157    | 4.09  | '.', '(', ')'                                         |
| rg  |   15333    | 2.96  | 'más', 'hoy', 'también', 'ayer', 'ya'                 |
| cc  |   15023    | 2.90  | 'y', 'pero', 'o', 'Pero', 'e'                         |

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

Se implemento un modelo de n-gramas representado en la clase NGram, donde lo primero que se tuvo en cuenta
es la agragación de los n-1 tags de inicio de cada sentencia y el tags de final de sentencia que son "<s>"
y "</s>" respectivamente.
Para poder implementar la probabilidad condicional de un token dado los previos n-1 tokens tuve que guardar
en un diccionario las ocurrencias de n-gramas y n-1-gramas.
También se implemento la probabilidad de una sentencia y la log-probability de una sentencia, utilizando la
probabilidad condicional.


Para entrenar el modelo: python scripts/train.py -n <n> -o <file> 

n: orden del modelo

o: archivo que contiene el modelo


Ejercicio 3
-----------

Se implemento la clase NGramGenerator. se guardan las probabilidades de un token dado los n-1 anteriores y
se guardan decendientemente para optimizar.
También se implementaron los métodos generate_token y generate_sent.
Además se escribió un scripts generate.py. 

Para correrlo python scripts/generate.py -i <file> -n <n>


i: modelo ya entrenado

n: cantidad de sentencias generadas


| n | oraciones gereradas                                                                                                                             |
|---|-------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | se . por y volar Ser Ser estancia ponerse negro Insistía reír el exponer banderizo su , — sobre hizo plata que . un restos — de preceda único |
|   | reconoció bien                                                                                                                                  |
| 2 | — pensó Sansa empezaba a los colgó el espectáculo ante el camino — Tal vez levantaba .                                                          |
|   | — Los Targaryen conquistó Dorne , tiene al sur , ser por un círculo de ellos un bebé .                                                          |
| 3 | El cuchillo también es mi sobrina , y sería antes de que lleguen Qhorin Mediamano tenía miedo de que anochezca .                        |
|   | — Hace demasiado tiempo , sí , puede que no fuera así .                                                                                         |
| 4 | — Bah , yo soy el capitán de su guardia , Mediamano había confeccionado media docena de thenitas que iban con él .                               |
|   | —¿ Con qué sueñas , niña ?                                                                                                                      |


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

