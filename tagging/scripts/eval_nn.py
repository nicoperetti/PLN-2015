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
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from tagging.cnn import CnnTagger


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
    lexicon = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    # files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    model = CnnTagger(lexicon)

    # tag
    hits, total = 0, 0
    hits_known, total_known = 0, 0
    hits_unknown, total_unknown = 0, 0
    n = len(sents)
    # print(n)
    for i, sent in enumerate(sents):
        try:
            word_sent, gold_tag_sent = zip(*sent)
            # print(gold_tag_sent)
            model_tag_sent = model.tag(word_sent)
            # print(model_tag_sent)
            assert len(model_tag_sent) == len(gold_tag_sent), i
            # global score
            hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
            hits += sum(hits_sent)
            total += len(sent)
            acc = (float(hits) / total) * 100
            # print(hits)
            # print(total)
            # raise
    # acuracy palabras conocidas y desconocidas
            # for j, word in enumerate(word_sent):
            #     g_t = gold_tag_sent[j]
            #     m_t = model_tag_sent[j]
            #     if model.unknown(word):
            #         total_unknown += 1
            #         if g_t == m_t:
            #             hits_unknown += 1
            #     else:
            #         total_known += 1
            #         if g_t == m_t:
            #             hits_known += 1

            # acc_know = (float(hits_known) / total_known) * 100
            # acc_unknow = (float(hits_unknown) / total_unknown) * 100

    # progress
            # por = float(i) * 100 / n
            # progress('{:3.1f}% ({:2.2f}%/{:2.2f}%/{:2.2f}%)'.format(por, acc, acc_know, acc_unknow))

            por = float(i) * 100 / n
            progress('{:3.1f}% ({:2.2f}%)'.format(por, acc))
        except:
            pass

    acc = float(hits) / total
    # acc_known = float(hits_known) / total_known
    # acc_unknown = float(hits_unknown) / total_unknown

    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))

    # print('')
    # print('Accuracy_known: {:2.2f}%'.format(acc_known * 100))

    # print('')
    # print('Accuracy_unknown: {:2.2f}%'.format(acc_unknown * 100))