# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from operator import itemgetter
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
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]

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

class NGramGenerator:

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
            asd = []
            final = []
            for j in k.items():
                l = list(j)
                l[1] *= -1
                l = tuple(l)
                asd.append(l)

            m = sorted(asd, key=itemgetter(1,0))
            for j in m:
                l = list(j)
                l[1] *= -1
                l = tuple(l)
                final.append(l)

            self.sorted_probs[i] = final

    def generate_sent(self):
        """Randomly generate a sentence."""


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
                break
        return token

