PLN 2015: Práctico 1
================================================


Ejercicio 1
-----------

En este ejercicio basicamente se eligió un corpus y se modifico el train.py para
que utilice el mismo.

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
Además se escribió un scripts generate.py. Para correrlo python scripts/generate.py -i <file> -n <n>
i: modelo ya entrenado
n: cantidad de sentencias generadas

oraciones gereradas
| n | oraciones  |
|---|------------|
| 1 |            |
| 2 |            |
| 3 |            |
| 4 |            |
|   |            |

Ejercicio 4
-----------

Ejercicio 5
-----------

Ejercicio 6
-----------

Ejercicio 7
-----------

