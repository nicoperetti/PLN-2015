import pickle
from collections import defaultdict
from corpus.ancora import SimpleAncoraCorpusReader
import numpy as np
import random



def preprocess(model, sents):
	tagset = model.tagset()

	tagset_d = defaultdict(int)
	for i, tag in enumerate(tagset):
		tagset_d[tag] = i

	X = []
	Y = []
	for sent in sents:
		n = len(sent) - 1
		for i, (word, t) in enumerate(sent):
			x = []
			y = [0 for _ in range(len(tagset))]
			for tag in tagset:
				if i == 0:
					x.append(0.0)
				else:
					x.append(model.out_prob(sent[i-1][0], tag))
				x.append(model.out_prob(word, tag))
				if i == n:
					x.append(0.0)
				else:
					x.append(model.out_prob(sent[i+1][0], tag))
			X.append(x)
			y[tagset_d[t]] = 1
			Y.append(y)
	return X, Y


if __name__ == '__main__':

	# load thel lexicon
	filename = 'models/Lexicon1'
	f = open(filename, 'rb')
	model = pickle.load(f)
	f.close()

	# load the data
	files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
	corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
	sents1 = list(corpus.tagged_sents())

	files = '3LB-CAST/.*\.tbf\.xml'
	corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
	sents2 = list(corpus.tagged_sents())	
	sents = sents1 + sents2
	n = len(sents)
	print(n)

	random.seed(7)
	random.shuffle(sents)

	split = int(n*.9)
	train_sent = sents[:split]
	# test_sent = sents[split:]
	x_train_data, y_train_data = preprocess(model, train_sent)
	# x_test_data, y_test_data = preprocess(model, sents[split:])

	assert len(x_train_data) == len(y_train_data)
	# assert len(x_test_data) == len(y_test_data)
	print(len(x_train_data))
	# print(len(x_test_data))

	x_train_data = np.float32(x_train_data)
	y_train_data = np.float32(y_train_data)
	# x_test_data = np.float32(x_test_data)
	# y_test_data = np.float32(y_test_data)

	#save values
	np.save('tagging/features/X_train_3-4.feat', x_train_data)
	np.save('tagging/features/Y_train_3-4.feat', y_train_data)
	# np.save('tagging/features/X_test.feat', x_test_data)
	# np.save('tagging/features/Y_test.feat', y_test_data)


