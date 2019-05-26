from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import pickle

MAX_SEQUENCE_LENGTH = 30

def predict(text):
    model = load_model('../neural_network/model.h5')
    with open('../neural_network/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    sequences = tokenizer.texts_to_sequences([text])
    data_int = pad_sequences(sequences, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH - 5))
    data = pad_sequences(data_int, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
    prediction_ar = model.predict(data)
    return prediction_ar