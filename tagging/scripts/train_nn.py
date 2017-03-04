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

	# fix random seed for reproducibility
	seed = 7
	np.random.seed(seed)

	# create model
	model = Sequential()
	model.add(Dense(48, input_dim=144, init='uniform', activation='sigmoid'))

	# json_file = open('tagging/models/cnn_model_3.json', 'r')
	# loaded_model_json = json_file.read()
	# json_file.close()
	# model = model_from_json(loaded_model_json)
	# # load weights into new model
	# model.load_weights("tagging/models/cnn_weights_3.h5")
	
	# Compile model
	adam = Adam(lr=0.1)
	model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

	# Fit the model
	model.fit(X_train, Y_train, nb_epoch=28, batch_size=20)
	
	scores = model.evaluate(X_train, Y_train, batch_size=20)
	print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

	print("Saving model to disk")
	model_json = model.to_json()
	with open("tagging/models/cnn_model_2.json", "w") as json_file:
	    json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("tagging/models/cnn_weights_2.h5")
	print("Saved model to disk")
