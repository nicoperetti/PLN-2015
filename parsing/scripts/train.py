"""Train a parser.

Usage:
  train.py [-m <model>] [-n <n>] [-u <unary>] -o <file>
  train.py -h | --help

Options:
  -m <model>        Model to use [default: flat]:
                      flat: Flat trees
                      rbranch: Right branching trees
                      lbranch: Left branching trees
                      upcfg: unlexicalized PCFG
  -n <n>            Order of the markovization model upcfg
  -u <unary>        True if acept unary rules[default: False]
  -o <file>         Output model file.
  -h --help         Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.baselines import Flat, RBranch, LBranch
from parsing.upcfg import UPCFG

models = {
    'flat': Flat,
    'rbranch': RBranch,
    'lbranch': LBranch,
    'upcfg': UPCFG,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading corpus...')
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)

    print('Training model...')
    mo = opts['-m']
    if mo == 'upcfg':
        n = opts['-n']
        if n is not None:
            n = int(n)
        unary = opts['-u']
        if unary == 'False':
            model = models[mo](corpus.parsed_sents(), horzMarkov=n)
        else:
            model = models[mo](corpus.parsed_sents(), horzMarkov=n, unary=True)
    else:
        model = models[mo](corpus.parsed_sents())

    print('Saving...')
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
