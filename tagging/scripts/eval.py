"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
from corpus.ancora import SimpleAncoraCorpusReader
from collections import defaultdict

def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    m_conf = defaultdict(dict)
    error_count = 0
    # tag
    hits, total = 0, 0
    hits_known, total_known = 0, 0
    hits_unknown, total_unknown = 0, 0
    n = len(sents)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = (float(hits) / total) * 100

# acuracy palabras conocidas y desconocidas
        for j, word in enumerate(word_sent):
            g_t = gold_tag_sent[j]
            m_t = model_tag_sent[j]
            if model.unknown(word):
                total_unknown += 1
                if g_t == m_t:
                    hits_unknown += 1
            else:
                total_known += 1
                if g_t == m_t:
                    hits_known += 1
            if g_t != m_t:
                error_count += 1
                if g_t in m_conf and m_t in m_conf[g_t]:
                    m_conf[g_t][m_t] += 1
                else:
                    m_conf[g_t][m_t] = 1

        acc_know = (float(hits_known) / total_known) * 100
        acc_unknow = (float(hits_unknown) / total_unknown) * 100

# progress
        por = float(i) * 100 / n
        progress('{:3.1f}% ({:2.2f}%/{:2.2f}%/{:2.2f}%)'.format(por, acc, acc_know, acc_unknow))


    acc = float(hits) / total
    acc_known = float(hits_known) / total_known
    acc_unknown = float(hits_unknown) / total_unknown

    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))

    print('')
    print('Accuracy_known: {:2.2f}%'.format(acc_known * 100))

    print('')
    print('Accuracy_unknown: {:2.2f}%'.format(acc_unknown * 100))

# matriz de confusión
    temp = defaultdict(int)
    for k,v in m_conf.items():
        temp[k] = sum(v.values())
#    a = sorted(temp.items(),key = lambda sor: -sor[1])[:10]
    a = sorted(temp.items(),key = lambda sor: -sor[1])
    t = [i[0] for i in a]

    matrix_c = []
    for tag_g in t:
        partial = []
        for tag_w in t:
            if tag_w in m_conf[tag_g]:
                p = 100 * m_conf[tag_g][tag_w]/float(error_count)
                p = truncate(p, 1)
            else:
                p = 0.0
            partial += [p]
        matrix_c.append(partial)

# print a matrix
    print('      ',''.join(['{:6}'.format(item) for item in t]),'\n')
    for tag, row in zip(t,matrix_c):
        tag += '   '
        r = [str(i) for i in row]
        print(tag, '   '.join(r))

# plot a confusion matrix
    plt.matshow(matrix_c)
    plt.title('Confusion matrix')
    tick_marks = np.arange(len(t))
    plt.xticks(tick_marks, t)
    plt.yticks(tick_marks, t)
    plt.colorbar()
    plt.show()
