from math import log2
from collections import defaultdict
from random import shuffle
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np

class CnnTagger:

    def __init__(self, lexicon):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.lexicon = lexicon
        self.tagset = self.lexicon.tagset()
        print(self.tagset)
        self.model = self.load_model()
        self.tagset_d = {}
        for i, tag in enumerate(self.tagset):
            self.tagset_d[i] = tag

    def load_model(self):
        # load json and create model
        json_file = open('model_2_simple_reg.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model_2_simple_reg.h5")
        print("Loaded model from disk")
        loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return loaded_model

    def preprocess(self, sent):
        X = []
        n = len(sent) - 1
        for i, word in enumerate(sent):
            x = []
            for tag in self.tagset:
                if i == 0:
                    x.append(0.0)
                else:
                    x.append(self.lexicon.out_prob(sent[i-1], tag))
                x.append(self.lexicon.out_prob(word, tag))
                if i == n:
                    x.append(0.0)
                else:
                    x.append(self.lexicon.out_prob(sent[i+1], tag))
            X.append(x)
        X = np.array(X)
        return X

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """        
        X = self.preprocess(sent)
        Y = self.model.predict(X)
        Y = [y.argmax() for y in Y]
        Y = [self.tagset_d[y] for y in Y]
        return Y