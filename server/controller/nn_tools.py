from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
import os
import numpy as np

import json

MAX_SEQUENCE_LENGTH = 30
model=None
tokenizer=None
NEURAL_NETWORK_DIR='./neural_network'

def init():
    global model, tokenizer
    model = load_model(os.path.join(NEURAL_NETWORK_DIR,'model.h5'))
    with open(os.path.join(NEURAL_NETWORK_DIR,'tokenizer.pickle'), 'rb') as handle:
        tokenizer = pickle.load(handle)


def predict(text):
    sequences = tokenizer.texts_to_sequences([text])
    data_int = pad_sequences(sequences, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH - 5))
    data = pad_sequences(data_int, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
    prediction_ar = model.predict(data)
    return prediction_ar


def get_summary(predictions):
    pr = np.array(predictions)
    means = np.mean(pr, axis=0)
    emotions = np.argmax(pr, axis=2)
    unique, counts = np.unique(emotions, axis=0, return_counts=True)
    n_unique = list(map(lambda x: str(x),unique.ravel()))
    n_counts = list(map(lambda x: int(x), counts))
    stat = dict(zip(n_unique, n_counts))
    for i in range(5):
        if not stat.get(str(i)):
            stat[str(i)] = 0
    percents = {k: int(v/len(pr)*100) for k, v in stat.items()}
    #print(predictions)
    # predictions = list(map(lambda x: int(x*100)/100, predictions))
    js = json.dumps({
        'means':means.tolist(),
        'emotions': emotions.tolist(),
        'counts': stat,
        'precents': percents,
        'predictions': np.around(predictions, decimals=2).tolist()
    })
    return js


def get_predictions(filepath):
    if not model:
        init()
    data = read_data(filepath)
    predictions = []
    for sample in data:
        predictions.append(predict(sample).tolist())
    return get_summary(predictions)


def read_data(filepath):
    filename, file_extension = os.path.splitext(filepath)
    if file_extension == ".csv":
        with open(filepath) as csvfile:
            data = csvfile.readlines()
            return data

ar = [[[0.23425, 0.2341, 0.43542, 0.3453, 0.3454]],[[0.9345, 0.3458, 0.7345, 0.3456, 0.3454]], [[0.5345, 0.2324, 0.3435345, 0.9435345, 0.4234]]]
get_summary(ar)