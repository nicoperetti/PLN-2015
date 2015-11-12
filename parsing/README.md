PLN 2015: Práctico 3
================================================

Entrenar y evaluar
------------------
para entrenar:

```
python3 parsing/scripts/train.py [-m <model>] [-n <n>] [-u <unary>] -o <file>
```
model: flat | rbranch | lbranch | upcfg. flat por default
n: orden markovización horizontal.
unary: True si se aceptan producciones unarias. False por default
file: modelo

para evaluar::
```
python3 parsing/scripts/eval.py -i <file> [-m <m>] [-n <n>]
```
file: model
m: sentencias con largo mayor i igual a m
n: cantidad de sentencias a evaluar

Ejercicio 1
-----------

Los resultados estan aplicados a evaluar los modelos con todas las oraciones
de largo menor o igual a 20.

Parsed 1444 sentences

Modelo baseline Flat:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 99.93%    | 14.57% | 25.43% |
| **Unlabeled** | 100.00%   | 14.58% | 25.45% |

Tiempo de evaluación:

real-0m11.667s
user-0m10.985s
sys-0m0.140s

Modelo baseline LBranch:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 8.81%     | 14.57% | 10.98% |
| **Unlabeled** | 14.71%    | 24.33% | 18.33% |

Tiempo de evaluación:

real-0m12.749s
user-0m12.477s
sys-0m0.224s


Modelo baseline RBranch:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 8.81%     | 14.57% | 10.98% |
| **Unlabeled** | 8.87%     | 14.68% | 11.06% |

Tiempo de evaluación:

real-0m12.325s
user-0m12.134s
sys-0m0.168s

Ejercicio 2
-----------

Se implemento en cky_parser.py el algoritmo CKY el cual toma una PCFG y una sentencia
y retorna el el árbol de parcing más probable.

Se implemento un test con ambiguedad, la sentencia es "the fast car mechanic", la 
cual tiene dos posibles formas de parsing.

Ejercicio 3
-----------
Modelo upcfg:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 73.25%    | 72.95% | 73.10% |
| **Unlabeled** | 75.36%    | 75.05% | 75.21% |


Tiempo de evaluación:

real-6m42.861s
user-6m31.865s
sys-0m1.595s

Ejercicio 4
-----------

Modelo upcfg con markovización horizontal de orden 0:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 70.25%    | 70.02% | 70.14% |
| **Unlabeled** | 72.11%    | 71.88% | 72.00% |

Tiempo de evaluación:

real-3m4.347s
user-3m3.584s
sys-0m0.264s

Modelo upcfg con markovización horizontal de orden 1:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 74.62%    | 74.53% | 74.57% |
| **Unlabeled** | 76.48%    | 76.38% | 76.43% |

Tiempo de evaluación:

real-3m27.898s
user-3m27.532s
sys-0m0.284s

Modelo upcfg con markovización horizontal de orden 2:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 74.89%    | 74.37% | 74.63% |
| **Unlabeled** | 76.81%    | 76.28% | 76.55% |

Tiempo de evaluación:

real-5m14.277s
user-5m13.566s
sys-0m0.472s

Modelo upcfg con markovización horizontal de orden 3:

|               | Precision | Recall | F1     |
|---------------|-----------|--------|--------|
| **Labeled**   | 74.08%    | 73.45% | 73.76% |
| **Unlabeled** | 76.24%    | 75.59% | 75.91% |

Tiempo de evaluación:

real-6m14.863s
user-6m9.782s
sys-0m1.124s

Ejercicio 5
-----------

Se implemento la contemplación de producciones unarias para el algoritmo CKY,
aunque en principio andaría ya que se escribió un test y lo pasa, pero tarda muy
mucho en evaluar, asique queda abierta la optimización del CKY para con producciones
unarias.
