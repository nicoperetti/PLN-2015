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
    word_tags = defaultdict(dict)
    ambi = defaultdict(dict)
    l_sent = 0
    for sent in sents:
        l_sent += len(sent)
        for (w,t) in sent:
            words[w] += 1
            tags[t] += 1
            if w in word_tags[t]:
                word_tags[t][w] += 1
            else:
                word_tags[t][w] = 1
            if t in ambi[w]:
                ambi[w][t] += 1
            else:
                ambi[w][t] = 1

    print('sents: {}'.format(len(sents)))
    print('word_ocur: {}'.format(l_sent))
    print('voc_words_size: {}'.format(len(words)))
    print('voc_tags_size: {}'.format(len(tags)))

    tags_sorted = sorted(tags.items(), key = lambda sor: -sor[1])
    tags_sorted = tags_sorted[:10]
    five_frec = []
    for (t,f) in tags_sorted:
        t_w_s = sorted(word_tags[t].items(), key = lambda sor: -sor[1])
        t_w_s = t_w_s[:5]
        five_frec.append([x for (x,y) in t_w_s])
    print("\n")
    print('tags    frec          %                       more frecuently words')
    for n, i in enumerate(tags_sorted):
        print(' {}     {}      {}    {}'.format(i[0],i[1], 100*float(i[1]/l_sent),five_frec[n]))

    count_ambi = [0 for i in range(9)]
    five_frec = []
    for (k,v) in ambi.items():
        l = len(v)
        count_ambi[l-1] += 1
    print('\n')
    print("ambiguous level      words number        %")
    for i,c in enumerate(count_ambi,1):
        p = (c/float(len(words)))*100
        print(' {}                  {}                    {}'.format(i, c, p))



