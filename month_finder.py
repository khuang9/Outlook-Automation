# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:31:51 2024

@author: kevinh
"""

import os

folders = []

def get_folders(src):
    global folders
   
    items = os.listdir(src)
   
    if len(items) > 100:
        return
   
    for item in items:
        s = os.path.join(src, item)
        if os.path.isdir(s):
            folders.append(item)
            print(item)
            get_folders(s)
           

source = input("Enter source:\n> ")
get_folders(source)
print(len(folders))
with open("months.txt", "a", encoding="utf-8") as months, open("discarded.txt", "a", encoding="utf-8") as discarded, open("folds.txt", "a", encoding="utf-8") as folds:
    for fold in folders:
        folds.write(fold)
        folds.write("\n")
       
        foldl = fold.lower()
        if "email" in foldl or "new folder" in foldl or fold[:2] == "20" or fold[-4:-2] == "20" or fold[-5:-3] == "-0" or fold[-5:-3] == "-1":
            discarded.write(fold)
            discarded.write("\n")
        else:
            months.write(fold)
            months.write("\n")