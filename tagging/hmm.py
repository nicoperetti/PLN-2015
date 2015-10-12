from math import log2
from collections import defaultdict

class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.tags = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tags

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        try:
            p = self.trans[prev_tags][tag]
        except KeyError:
            p = 0.0
        return p

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        try:
            p = self.out[tag][word]
        except KeyError:
            p = 0.0
        return p

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.
        y -- tagging.
        """
        p = 1.0
        prev_tag = ('<s>',) * (self.n - 1)
        for tag in y:
            p *= self.trans_prob(tag, prev_tag)
            prev_tag = prev_tag[1:]
            if self.n > 1:
                prev_tag += (tag,)
        return p

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.
        x -- sentence.
        y -- tagging.
        """
        p = 1.0
        for word, tag in zip(x, y):
            p *= self.out_prob(word, tag)
        return p

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
        y -- tagging.
        """
        p = 0.0
        prev_tag = ('<s>',) * (self.n - 1)
        for tag in y:
            p += log2(self.trans_prob(tag, prev_tag))
            prev_tag = prev_tag[1:]
            if self.n > 1:
                prev_tag += (tag,)
        return p

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.
        x -- sentence.
        y -- tagging.
        """
        p = 0.0
        for word, tag in zip(x, y):
            p += log2(self.out_prob(word, tag))
        return p

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
        tagger = ViterbiTagger(self)
        return tagger.tag(sent)


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
        hmm = self.hmm
        n = hmm.n
        self._pi = defaultdict(lambda : defaultdict(tuple))
        ini = ('<s>',) * (n - 1)
        self._pi[0][ini] = (log2(1.0), [])

        for i, word in enumerate(sent, 1):
            pi_ant = self._pi[i-1].items()
            for key, value in pi_ant:
                for v in hmm.tagset():
                    q = hmm.trans_prob(v, key)
                    e = hmm.out_prob(word, v)
                    if q * e != 0:
                        asd = key[1:] + (v,)
                        pro = value[0] + log2(q) + log2(e)
                        lis = list(value[1])
                        lis.append(v)
                        self._pi[i][asd] = (pro, lis)
        # mejorar
        las_pi = self._pi[len(sent)].items()
        return max([(prob ,dic) for key, (prob ,dic) in las_pi])[1]
#        for hola, chau in las_pi:
#            result = chau[1]
#        return result

