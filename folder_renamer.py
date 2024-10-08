# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 17:43:37 2024

@author: kevinh
"""

import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from string_compare import match_degree
from colour_text import colour


folder_type = "modeltype"
folder_month = "modelmonth"

model_type = load_model(os.path.join(folder_type, "model.keras"))
model_month = load_model(os.path.join(folder_month, "model2.keras"))

with open(os.path.join(folder_type, "tokenizer.json"), "r") as t1, open(os.path.join(folder_month, "tokenizer2.json")) as t2:
    tokenizer_type = tokenizer_from_json(t1.read())
    tokenizer_month = tokenizer_from_json(t2.read())
    
    
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
new_names = ["01 January", "02 February", "03 March", "04 April", "05 May", "06 June", "07 July", "08 August", "09 September", "10 October", "11 November", "12 December"]
            
def process_month(inp, num_spaces, pad_dash=True, pop_years=False):
    if pad_dash:
        if "-" in inp:
            dash_ind = inp.index("-")
            inp = inp[:dash_ind] + " - " + inp[dash_ind + 1:]
    
    words = inp.split()
    
    for i in range(len(words)):
        try:
            int(words[i])
        except ValueError:
            continue
        else:
            if 2000 < int(words[i]) < 3000:
                if pop_years:
                    words.pop(i)
            else:
                if i == len(words) - 1:
                    words[i] += " " * num_spaces
                else:
                    words[i] += " " * (num_spaces - 1)
                
    return " ".join(words)


def predict_month(inp):
    inp = process_month(inp, 5, pop_years=True)
    
    max_len = 30
    inp_padded = pad_sequences(tokenizer_month.texts_to_sequences([inp]), maxlen=max_len)
    
    prediction = model_month.predict(inp_padded, verbose=0)
    for i in range(len(prediction[0])):
        prediction[0][i] = (prediction[0][i] + match_degree(inp.lower(), months[i].lower())) / 2
        
    prediction = new_names[np.argmax(prediction)]
    return prediction

def predict_type(inp):
    try:
        int(inp)
    except ValueError:
        pass
    else:
        if len(inp) == 2 and 1 <= int(inp) <= 12:
            return "Month"
    
    max_match = 0
    for month in months:
        max_match = max(max_match, match_degree(inp.lower(), month.lower(), strip_puncs=True, strip_nums=True))
    
    inp = process_month(inp, 1)
    max_len = 50
    inp = pad_sequences(tokenizer_type.texts_to_sequences([inp]), maxlen=max_len)
    
    options = ["Month", "Not month"]
    prediction = options[round((1 - max_match + model_type.predict(inp, verbose=0)[0][0]) / 2)]
    return prediction


def rename_folders(src):
    items = next(os.walk(src))[1]
    
    for item in items:
        s = os.path.join(src, item)
        
        if predict_type(item) == "Month" and item not in new_names:
            new_name = predict_month(item)
            if new_name in items:
                print(f"{src}{os.sep}{colour(item, (0, 255, 255))} left as is\n")
                rename_folders(s)
            else:
                print(f"{src}{os.sep}{colour(item, (255, 0, 0))} renamed to {colour(new_name, (0, 255, 0))}\n")
                os.rename(s, os.path.join(src, new_name))
                rename_folders(os.path.join(src, new_name))
        else:
            print(f"{src}{os.sep}{colour(item, (0, 255, 255))} left as is\n")
            rename_folders(s)
                
           
source = input("Enter desired directory to change names in:\n> ")
rename_folders(source)