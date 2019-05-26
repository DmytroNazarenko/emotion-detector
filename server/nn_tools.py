from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import pickle
import os
import csv

MAX_SEQUENCE_LENGTH = 30
model=None
tokenizer=None

def init():
    global model, tokenizer
    model = load_model('../neural_network/model.h5')
    with open('../neural_network/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)


def predict(text):
    sequences = tokenizer.texts_to_sequences([text])
    data_int = pad_sequences(sequences, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH - 5))
    data = pad_sequences(data_int, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
    prediction_ar = model.predict(data)
    return prediction_ar


def get_predictions(filepath):
    init()
    data = read_data(filepath)
    predictions = []
    for sample in data:
        predictions.append(predict(sample))
    return predictions


def read_data(filepath):
    filename, file_extension = os.path.splitext(filepath)
    if file_extension == ".csv":
        with open(filepath) as csvfile:
            data = csvfile.readlines()
            return data
