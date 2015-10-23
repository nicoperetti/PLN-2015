from tagging.features import *
from sklearn.pipeline import Pipeline
from featureforge.vectorizer import Vectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

class MEMM:

    def __init__(self, n, tagged_sents, clf='LR'):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """

        self.n = n
        words_voc = []
        for tagged_sent in tagged_sents:
            if len(tagged_sent) > 0:
                words_voc += list(zip(*tagged_sent))[0]
        words_voc = set(words_voc)
        self.words_voc = words_voc

        f = [word_lower, word_istitle, word_isupper, word_isdigit]
        f_p_w = [PrevWord(i) for i in f]
        f_np_t = [NPrevTags(i) for i in range(1,n)]
        features = f_p_w + f_np_t + f
        vect = Vectorizer(features)
        if clf == 'LSVC':
            clas = LinearSVC()
        elif clf == 'MNB':
            clas = MultinomialNB()
        else:
            clas = LogisticRegression()
        self.p = Pipeline([('vect',vect),('clas',clas)])
        hs = self.sents_histories(tagged_sents)
        tgs = self.sents_tags(tagged_sents)
        self.p.fit(hs, tgs)

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.
        tagged_sents -- the corpus (a list of sentences)
        """
        result = []
        for tagged_sent in tagged_sents:
            if len(tagged_sent) > 0:
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
            if len(tagger_sent) > 0:
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
        prev_tags = ('<s>',) * (self.n - 1)
        result = []
        for i in range(len(sent)):
            history = History(sent, prev_tags, i)
            tag = self.tag_history(history)
            result += tag
            prev_tags += tuple(tag)
            prev_tags = prev_tags[1:]
        return result

    def tag_history(self, h):
        """Tag a history.
        h -- the history.
        """
        pipe = self.p
        return pipe.predict([h])


    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        result = True
        if w in self.words_voc:
            result = False
        return result
