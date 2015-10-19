from tagging.features import History

class MEMM:

    def __init__(self, n, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.
        tagged_sents -- the corpus (a list of sentences)
        """
        result = []
        for tagged_sent in tagged_sents:
            h = self.sent_histories(tagged_sent)
            result += h
        return result

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        sent = list(zip(*tagged_sent))[0]
        tag = list(zip(*tagged_sent))[1]
        tag = ('<s>',) * (n-1) + tag
        l = len(sent)
        result = []
        for i in range(l):
            prev_tag = tag[i:i+n-1]
            h = History(list(sent), prev_tag, i)
            result.append(h)
        return result

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.
        tagged_sents -- the corpus (a list of sentences)
        """
        result = []
        for tagger_sent in tagged_sents:
            result += self.sent_tags(tagger_sent)
        return result

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        tags = list(zip(*tagged_sent))[1]
        return tags

    def tag(self, sent):
        """Tag a sentence.
        sent -- the sentence.
        """

    def tag_history(self, h):
        """Tag a history.
        h -- the history.
        """

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
