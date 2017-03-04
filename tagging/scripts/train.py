"""Train a sequence tagger.

Usage:
  train.py -o <file>
  train.py -h | --help

Options:
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.lexicon import Lexicon
import random

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents1 = list(corpus.tagged_sents())

    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents2 = list(corpus.tagged_sents())  
    sents = sents1 + sents2

    random.seed(7)
    random.shuffle(sents)
    split = int(len(sents)*.9)
    sents = sents[:split]

    # train the model
    model = Lexicon(sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
