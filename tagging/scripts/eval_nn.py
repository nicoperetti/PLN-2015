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
import random


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
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents1 = list(corpus.tagged_sents())

    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents2 = list(corpus.tagged_sents())    
    sents = sents1 + sents2
    n = len(sents)
    print(n)
    random.seed(7)
    random.shuffle(sents)

    split = int(n*.9)
    # train_sents = sents[:split]
    test_sents = sents[split:]

    model = CnnTagger(lexicon)

    # tag
    hits, total = 0, 0
    hits_known, total_known = 0, 0
    hits_unknown, total_unknown = 0, 0
    n = len(test_sents)
    print(n)
    for i, sent in enumerate(test_sents, 1):
        try:
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
                if lexicon.unknown(word):
                    total_unknown += 1
                    if g_t == m_t:
                        hits_unknown += 1
                else:
                    total_known += 1
                    if g_t == m_t:
                        hits_known += 1

            acc_know = (float(hits_known) / total_known) * 100
            acc_unknow = (float(hits_unknown) / total_unknown) * 100

    # progress
            por = float(i) * 100 / n
            progress('{:3.1f}% ({:2.2f}%/{:2.2f}%/{:2.2f}%)'.format(por, acc, acc_know, acc_unknow))

            # por = float(i) * 100 / n
            # progress('{:3.1f}% ({:2.2f}%)'.format(por, acc))
        except:
            pass

    acc = float(hits) / total
    acc_known = float(hits_known) / total_known
    acc_unknown = float(hits_unknown) / total_unknown

    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))

    print('')
    print('Accuracy_known: {:2.2f}%'.format(acc_known * 100))

    print('')
    print('Accuracy_unknown: {:2.2f}%'.format(acc_unknown * 100))