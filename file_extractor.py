# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:31:00 2024

@author: kevinh
"""

import os, shutil

extracted = 0
dupes = 0

def extract(src, dest):
    global extracted, dupes
   
    for item in os.listdir(src):
        s, d = os.path.join(src, item), os.path.join(dest, item)
       
        if os.path.isfile(s):
            if os.path.exists(d):
                dupes += 1
            else:
                shutil.move(s, d)
                extracted += 1
               
        elif os.path.isdir(s):
            extract(s, dest)
   
   
source = input("Enter the path to the folder to extract from:\n> ")
destination = input("Enter the path to the location to extract to:\n> ")

extract(source, destination)

print(f"Successfully extracted {extracted} files!")
print(f"Skipped {dupes} duplicate files")