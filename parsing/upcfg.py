from collections import defaultdict
from parsing.util import unlexicalize, lexicalize
from nltk.grammar import Nonterminal as N, ProbabilisticProduction, induce_pcfg
from parsing.cky_parser import CKYParser
from nltk.tree import Tree


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='S'):
        """
        parsed_sents -- list of training trees.
        """
        production = []
        produc_count = defaultdict(int)
        produc_left_count = defaultdict(int)

# DOIT pasar a normal_form

        for parsed_sent in parsed_sents:
            uparsed_sent = parsed_sent.copy(deep=True)
            uparsed_sent = unlexicalize(uparsed_sent)
            prod = uparsed_sent.productions()
            for p in prod:
                X = str(p.lhs())
                tupl = (X,)
                for i in p.rhs():
                    tupl += (str(i),)
                produc_count[tupl] += 1
                produc_left_count[X] += 1

        for key, value in produc_count.items():
            X = key[0]
            Y = key[1]
            if len(key) < 3:
                p = produc_count[(X, Y)] / float(produc_left_count[X])
                pp = ProbabilisticProduction(N(X), [Y], prob=p)
            else:
                Z = key[2]
                p = produc_count[(X, Y, Z)] / float(produc_left_count[X])
                pp = ProbabilisticProduction(N(X), [N(Y), N(Z)], prob=p)
            production += [pp]
        self.grammar = induce_pcfg(N(start), production)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.grammar.productions()

    def parse(self, tagged_sent):
        """Parse a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        parser = CKYParser(self.grammar)
        sent, pos_tag = zip(*tagged_sent)
        pos_tag = list(pos_tag)
        prob, tree = parser.parse(pos_tag)
        if tree is None:
            start = self.grammar.start()
            leaves = [Tree(tag, [word]) for word, tag in tagged_sent]
            result = Tree(repr(start), leaves)
        else:
            result = lexicalize(tree, sent)
        return result
