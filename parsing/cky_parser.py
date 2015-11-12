from collections import defaultdict
from nltk.tree import Tree


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        produc = grammar.productions()
        self.start = repr(grammar.start())
        self.lexical_produc = defaultdict(list)
        self.nonlexical_produc = defaultdict(list)
        self.nonlexical_unary_produc = defaultdict(list)
        self.unary = False

        for prod in produc:
            if prod.is_lexical():
                x_i = prod.rhs()[0]
                self.lexical_produc[x_i].append(prod)
            else:
                if self.is_unary(prod):
                    Y = str(prod.rhs()[0])
                    self.nonlexical_unary_produc[Y].append(prod)
                else:
                    Y, Z = self.get_param(prod, 'right')
                    self.nonlexical_produc[(Y, Z)].append(prod)
        if len(self.nonlexical_unary_produc) > 0:
            self.unary = True
            self.nonlexical_unary_produc = dict(self.nonlexical_unary_produc)

    def is_unary(self, production):
        result = False
        if len(production.rhs()) == 1:
            result = True
        return result

    def get_param(self, production, option):
        if option == 'left':
            result = str(production.lhs())
        elif option == 'right':
            p = production.rhs()
            Y = str(p[0])
            Z = str(p[1])
            result = (Y, Z)
        else:
            result = production.logprob()
        return result

    def parse(self, sent):
        """Parse a sequence of terminals.
        sent -- the sequence of terminals.
        """
        n = len(sent)
        self._pi = defaultdict(dict)
        self._bp = defaultdict(dict)
        lp = 0.0
        t = None

        # initialization
        for i, w in enumerate(sent, 1):
            for production in self.lexical_produc[w]:
                key = (i, i)
                non_terminal = self.get_param(production, 'left')
                prob = self.get_param(production, 'prob')
                self._pi[key][non_terminal] = prob
                tree = Tree(non_terminal, [w])
                self._bp[key][non_terminal] = tree

            # handle unary
            if self.unary:
                added = True
                while added:
                    added = False
                    pi_ant = self._pi[(i,i)]
                    bp_ant = self._bp[(i,i)]
                    dict_pi_ant = dict(pi_ant)
                    for B, prob in dict_pi_ant.items():
                        if B in self.nonlexical_unary_produc:
                            prod = self.nonlexical_unary_produc[B]
                            for production in prod:
                                A = self.get_param(production, 'left')
                                p = prob + self.get_param(production, 'prob')
                                if (A not in dict_pi_ant) or (p > dict_pi_ant[A]):
                                    pi_ant[A] = p
                                    leave = bp_ant[B]
                                    tree = Tree(A, [leave])
                                    bp_ant[A] = tree
                                    added = True

        # cky
        for l in range(1, n):
            for i in range(1, (n-l) + 1):
                j = i + l
                key = (i, j)
                for s in range(i, j):
                    pi_1_ant = self._pi[(i, s)]
                    pi_2_ant = self._pi[(s+1, j)]
                    izq = self._bp[(i, s)]
                    der = self._bp[(s+1, j)]
                    for Y, prob_pi_1 in pi_1_ant.items():
                        for Z, prob_pi_2 in pi_2_ant.items():
                            prod = self.nonlexical_produc[(Y, Z)]
                            for production in prod:
                                X = self.get_param(production, 'left')
                                prob = self.get_param(production, 'prob')
                                prob += prob_pi_1 + prob_pi_2
                                if X in self._pi[key]:
                                    if prob > self._pi[key][X]:
                                        self._pi[key][X] = prob
                                        tree = Tree(X, [izq[Y], der[Z]])
                                        self._bp[key][X] = tree
                                else:
                                    self._pi[key][X] = prob
                                    tree = Tree(X, [izq[Y], der[Z]])
                                    self._bp[key][X] = tree
                # handle unary
                if self.unary:
                    added = True
                    while added:
                        added = False
                        pi_ant = self._pi[key]
                        bp_ant = self._bp[key]
                        dict_pi_ant = dict(pi_ant)
                        for B, prob in dict_pi_ant.items():
                            if B in self.nonlexical_unary_produc:
                                prod = self.nonlexical_unary_produc[B]
                                for production in prod:
                                    A = self.get_param(production, 'left')
                                    p = prob + self.get_param(production, 'prob')
                                    if (A not in dict_pi_ant) or (p > dict_pi_ant[A]):
                                        pi_ant[A] = p
                                        leave = bp_ant[B]
                                        tree = Tree(A, [leave])
                                        bp_ant[A] = tree
                                        added = True

        if self.start in self._pi[(1, n)]:
            lp = self._pi[(1, n)][self.start]
            t = self._bp[(1, n)][self.start]
        return (lp, t)
