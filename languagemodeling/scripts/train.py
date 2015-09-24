"""Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpolated : N-gram with interpotated smoothing
                  backoff: N-gram with discounting back-off smoothing
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import gutenberg, PlaintextCorpusReader
from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram, BackOffNGram

if __name__ == '__main__':
    opts = docopt(__doc__)


    # load the data
#    sents = gutenberg.sents('austen-emma.txt')
    corpus = PlaintextCorpusReader('corpus/', '1.txt')
    sents = corpus.sents()

    # split the corpus(90%-10%)
    cant = int(90 * len(sents) / 100)
    sents = sents[:cant]

    # train the model
    n = int(opts['-n'])
    model = opts['-m']
    if model == 'addone':
        m = AddOneNGram(n, sents)
    elif model == 'interpolated':
        m = InterpolatedNGram(n, sents)
    elif model == 'backoff':
        m = BackOffNGram(n, sents, 0.5)
    else:
        m = NGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(m, f)
    f.close()
