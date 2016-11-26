from keras.models import Sequential
from keras.layers import Dense
from keras.layers.advanced_activations import LeakyReLU
import numpy as np


def network_model():
    model = create_model()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


def create_model():
    activation_function = LeakyReLU(alpha=0.2,name='leakyRelu')
    # activation_function = 'sigmoid'

    model = Sequential()

    model.add(Dense(9, input_dim=9, init='normal', activation=activation_function))
    model.add(Dense(64, init='normal', activation=activation_function))
    model.add(Dense(128, init='normal', activation=activation_function))
    model.add(Dense(256, init='normal', activation=activation_function))
    model.add(Dense(9, init='normal', activation='softmax'))

    return model
