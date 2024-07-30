# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 12:03:19 2024

@author: kevinh
"""

import os, shutil, winsound
from string_compare import match_degree
from colour_text import colour

loading_length = 33
loading_colour = (50, 205, 50)

nums = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def month_format(month_chars, separator, leading_zero=True, num_first=True, month_only=False, num_only=False):
    formatted = ["0"]
   
    for m in range(12):
        if leading_zero:
            num = nums[m]
        else:
            num = int(nums[m])
           
        month = months[m][:month_chars]
       
        if month_only:
            formatted.append(month)
        elif num_only:
            formatted.append(str(num))
        elif num_first:
            formatted.append(f"{num}{sep}{month}")
        else:
            formatted.append(f"{month}{sep}{num}")

    return formatted

sep = input("\nEnter a folder name separator (dash, space, comma, etc.): ")

m4n2 = month_format(9, sep, num_first=False)
n2m4 = month_format(9, sep)
m3n2 = month_format(3, sep, num_first=False)
n2m3 = month_format(3, sep)
m4n1 = month_format(9, sep, leading_zero=False, num_first=False)
n1m4 = month_format(9, sep, leading_zero=False)
m3n1 = month_format(3, sep, leading_zero=False, num_first=False)
n1m3 = month_format(3, sep, leading_zero=False)
m4 = month_format(9, sep, month_only=True)
m3 = month_format(3, sep, month_only=True)
n2 = month_format(0, sep, num_only=True)
n1 = month_format(0, sep, leading_zero=False, num_only=True)

formats = [m4, m3, n2, n1, m4n2, n2m4, m3n2, n2m3, m4n1, n1m4, m3n1, n1m3]

print("\nWhat month format would you like to follow?")
print(" (1)  Full month name only")
print(" (2)  Abbreviated month name only")
print(" (3)  Corresponding number w/ leading zero only")
print(" (4)  Corresponding number w/o leading zero only")
print(" (5)  Full month name + Corresponding number w/ leading zero")
print(" (6)  Corresponding number w/ leading zero + Full month name")
print(" (7)  Abbreviated month name + Corresponding number w/ leading zero")
print(" (8)  Corresponding number w/ leading zero + Abbreviated month name")
print(" (9)  Full month name + Corresponding number w/o leading zero")
print(" (10) Corresponding number w/o leading zero + Full month name")
print(" (11) Abbreviated month name + Corresponding number w/o leading zero")
print(" (12) Corresponding number w/o leading zero + Abbreviated month name\n")

month_folders = formats[int(input("Enter an option #: ")) - 1]

def get_info(name):
    # return customer, year, month
    i1 = name.find("-")
    i2 = -1
    i3 = name.rfind("_")
    
    for i in range(i1 - 1, -1, -1):
      if name[i] == "_":
        i2 = i
        break
      
    return name[i2 + 1 : i1].upper(), name[i3 + 1 : i3 + 5], name[i3 + 5 : i3 + 7]

def get_year(year, folders):
    for f in folders:
        if f[-4:] == year and "852'S" in f.upper() or f == year:
            return f
       
    return year

def get_folder(path):
    folders = os.listdir(path)
   
    for f in folders:
        if f[-5:].lower() == "indicator":
            target = os.path.join(path, f)
            new_path = get_folder(target)
           
            if new_path == target:
                return target
            else:
                return new_path
           
    return path

old_path = input("Enter current directory path:\n> ")
new_path = input("Enter desired directory path:\n> ")
print("-----------------------------------------------------------------------------")
files = os.listdir(old_path)
folders = os.listdir(new_path)

moved = 0
skipped = 0
weird = 0

custs = {}

for file in files:
    customer, year, month = get_info(file)
   
    if customer not in custs:
        best_match, max_match = "", 0
        for folder in folders:
            m_deg = match_degree(customer.upper(), folder.upper())
           
            if m_deg == 1:
                best_match = folder
                max_match = 1
                break
            elif m_deg > max_match:
                best_match = folder
                max_match = m_deg
           
        if max_match > 0.8:
            print(f"Files for {customer} moved to folder '{best_match}'")
        else:
            print(f"Should files for {customer} be moved to folder '{best_match}'?")
            while True:
                correct = input("Press ENTER if the folder is correct or enter the correct folder here if not:\n> ")
                if correct == "":
                    break
                elif correct in folders:
                    best_match = correct
                    break
                else:
                    print(f"ERROR: folder '{correct}' does not exist")
                   
        custs[customer] = best_match
               
    try:
        int(year)
        month = int(month)
    except ValueError:
        weird += 1
    else:
        if int(year) < 2000:
            weird += 1
        else:
            #todo: go through folder and change all ai-detected months to selected format
            # todo: maybe ai to determine whivh folder is which month and standardize all folder names
            # dest = os.path.join(new_path, year, month_folders[month])
            target_dir = get_folder(os.path.join(new_path, custs[customer]))
            dest = os.path.join(target_dir, get_year(year, os.listdir(target_dir)), month_folders[month])
            
            os.makedirs(dest, exist_ok=True)
            if not os.path.exists(os.path.join(dest, file)):
                shutil.move(os.path.join(old_path, file), os.path.join(dest, file))
                moved += 1
                percent = moved/len(files)
                num_slashes = int(loading_length*percent)
                print("\x1b[2K", end="\r")
                print(f"{moved}/{len(files)} files moved.....{'%.2f'%(100*percent)}% [{colour('/'*num_slashes, loading_colour)}{' '*(loading_length - num_slashes)}]", end="\r")
            else:
                skipped += 1

print()
print("-------------------------------------")
print(f"Finished moving {moved} files!")
print(f"Skipped {skipped} duplicate files")
print(f"Skipped {weird} weirdly named files")

freqs = {"C3":131, "C#3":139, "D3":147, "D#3":156, "E3":165, "F3":175, "F#3":185, "G3":196, "G#3":208, "A3":220, "A#3":233, "B3":247,
         "C4":262, "C#4":277, "D4":294, "D#4":311, "E4":330, "F4":349, "F#4":370, "G4":392, "G#4":415, "A4":440, "A#4":466, "B4":494,
         "C5":523, "C#5":554, "D5":587, "D#5":622, "E5":659, "F5":698, "F#5":740, "G5":784, "G#5":831, "A5":880, "A#5":932, "B5":988, }

song = ["C4", "D4", "C4", "A3", "A3", "A3", "G3", "A3", "A#3", "A3"]
for note in song:
    winsound.Beep(freqs[note], 1000)