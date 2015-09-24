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

Ejercicio 3
-----------

Ejercicio 4
-----------

Ejercicio 5
-----------

Ejercicio 6
-----------

Ejercicio 7
-----------

