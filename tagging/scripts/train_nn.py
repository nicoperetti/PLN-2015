from docopt import docopt
import pickle
from corpus.ancora import SimpleAncoraCorpusReader
from tagging.lexicon import Lexicon
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.regularizers import l2
from keras.optimizers import Adam, SGD
import numpy as np
from collections import defaultdict
import os


if __name__ == '__main__':
	# opts = docopt(__doc__)

	# # load the data
	# files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
	# corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
	# sents = list(corpus.tagged_sents())
	# print(len(sents))


	# # load the model
	# # filename = opts['-i']
	# filename = 'models/Lexicon2'
	# f = open(filename, 'rb')
	# model = pickle.load(f)
	# f.close()

	# tagset = model.tagset()

	# tagset_d = defaultdict(int)
	# for i, tag in enumerate(tagset):
	# 	tagset_d[tag] = i
	# print(len(model.tagset()))
	# print(model.tagset())

	# X = []
	# Y = []
	# for sent in sents:
	# 	n = len(sent) - 1
	# 	for i, (word, t) in enumerate(sent):
	# 		x = []
	# 		y = [0 for _ in range(len(tagset))]
	# 		for tag in tagset:
	# 			if i == 0:
	# 				x.append(0.0)
	# 			else:
	# 				x.append(model.out_prob(sent[i-1][0], tag))
	# 			x.append(model.out_prob(word, tag))
	# 			if i == n:
	# 				x.append(0.0)
	# 			else:
	# 				x.append(model.out_prob(sent[i+1][0], tag))
	# 		X.append(x)
	# 		y[tagset_d[t]] = 1
	# 		Y.append(y)

	# # split = int(len(X)*.8)
	# X_val = X[:22481]
	# Y_val = Y[:22481]
	# X_test = X_val[:10]
	# Y_test = Y_val[:10]
	# X = X[22481:]
	# Y = Y[22481:]
	# X = np.array(X)
	# Y = np.array(Y)
	# # print(X.dtype)
	# # X = np.float32(X)
	# # Y = np.float32(Y)
	# # print(X.dtype)
	# X_val = np.array(X_val)
	# Y_val = np.array(Y_val)
	# np.save('X_train_simple', X)
	# np.save('Y_train_simple', Y)
	# np.save('X_val_simple', X_val)
	# np.save('Y_val_simple', Y_val)

	X = np.load('X_train_simple.npy')
	Y = np.load('Y_train_simple.npy')
	X_val = np.load('X_val_simple.npy')
	Y_val = np.load('Y_val_simple.npy')
	
	print(X.shape)
	print(Y.shape)
	# fix random seed for reproducibility
	seed = 7
	np.random.seed(seed)

	# # create model
	# model1 = Sequential()
	# # model1.add(Dense(47, input_dim=188, activation='sigmoid'))
	# model1.add(Dense(47, input_dim=141, init='uniform', activation='sigmoid')
	# # model1.add(Dense(47, init='uniform', activation='sigmoid', W_regularizer=l2(0.01), b_regularizer=l2(0.01)))

	json_file = open('model_1_simple_reg.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	model1 = model_from_json(loaded_model_json)
	# load weights into new model
	model1.load_weights("model_1_simple_reg.h5")
	
	# Compile model
	# model1.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	adam = Adam(lr=0.001)
	model1.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

	# Fit the model
	model1.fit(X, Y, nb_epoch=20, batch_size=20)
	
	scores = model1.evaluate(X_val, Y_val, batch_size=20)
	print("%s: %.2f%%" % (model1.metrics_names[1], scores[1]*100))

	# X_test = np.array(X_test)
	# y = model1.predict(X_test)
	# print(y)
	# print("---------------------------------------------------")
	# print(Y_test)



	print("Saving model to disk")
	model_json = model1.to_json()
	with open("model_2_simple_reg.json", "w") as json_file:
	    json_file.write(model_json)
	# serialize weights to HDF5
	model1.save_weights("model_2_simple_reg.h5")
	print("Saved model to disk")



	# corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', '3LB-CAST/.*\.tbf\.xml')
	# sents = list(corpus.tagged_sents())

	# X = []
	# Y = []
	# for sent in sents:
	# 	n = len(sent) - 1
	# 	for i, (word, t) in enumerate(sent):
	# 		x = []
	# 		y = [0.0 for _ in range(len(tagset))]
	# 		for tag in tagset:
	# 			if i == 0:
	# 				x.append(0.0)
	# 			else:
	# 				x.append(model.out_prob(sent[i-1][0], tag))
	# 			x.append(model.out_prob(word, tag))
	# 			if i == n:
	# 				x.append(0.0)
	# 			else:
	# 				x.append(model.out_prob(sent[i+1][0], tag))
	# 		X.append(x)
	# 		y[tagset_d[t]] = 1.0
	# 		Y.append(y)

	# X = np.array(X)
	# Y = np.array(Y)


	# # evaluate the model
	# scores = model1.evaluate(X, Y)
	# print("%s: %.2f%%" % (model1.metrics_names[1], scores[1]*100))

	# serialize mode omentum=0.9, nesterov=True)
	# print("Saving model to disk"sgd model_json = model1.to_json()
	# with open("model1.json", "w") as json_file:
	#     json_file.write(model_json)
	# # serialize weights to HDF5
	# model1.save_weights("model1.h5")
	# print("Saved model to disk")


	# # load json and create model
	# json_file = open('model1.json', 'r')
	# loaded_model_json = json_file.read()
	# json_file.close()
	# loaded_model = model_from_json(loaded_model_json)
	# # load weights into new model
	# loaded_model.load_weights("model1.h5")
	# print("Loaded model from disk")
	
