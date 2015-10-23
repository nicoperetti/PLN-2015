"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-n <n>] [-c <clf>]-o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
                  addone: Addone
                  memm: MEMM
  -n <n>        Order of the model[only if the model is not base]
  -c <clf>      Clasf [default: LR]
                  LR: LogisticRegression
                  LSVC: LinearSVC
                  MNB: MultinomialNB
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import MLHMM
from tagging.memm import MEMM

models = {
    'base': BaselineTagger,
    'addone':MLHMM,
    'memm': MEMM,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # train the model
    m = opts['-m']
    if m == 'addone':
        n = int(opts['-n'])
        model = models[m](n, sents)
    elif m == 'memm':
        n = int(opts['-n'])
        clf = opts['-c']
        model = models[m](n, sents, clf)
    else:
        model = models[m](sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
