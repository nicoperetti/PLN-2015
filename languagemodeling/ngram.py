# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from random import random

class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        for sent in sents:
            sent = (['<s>'] *(n-1)) + sent # agrego n-1 tags de inicio de oracion
            sent.append('</s>')
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tokens]


    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.count(tuple(tokens))) / self.count(tuple(prev_tokens))

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
        sent -- the sentence as a list of tokens.
        """
        n = self.n
        prob_sent = 1
        sent.append('</s>') # agrego el fin de oracion a la sentencia
        prev_token = ['<s>'] * (n-1) # agrego los principios de oracion
        for token in sent: 
            prob_sent *= self.cond_prob(token, prev_token)
            prev_token.append(token)
            prev_token = prev_token[1:]
            if prob_sent == 0: # si es cero termino
                break
        return prob_sent

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
        sent -- the sentence as a list of tokens.
        """
        n = self.n
        prob_log_sent = 0
        sent.append('</s>') # agrego el fin de oracion a la sentencia
        prev_token = ['<s>'] * (n-1) # agrego los principios de oracion
        for token in sent:
            p = self.cond_prob(token, prev_token)
            if p == 0: # si es cero termino
                prob_log_sent = float("-inf")
                break
            prob_log_sent += log(p, 2)
            prev_token.append(token)
            prev_token = prev_token[1:]
        return prob_log_sent

#    def sent_log_prob(self, sent):
#        a = self.sent_prob(sent)
#        if a != 0:
#            return log(a,2)
#        else:
#            return float('-inf')
    def cross_entropy(self, M, sents):
        """M -- total number of words in the test corpus.
        sents -- the sentences as a list of tokens.
        """
        l = 0.0
        for sent in sents:
            l += self.sent_log_prob(sent)
        return l/M

    def perplexity(self, M, sents):
        """M -- total number of words in the test corpus.
        sents -- the sentences as a list of tokens.
        """
        l = self.cross_entropy(M, sents)
        return 2**(-l)

class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """

        super(AddOneNGram, self).__init__(n, sents) # heredo de la clase NGram

        v_list = []
        for gram, c in self.counts.items():
            if len(gram) == self.n:
                for i in gram:
                    v_list.append(i)
        v_list = list(set(v_list))
        if '<s>' in v_list:
            v_list.remove('<s>')
        self.v = len(v_list)


    def V(self):
        """Size of the vocabulary.
        """
        return self.v


    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        nom = self.count(tuple(tokens)) + 1.0
        dem = float(self.count(tuple(prev_tokens)) + self.V())
        return nom / dem


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        super(InterpolatedNGram, self).__init__(n, sents) # heredo de la clase NGram

        self.addone = addone
        self.gamma = gamma
        self.counts = counts = defaultdict(int)
        for sent in sents:
            sent = (['<s>'] *(n-1)) + sent # agrego n-1 tags de inicio de oracion
            sent.append('</s>')
            n1 = n
            for _ in range(n):
                for i in range(len(sent) - n1 + 1):
                    ngram = tuple(sent[i: i + n1])
                    counts[ngram] += 1
                    if n1 == 1 and ngram != ('<s>',): # excluyo el <s> para que no me sume muchas veces el ().
                        counts[ngram[:-1]] += 1 # ngram = ().
                n1 -= 1


    def cond_prob_ML(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []

        tokens = prev_tokens + [token]
        if float(self.count(tuple(tokens))) == 0.0:
            p = 0.0
        else:
            p = float(self.count(tuple(tokens))) / self.count(tuple(prev_tokens))
        return p

    def lamb(self, prev_tokens):
        """ calculate a lambda
        """
        prev_tokens = tuple(prev_tokens)
        return self.count(prev_tokens) / (self.count(prev_tokens) + self.gamma)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
#        if self.addone:
#            
#        else:
        p = 0.0
        l = 1.0
        if self.n > 1:
            l = self.lamb(prev_tokens)
        p += l * self.cond_prob_ML(token, prev_tokens)
        v = 1 - l
        for m in range(self.n - 1):
            prev_tokens = prev_tokens[1:]
            if (m + 1) == (self.n - 1): # ultimo lambda
                l = v
            else:
                l = v * self.lamb(prev_tokens)
            p += l * self.cond_prob_ML(token, prev_tokens)
            v = v -l
        return p

class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.n = model.n
        self.counts = model.counts
        self.probs = defaultdict(dict)
        self.sorted_probs = defaultdict(dict)
        for i,k in self.counts.items():
            if len(i) == self.n:
                token = i[-1:][0]
                prev_token = i[:-1]
                p = model.cond_prob(token, list(prev_token))
                self.probs[prev_token][token] = p

        for i,k in self.probs.items():
            m = sorted(k.items(), key =lambda asd: (-asd[1], asd[0]))
            self.sorted_probs[i] = m

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        tokens_list = self.sorted_probs[prev_tokens]
        u = random()
        prob = 0
        for i in range(len(tokens_list)):
            prob += tokens_list[i][1]
            if u <= prob:
                token = tokens_list[i][0]
                return token

    def generate_sent(self):
        """Randomly generate a sentence."""
        sent = []
        tok = ''
        prev_token = ['<s>'] * (self.n -1)
        while sent == [] or tok != '</s>':
            tok = self.generate_token(tuple(prev_token))
            sent.append(tok)
            prev_token.append(tok)
            prev_token = prev_token[1:]
        return sent[:-1]


