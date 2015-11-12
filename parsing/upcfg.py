from collections import defaultdict
from parsing.util import unlexicalize, lexicalize
from nltk.grammar import Nonterminal as N, ProbabilisticProduction, PCFG
from parsing.cky_parser import CKYParser
from nltk.tree import Tree


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, horzMarkov=None, unary=False, start='sentence'):
        """
        parsed_sents -- list of training trees.
        n-- horizontal markovization order
        """
        produc_count = defaultdict(int)
        produc_left_count = defaultdict(int)
        for parsed_sent in parsed_sents:
            uparsed_sent = parsed_sent.copy(deep=True)
            uparsed_sent = unlexicalize(uparsed_sent)
            uparsed_sent.chomsky_normal_form(horzMarkov=horzMarkov)
            if not unary:
                uparsed_sent.collapse_unary(collapsePOS=True, collapseRoot=True)
            prod = uparsed_sent.productions()
            for p in prod:
                produc_count[p] += 1
                produc_left_count[p.lhs()] += 1
        production = [ProbabilisticProduction(p.lhs(), p.rhs(),
                      prob=produc_count[p]/float(produc_left_count[p.lhs()]))
                      for p in produc_count]
        self.grammar = PCFG(N(start), production)
        self.parser = CKYParser(self.grammar)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.grammar.productions()

    def parse(self, tagged_sent):
        """Parse a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        parser = self.parser
        sent, pos_tag = zip(*tagged_sent)
        prob, tree = parser.parse(list(pos_tag))
        if tree is None:
            start = self.grammar.start()
            leaves = [Tree(tag, [word]) for word, tag in tagged_sent]
            result = Tree(repr(start), leaves)
        else:
            result = lexicalize(tree, sent)
            result.un_chomsky_normal_form()
        return result
