from math import log2

class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.tagset = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        return self.trans[prev_tags][tag]

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        return self.out[tag][word]

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

class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
