# https://docs.python.org/3/library/collections.html
from collections import defaultdict


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
            if self.n != 1:
                sent = ['<s>'] + sent
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
        if n == 1: # unigramas
            for token in sent:
                prob_sent *= self.cond_prob(token)
                if prob_sent == 0: # si es cero termino
                    break
        else: # n-gramas
            prev_token = ['<s>']
            for token in sent: 
                prob_sent *= self.cond_prob(token, prev_token)
                prev_token.append(token)
                if len(prev_token) == n: # tengo que sacar un token de los previos
                    prev_token = prev_token[1:]
                if prob_sent == 0: # si es cero termino
                    break
        return prob_sent














