# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:31:00 2024

@author: kevinh
"""

import os, shutil, winsound
from range_finder import get_range
from colour_text import colour

loading_length = 33
loading_colour = (0, 255, 0)

extracted = 0
dupes = 0
folder_num = 1
folders = []
selected_folders = []
total_files = 0

percent = 0
num_slashes = 0

def list_folders(src):
    global folder_num, total_files
   
    for item in os.listdir(src):
        s = os.path.join(src, item)
        if os.path.isdir(s):
            print(f"({folder_num}) {s}")
            folders.append(s)
            folder_num += 1
            list_folders(s)
        elif os.path.isfile(s):
            total_files += 1
   
def extract(src, dest, custom=False):
    global extracted, dupes
   
    for item in os.listdir(src):
        s, d = os.path.join(src, item), os.path.join(dest, item)
       
        if os.path.isfile(s):
            if os.path.exists(d):
                dupes += 1
            else:
                shutil.move(s, d)
                extracted += 1
                percent = extracted/total_files
                num_slashes = int(loading_length*percent)
                
            print("\x1b[2K", end="\r")
            print(f"{extracted}/{total_files} items extracted.....{'%.2f'%(100*percent)}% [{colour('/'*num_slashes, loading_colour)}{' '*(loading_length - num_slashes)}] | {dupes} duplicates found", end="\r")
               
        elif os.path.isdir(s):
            if not custom or s in selected_folders:
                extract(s, dest, custom=custom)
   
   
source = input("Enter the path to the folder to extract from:\n> ")
destination = input("Enter the path to the location to extract to:\n> ")

print("\nFolders:")
list_folders(source)
#todo: maybe let user decide on specific range of folders in printed list to extract from
print("-------------------------------------")

choice = input("Proceed? (y/n)\nOr enter 'c' for custom selection\n> ").lower()
if choice == "n":
    print("Operation terminated successfully!")
else:
    if choice == "y":
        extract(source, destination)
    else:
        selection = get_range(input("Enter a custom selection (Ex: 1-3,5,7-9)\n> "))
        while selection == None:
            selection = get_range(input("> "))
           
        selected_folders = [folders[n-1] for n in selection]
        extract(source, destination, custom=True)
           
    print()
    print("-------------------------------------")
    print(f"Successfully extracted {extracted} files!")
    print(f"Skipped {dupes} duplicate files")
   
    freqs = {"C3":131, "C#3":139, "D3":147, "D#3":156, "E3":165, "F3":175, "F#3":185, "G3":196, "G#3":208, "A3":220, "A#3":233, "B3":247,
             "C4":262, "C#4":277, "D4":294, "D#4":311, "E4":330, "F4":349, "F#4":370, "G4":392, "G#4":415, "A4":440, "A#4":466, "B4":494,
             "C5":523, "C#5":554, "D5":587, "D#5":622, "E5":659, "F5":698, "F#5":740, "G5":784, "G#5":831, "A5":880, "A#5":932, "B5":988, }
   
    song = ["C4", "D4", "C4", "A3", "A3", "A3", "G3", "A3", "A#3", "A3"]
    for note in song:
        winsound.Beep(freqs[note], 1000)