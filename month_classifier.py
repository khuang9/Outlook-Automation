# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:00:44 2024

@author: kevinh
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from random import shuffle

names = []
labels = []

with open("file.txt", "r") as f:
    fr = [r.rstrip() for r in f.readlines()]
    
for r in fr:
    slash_index = r.rfind("/")
    names.append(r[:slash_index])
    labels.append(int(r[slash_index + 1:]) - 1)
    
indices = [i for i in range(len(names))]
shuffle(indices)
names = [names[ni] for ni in indices]
labels = [labels[li] for li in indices]


max_len = 30
max_words = 62
training_size = int(len(names) * 0.65)
epochs = 50

tokenizer = Tokenizer(num_words=max_words, char_level=True, oov_token="!!OOV!!")
tokenizer.fit_on_texts(names)

seq = tokenizer.texts_to_sequences(names)
pad = pad_sequences(seq, maxlen=max_len, padding="post", truncating="post")

n_train = pad[:training_size]
n_test = pad[training_size:]

l_train = np.array(labels[:training_size])
l_test = np.array(labels[training_size:])

model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(max_words, 64, input_shape=(max_len,)),
    tf.keras.layers.Conv1D(128, 3, activation="relu"),
    tf.keras.layers.GlobalMaxPooling1D(),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(12, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(n_train, l_train, epochs=epochs, validation_data=(n_test, l_test))

with open("tokenizer2.json", "w") as f:
    f.write(tokenizer.to_json())
    
model.save("model2.keras")
