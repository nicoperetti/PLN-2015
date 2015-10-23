from collections import defaultdict

class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        dict_t = defaultdict(dict)
        tag_frec = defaultdict(int)
        for tagged_sent in tagged_sents:
            for k, v in tagged_sent:
                tag_frec[v] += 1
                if k in dict_t and v in dict_t[k]:
                    dict_t[k][v] += 1
                else:
                    dict_t[k][v] = 1


# busco el tag mas frecuente
        m = sorted(tag_frec.items(), key = lambda sor: -sor[1])
        self.tag_more_frec = m[0][0]
# busco los tags mas frecuentes para cada palabra
        self.tag_dict = defaultdict(str)
        for k, v in dict_t.items():
            parcial_v = sorted(v.items(), key = lambda sor: -sor[1])
            self.tag_dict[k] = parcial_v[0][0]

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.
        w -- the word.
        """
        if self.unknown(w):
            tag = self.tag_more_frec
        else:
            tag = self.tag_dict[w]
        return tag

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        result = False
        word = self.tag_dict[w]
        if word == "":
            result = True
        return result
