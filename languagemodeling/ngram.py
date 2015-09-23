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

    def cross_entropy(self, M, sents):
        """M -- total number of words in the test corpus.
        sents -- the sentences as a list of tokens.
        """
        l = 0.0
        for sent in sents:
            l += self.sent_log_prob(sent)
        return l/M

    def perplexity(self, sents):
        """
        sents -- the sentences as a list of tokens.
        """
        M = 0 # total number of words in the test corpus
        for sent in sents:
            M += len(sent)
        l = self.cross_entropy(M, sents)
        return 2**(-l)


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
            m = sorted(k.items(), key =lambda sor: (-sor[1], sor[0]))
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


class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        super(AddOneNGram, self).__init__(n, sents) # heredo de la clase NGram

# vocabulario
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


class Intermediate(AddOneNGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        super(Intermediate, self).__init__(n, sents)

        self.counts = counts = defaultdict(int)

        # calculo los counts
        for sent in sents:
            sent = (['<s>'] *(n-1)) + sent # agrego n-1 tags de inicio de oracion
            sent.append('</s>')
            n1 = n
            for _ in range(n):
                for i in range(len(sent) - n1 + 1):
                    ngram = tuple(sent[i: i + n1])
                    counts[ngram] += 1
                    if n1 == 1:
                        counts[ngram[:-1]] += 1 # ngram = ().
                tag_st = tuple(['<s>'] *(n1-1))
                if tag_st != ():
                    counts[tag_st] += 1
                n1 -= 1
                sent = sent[1:]

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

    def cond_prob_addone(self, token, prev_tokens=None):
        """Conditional probability of a token with smoothing addone.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []

        tokens = prev_tokens + [token]
        p = float(self.count(tuple(tokens)) + 1) / (self.count(tuple(prev_tokens)) + self.V())
        return p


class InterpolatedNGram(Intermediate):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """

        if not gamma:
            held_out = sents[int(90*len(sents)/100):]
            sents = sents[:int(90*len(sents)/100)]

        super(InterpolatedNGram, self).__init__(n, sents) # heredo de la clase NGram

        self.addone = addone

# calculo de gamma
        if not gamma:
            self.gamma = 1
            pp1 = self.perplexity(held_out)
            result = self.gamma
            for _ in range(5): # DOIT mejorar esto
                self.gamma += 200 # DOIT elejir algo mejor
                pp2 = self.perplexity(held_out)
                if pp2 < pp1:
                    result = self.gamma
                    pp1 = pp2
            self.gamma = result
        else:
            self.gamma = gamma

    def lamb(self, prev_tokens):
        """ calculate a lambda
        """
        if not prev_tokens:
            prev_tokens = []
        prev_tokens = tuple(prev_tokens)
        return self.count(prev_tokens) / (self.count(prev_tokens) + self.gamma)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        p = 0.0
        l = 1.0
        if self.n > 1:
            l = self.lamb(prev_tokens)
            p += l * self.cond_prob_ML(token, prev_tokens)
        else:
            if self.addone:
                p += l * self.cond_prob_addone(token, prev_tokens)
            else:
                p += l * self.cond_prob_ML(token, prev_tokens)
        v = 1 - l

        for m in range(self.n - 1):
            prev_tokens = prev_tokens[1:]
            if (m + 1) == (self.n - 1): # ultimo lambda
                l = v
            else:
                l = v * self.lamb(prev_tokens)

            if (m + 1) == (self.n - 1) and self.addone:
                p += l * self.cond_prob_addone(token, prev_tokens)
            else:
                p += l * self.cond_prob_ML(token, prev_tokens)
            v = v -l
        return p


class BackOffNGram(Intermediate):

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """

        if beta == None:
            held_out = sents[int(90*len(sents)/100):]
            sents = sents[:int(90*len(sents)/100)]

        super(BackOffNGram, self).__init__(n, sents) # heredo de la clase NGram

        self.addone = addone

# calculo de beta
        if beta == None:
            self.beta = 0.0
            pp1 = self.perplexity(held_out)
            result = self.beta
            for _ in range(10): # DOIT mejorar esto
                self.beta += 0.1 # DOIT elejir algo mejor
                pp2 = self.perplexity(held_out)
                if pp2 < pp1:
                    result = self.beta
                    pp1 = pp2
            self.beta = result
        else:
            self.beta = beta

# armo el diccionario A
        self.dict_A = defaultdict(dict)
        for key, c in self.counts.items():
            if len(key) > 1: # necesito todas mayores a 1
                k = list(key)
                if k[-1:][0] != '<s>': # mejorar esto muy feo
                    self.dict_A[tuple(k[:-1])][k[-1:][0]] = 1

# calculo los alphas
        self.dict_alpha = defaultdict(int)
        list_counts = dict(self.counts.items())
        list_counts = list_counts.keys()
        list_counts = sorted(list_counts, key =len)
        list_counts = list_counts[1:] # saco la tupla vacia
        for tokens in list_counts:
            list_A = list(self.A(tokens))
            if len(list_A) == 0:
                self.dict_alpha[tokens] = 0.0
            else:
                self.dict_alpha[tokens] = self.beta * len(list_A) / float(self.counts[tokens])

# calculo los denom
        self.dict_denom = defaultdict(int)
        list_counts = dict(self.counts.items())
        list_counts = list_counts.keys()
        list_counts = sorted(list_counts, key =len)
        list_counts = list_counts[1:] # saco la tupla vacia
        for tokens in list_counts:
            list_A = list(self.A(tokens))
            prev_tokens = list(tokens)
            p = 0
            for tok in list_A:
                p += self.cond_prob(tok, prev_tokens[1:])
            self.dict_denom[tokens] = 1 - p


    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        tokens_list = self.dict_A[tokens]
        return set(tokens_list)

    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        if self.beta == 0:
            result = 0
        else:
            result = 1
        if self.dict_alpha[tokens] != 0:
            result = self.dict_alpha[tokens]
        return result

    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        result = 1
        if self.dict_denom[tokens] != 0:
            result = self.dict_denom[tokens]
        return result

    def cond_prob_unigram(self, token):
        """Conditional probability of a token for unigram.
        token -- the token.
        """
        if self.addone:
            c_p = self.cond_prob_addone(token)
        else:
            c_p = self.cond_prob_ML(token)
        return c_p

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """

        if self.n == 1 or not prev_tokens:
            result = self.cond_prob_unigram(token)
        else:
            p_tok = tuple(prev_tokens)
            list_A = list(self.A(p_tok))
            if token in list_A:
                tokens = p_tok + (token,)
                result = (self.count(tokens) - self.beta) / float(self.count(p_tok))
            else:
                if len(prev_tokens) > 1:
                    c_p = self.cond_prob(token, prev_tokens[1:])
                else:
                    c_p = self.cond_prob_unigram(token)
                alp = self.alpha(p_tok)
                d = self.denom(p_tok)
                if c_p == 0:
                    result = 0.0
                else:
                    result = alp * (c_p / d)
        return result

