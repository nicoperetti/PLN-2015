"""Evaluate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import gutenberg
from languagemodeling.ngram import AddOneNGram, InterpolatedNGram

if __name__ == '__main__':
    opts = docopt(__doc__)

    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    sents = gutenberg.sents('austen-emma.txt')

    # split the corpus(90%-10%)
    corpus_set = int(90 * len(sents) / 100)
    sents = sents[corpus_set:]

    M = 0
    for sent in sents:
        M += len(sent)
    pp = model.perplexity(M, sents)
    print(pp)
