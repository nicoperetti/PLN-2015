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
    word_tags = defaultdict(int)
    amb = defaultdict(dict)
    long_sent = 0
    for sent in sents:
        long_sent += len(sent)
        for pair in sent:
            words[pair[0]] += 1
            tags[pair[1]] += 1
            word_tags[pair] += 1
            try:
                amb[pair[0]][pair[1]] += 1
            except KeyError:
                amb[pair[0]][pair[1]] = 1

    tags_sorted = sorted(tags.items(), key = lambda sor: -sor[1])
    word_tags = sorted(word_tags.items(), key = lambda sor: -sor[1])

    tags_sorted = tags_sorted[:10]
    tags_sorted_f = [d[0] for d in tags_sorted]
    tags_ocur = long_sent
    print('sents: {}'.format(len(sents)))
    print('word_ocur: {}'.format(long_sent))
    print('voc_words_size: {}'.format(len(words)))
    print('voc_tags_size: {}'.format(len(tags)))
    for i in tags_sorted:
        print('tags_frec: {}, frec: {}, %: {}'.format(i[0],i[1], float(i[1]/tags_ocur)))

    for t in tags_sorted_f:
        print(t)
        print("\n")
        count = 0
        for pair in word_tags:
            if pair[0][1] == t:
                print(pair[0][0])
                count += 1
            if count == 5:
                break

#    asd = []
#    for i in range(10):
#        asd.append(0)
#    for l in range(10):
#        
