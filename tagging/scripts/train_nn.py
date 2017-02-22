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

	# load features
	X_train = np.load('tagging/features/X_train.feat.npy')
	Y_train = np.load('tagging/features/Y_train.feat.npy')


	# split in train and validation set
	# print(len(X_train))
	# split = int(len(X_train)*.9)
	# X_train = X_train[:split]
	# Y_train = Y_train[:split]
	# X_val = X_train[split:]
	# Y_val = Y_train[split:]
	
	print(X_train.shape)
	print(Y_train.shape)
	# print(X_val.shape)
	# print(Y_val.shape)
	


	# fix random seed for reproducibility
	seed = 7
	np.random.seed(seed)

	# create model
	# model = Sequential()
	# model.add(Dense(48, input_dim=144, init='uniform', activation='sigmoid'))
	# model.add(Dense(48, init='uniform', activation='sigmoid'))

	# model.add(Dense(48, input_dim=192, init='uniform', activation='sigmoid'))
	# model.add(Dense(48, init='uniform', activation='sigmoid'))

	json_file = open('models/cnn_model_5h.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	model = model_from_json(loaded_model_json)
	# load weights into new model
	model.load_weights("models/cnn_weights_5h.h5")
	
	# Compile model
	adam = Adam(lr=0.0001)
	model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

	# Fit the model
	model.fit(X_train, Y_train, nb_epoch=5, batch_size=100)
	
	scores = model.evaluate(X_train, Y_train, batch_size=100)
	print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

	print("Saving model to disk")
	model_json = model.to_json()
	with open("models/cnn_model_6h.json", "w") as json_file:
	    json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("models/cnn_weights_6h.h5")
	print("Saved model to disk")
