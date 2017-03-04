from math import log2
from collections import defaultdict
from random import shuffle

class Lexicon:

    def __init__(self, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.t_w_out_p = defaultdict(dict)
        self.w_t_out_p = defaultdict(dict)
        self.wcount = defaultdict(int)
        self.tcount = defaultdict(int)
        self.word_set = []
        self.tags_set = []

        for tagged_sent in tagged_sents:
            for word, tag in tagged_sent:
                if word in self.t_w_out_p[tag]:
                    self.t_w_out_p[tag][word] += 1
                else:
                    self.t_w_out_p[tag][word] = 1

                if tag in self.w_t_out_p[word]:
                    self.w_t_out_p[word][tag] += 1
                else:
                    self.w_t_out_p[word][tag] = 1
                
                self.word_set.append(word)
                self.tags_set.append(tag)
                self.wcount[(word,)] += 1
                self.tcount[(tag,)] += 1

        self.word_set = set(self.word_set)
        self.tags_set = list(set(self.tags_set))
        self.tagset_len = len(self.tags_set)
        self.wordset_len = len(self.word_set)

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return not w in self.word_set

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tags_set

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        p = 0.0
        try:
            p = self.t_w_out_p[tag][word]/float(self.tcount[(tag,)])
        except:
            p = 0.0
        return p