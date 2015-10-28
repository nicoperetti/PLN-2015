from nltk.grammar import PCFG
from collections import defaultdict
from nltk.tree import Tree

class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        produc = grammar.productions()
        self.N = []
        self.lexical_produc = []
        self.nonlexical_produc = []

        for prod in produc:
            self.N.append(repr(prod.lhs()))
            if prod.is_lexical():
                self.lexical_produc.append(prod)
            else:
                self.nonlexical_produc.append(prod)

    def parse(self, sent):
        """Parse a sequence of terminals.
        sent -- the sequence of terminals.
        """
        n = len(sent)
        self._pi = defaultdict(dict)
        self._bp = defaultdict(dict)

        # initialization
        for i, w in enumerate(sent, 1):
            for production in self.lexical_produc:
                if production.rhs()[0] == w:
                    key = (i, i)
                    non_terminal = repr(production.lhs())
                    prob = production.logprob()
                    self._pi[key][non_terminal] = prob
                    tree = Tree(non_terminal, [w])
                    self._bp[key][non_terminal] = tree

        # cky
        for l in range(1, n):
            for i in range(1, (n-l) + 1):
                j = i + l
                for production in self.nonlexical_produc:
                    for s in range(i,j):
                        Y, Z = production.rhs()
                        Y = repr(Y)
                        Z = repr(Z)
                        pi_1_ant = self._pi[(i, s)]
                        pi_2_ant = self._pi[(s+1, j)]
                        if Y in pi_1_ant and Z in pi_2_ant:
                            prob = production.logprob()
                            prob += self._pi[(i, s)][Y] + self._pi[(s+1, j)][Z]
                            X = repr(production.lhs())
                            if X in self._pi[(i,j)]:
                                if prob > self._pi[(i,j)][X]:
                                    self._pi[(i,j)][X] = prob
                            else:
                                self._pi[(i,j)][X] = prob


        for i in self._pi.items():
            print(i)
        print("")
        for i in self._bp.items():
            print(i)



