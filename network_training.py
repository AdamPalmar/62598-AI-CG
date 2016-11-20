from keras.models import Sequential
from keras.layers import Dense
import numpy as np


def network_model():
    model = Sequential()
    model.add(Dense(12, input_dim=9, init='uniform', activation='relu'))
    model.add(Dense(32, init='uniform', activation='relu'))
    model.add(Dense(32, init='uniform', activation='relu'))
    model.add(Dense(9, init='uniform', activation='softmax'))

    model.compile(loss='mean_squared_error', optimizer='adam')

    return model