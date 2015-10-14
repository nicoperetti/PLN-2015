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
#        self._pi = defaultdict(lambda : defaultdict(tuple))
        self._pi = defaultdict(dict)
        ini = ('<s>',) * (n - 1)
        self._pi[0][ini] = (log2(1.0), [])

        for i, word in enumerate(sent, 1):
            pi_ant = self._pi[i-1].items()
            for key, (p, dic) in pi_ant:
                for v in hmm.tagset():
                    q = hmm.trans_prob(v, key)
                    e = hmm.out_prob(word, v)
                    if q * e != 0:
                        tupl = key[1:] + (v,)
                        pro = p + log2(q) + log2(e)
                        lis = list(dic)
                        lis.append(v)
                        self._pi[i][tupl] = (pro, lis)
        las_pi = self._pi[len(sent)].items()
        return max([(prob ,dic) for key, (prob ,dic) in las_pi])[1]


class MLHMM:

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        tagset = []
        tag_frec = defaultdict(int)
        for tagged_sent in tagged_sents:
            tags = ["<s>"] * (n-1) + [tag for word, tag in tagged_sent] + ["</s>"]
            for i in range(len(tags) - n + 1):
                key = tuple(tags[i: i + n])
                tag_frec[key] += 1
                tag_frec[key[:-1]] += 1
        self.tag_frec = tag_frec
        self.n = n

    def tcount(self, tokens):
        """Count for an k-gram or k-1-gram.
        tokens -- the k-gram tuple.
        """
        return self.tag_frec[tokens]

#    def unknown(self, w):
#        """Check if a word is unknown for the model.
#        w -- the word.
#        """

#    def tagset(self):
#        """Returns the set of tags.
#        """

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        if not prev_tags:
            prev_tags = ()
        assert len(prev_tags) == self.n - 1

        tags = prev_tags + (tag,)
        tags_c = self.tcount(tags)
        prev_tags_c = self.tcount(prev_tags)
        return tags_c / float(prev_tags_c)

#    def out_prob(self, word, tag):
#        """Probability of a word given a tag.
# 
#        word -- the word.
#        tag -- the tag.
#        """

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.
        y -- tagging.
        """
        print(self.tag_frec)
        p = 1.0
        prev_tag = ('<s>',) * (self.n - 1)
        y += ["</s>"]
        for tag in y:
            p *= self.trans_prob(tag, tuple(prev_tag))
            print(p)
            prev_tag = prev_tag[1:]
            if self.n > 1:
                prev_tag += (tag,)
        return p

#    def prob(self, x, y):
#        """
#        Joint probability of a sentence and its tagging.
#        Warning: subject to underflow problems.
# 
#        x -- sentence.
#        y -- tagging.
#        """
# 
#    def tag_log_prob(self, y):
#        """
#        Log-probability of a tagging.
# 
#        y -- tagging.
#        """
# 
#    def log_prob(self, x, y):
#        """
#        Joint log-probability of a sentence and its tagging.
# 
#        x -- sentence.
#        y -- tagging.
#        """
# 
#    def tag(self, sent):
#        """Returns the most probable tagging for a sentence.
# 
#        sent -- the sentence.
#        """
