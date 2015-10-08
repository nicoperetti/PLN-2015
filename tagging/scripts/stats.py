"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt

from corpus.ancora import SimpleAncoraCorpusReader
from collections import defaultdict

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = list(corpus.tagged_sents())

    # compute the statistics
    words = defaultdict(int)
    tags = defaultdict(int)
    long_sent = 0
    for sent in sents:
        l += len(sent)
        for pair in sent:
            words[pair[0]] += 1
            tags[pair[1]] += 1

    tags_sorted = sorted(tags.items(), key = lambda sor: -sor[1])
    tags_sorted = tags_sorted[:10]
    tags_ocur = long_sent
    print('sents: {}'.format(len(sents)))
    print('word_ocur: {}'.format(long_sent)
    print('voc_words_size: {}'.format(len(words)))
    print('voc_tags_size: {}'.format(len(tags)))
    print('tags_frec: {}'.format()


