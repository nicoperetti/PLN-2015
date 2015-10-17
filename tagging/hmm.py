from math import log2
from collections import defaultdict
from random import shuffle
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
        tags = y + ['</s>']
        for tag in tags:
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
        p_w_t = 1.0
        for word, tag in zip(x, y):
            p_w_t *= self.out_prob(word, tag)
        p_t = self.tag_prob(y)
        return p_t * p_w_t

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
        y -- tagging.
        """
        p = 0.0
        prev_tag = ('<s>',) * (self.n - 1)
        tags = y + ['</s>']
        for tag in tags:
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
        p_w_t = 0.0
        for word, tag in zip(x, y):
            p_w_t += log2(self.out_prob(word, tag))
        p_t = self.tag_log_prob(y)
        return p_t + p_w_t

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
        self._pi = defaultdict(dict)
        ini = ('<s>',) * (n - 1)
        self._pi[0][ini] = (log2(1.0), [])
        K = list(hmm.tagset())

#        for i, word in enumerate(sent, 1):
#            pi_ant = self._pi[i-1].items()
#            for key, (p, dic) in pi_ant:
#                for v in K:
#                    e = hmm.out_prob(word, v)
#                    q = hmm.trans_prob(v, key)
#                    if q * e != 0:
#                        tupl = key + (v,)
#                        tupl = tupl[1:]
#                        pro = p + log2(q) + log2(e)
#                        lis = list(dic)
#                        lis.append(v)
#                        try:
#                            j = self._pi[i][tupl][0]
#                            if j < pro:
#                                self._pi[i][tupl] = (pro, lis)
#                        except KeyError:
#                            self._pi[i][tupl] = (pro, lis)

        for i, word in enumerate(sent, 1):
            print(i)
            pi_ant = self._pi[i-1].items()
            for v in K:
                e = hmm.out_prob(word, v)
                if e != 0:
                    for key, (p, dic) in pi_ant:
                        q = hmm.trans_prob(v, key)
                        if q * e != 0:
                            tupl = key + (v,)
                            tupl = tupl[1:]
                            print("q: ",log2(q))
                            print("e: ",log2(e))
                            pro = p + log2(q) + log2(e)
                            lis = list(dic)
                            lis.append(v)
                            try:
                                j = self._pi[i][tupl][0]
                                if j < pro:
                                    self._pi[i][tupl] = (pro, lis)
                            except KeyError:
                                self._pi[i][tupl] = (pro, lis)
#                                print("q: ",log2(q))
#                                print("e: ",log2(e))

        las_pi = self._pi[len(sent)].items()
        final = []
        print(self._pi)
        for key, (prob ,dic) in las_pi:
            t_p = hmm.trans_prob('</s>', key)
            if t_p != 0:
                final += [(prob + log2(t_p), dic)]
        return max(final)[1]
#        return max([(prob ,dic) for key, (prob ,dic) in las_pi])[1]


class MLHMM:

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.addone = addone
        self.n = n
        tag_frec = defaultdict(int)
        self.out_p = defaultdict(dict)
        self.tcount_1 = defaultdict(int)
        word_set = []
        tags_set = []
        for tagged_sent in tagged_sents:
            tags = ["<s>"] * (n-1)
            for word, tag in tagged_sent:
                try:
                    self.out_p[tag][word] += 1
                except KeyError:
                    self.out_p[tag][word] = 1
                tags += [tag]
                word_set += [word]
                tags_set += [tag]
                self.tcount_1[(tag,)] += 1
            tags += ["</s>"]
            for i in range(len(tags) - n + 1):
                key = tuple(tags[i: i + n])
                tag_frec[key] += 1
                tag_frec[key[:-1]] += 1
        self.tag_frec = tag_frec

        self.word_set = set(word_set)
        self.tags_set = set(tags_set)
        self.tagset_len = len(self.tags_set)
        self.wordset_len = len(self.word_set)

    def tcount(self, tokens):
        """Count for an k-gram or k-1-gram.
        tokens -- the k-gram tuple.
        """
        return self.tag_frec[tokens]

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        result = True
        if w in self.word_set:
            result = False
        return result

    def tagset(self):
        """Returns the set of tags.
        """
        return set(self.tags_set)

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        addone = self.addone
#        if not prev_tags:
#            prev_tags = ()
#        assert len(prev_tags) == self.n - 1
        if self.n == 1:
            prev_tags = ()
        assert len(prev_tags) == self.n - 1

        tags = prev_tags + (tag,)
        tags_c = self.tcount(tags)
        prev_tags_c = self.tcount(prev_tags)
        if addone:
            result = (tags_c + 1)/ float(prev_tags_c + self.tagset_len)
        else:
            result = tags_c / float(prev_tags_c)
        return result

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        unk_w = self.unknown(word)
#        print("tag: ",tag)
        if unk_w:
            p = 1/float(self.wordset_len)
        else:
            p = float(self.tcount_1[(tag,)])
#            print("count of tag: ",p)
            if p != 0:
                try:
                    a = self.out_p[tag][word]
                except KeyError:
                    a = 0
                p = a/p
        return p

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.
        y -- tagging.
        """
        p = 1.0
        prev_tag = ('<s>',) * (self.n - 1)
        tags = y + ["</s>"]
        for tag in tags:
            p *= self.trans_prob(tag, tuple(prev_tag))
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
        p_w_t = 1.0
        for word, tag in zip(x,y):
            p_w_t *= self.out_prob(word, tag)
        p_t = self.tag_prob(y)
        return p_t * p_w_t

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
        y -- tagging.
        """
        p = 0.0
        prev_tag = ('<s>',) * (self.n - 1)
        tags = y + ["</s>"]
        for tag in tags:
            t_p = self.trans_prob(tag, tuple(prev_tag))
            if t_p == 0:
                p = float("-inf")
                break
            else:
                p += log2(t_p)
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
        p_w_t = 0.0
        for word, tag in zip(x,y):
            p_w_t += log2(self.out_prob(word, tag)) #DOIT ver si es cero
        p_t = self.tag_log_prob(y)
        return p_t + p_w_t


    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
        tagger = ViterbiTagger(self)
        return tagger.tag(sent)
