"""Evaulate a parser.

Usage:
  eval.py -i <file> [-m <m>] [-n <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -m <m>        Parse only sentences of length <= <m>.
  -n <n>        Parse only <n> sentences (useful for profiling).
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.util import spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    print('Loading corpus...')
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    parsed_sents = list(corpus.parsed_sents())

    print('Parsing...')
    hits, hits_unlabeled, total_gold, total_model = 0, 0, 0, 0
    count = 1
    n = opts['-n']
    m = opts['-m']
    if m is None:
        m = float('inf')
    else:
        m = int(m)
    if n is None:
        n = len(parsed_sents)
    else:
        n = int(n)

    format_part1 = '{:3.1f}% ({}/{})'
    format_part2 = '(P-L={:2.2f}%, R-L={:2.2f}%, F1-L={:2.2f}%)'
    format_part3 = '(P-Un={:2.2f}%, R-Un={:2.2f}%, F1-Un={:2.2f}%)'
    format_str = format_part1 + ' ' + format_part2 + ' ' + format_part3
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    l_p_s = len(parsed_sents)  # number of sentences

    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()
        if len(tagged_sent) <= m and count <= n:
            # parse
            model_parsed_sent = model.parse(tagged_sent)

            # compute labeled scores
            gold_spans = spans(gold_parsed_sent, unary=False)
            model_spans = spans(model_parsed_sent, unary=False)
            hits += len(gold_spans & model_spans)
            total_gold += len(gold_spans)  # labeled and unlabeled
            total_model += len(model_spans)  # labeled and unlabeled

            # compute labeled partial results
            prec = float(hits) / total_model * 100
            rec = float(hits) / total_gold * 100
            f1 = 2 * prec * rec / (prec + rec)

            # compute unlabeled scores
            gold_spans_unlabeled = set([(y, z) for x, y, z in gold_spans])
            model_spans_unlabeled = set([(y, z) for x, y, z in model_spans])
            hits_unlabeled += len(gold_spans_unlabeled & model_spans_unlabeled)

            # compute unlabeled partial results
            prec_unlabeled = float(hits_unlabeled) / total_model * 100
            rec_unlabeled = float(hits_unlabeled) / total_gold * 100
            den = prec_unlabeled + rec_unlabeled
            f1_unlabeled = 2 * prec_unlabeled * rec_unlabeled / den

            progress(format_str.format(float(count) * 100 / n, count, l_p_s,
                     prec, rec, f1, prec_unlabeled, rec_unlabeled,
                     f1_unlabeled))

            count += 1

    print('')
    print('Parsed {} sentences'.format(count - 1))
    print('Labeled')
    print('  Precision: {:2.2f}% '.format(prec))
    print('  Recall: {:2.2f}% '.format(rec))
    print('  F1: {:2.2f}% '.format(f1))

    print('Unlabeled')
    print('  Precision: {:2.2f}% '.format(prec_unlabeled))
    print('  Recall: {:2.2f}% '.format(rec_unlabeled))
    print('  F1: {:2.2f}% '.format(f1_unlabeled))
