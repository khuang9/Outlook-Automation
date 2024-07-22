# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 12:03:19 2024

@author: kevinh
"""

import os, shutil
from string_compare import match_degree

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
print(" (1)  Full month name only")
print(" (2)  Abbreviated month name only")
print(" (3)  Corresponding number w/ leading zero only")
print(" (4)  Corresponding number w/o leading zero only")
print(" (5)  Full month name + Corresponding number w/ leading zero")
print(" (6)  Corresponding number w/ leading zero + Full month name")
print(" (7)  Abbreviated month name + Corresponding number w/ leading zero")
print(" (8)  Corresponding number w/ leading zero + Abbreviated month name")
print(" (9)  Full month name + Corresponding number w/o leading zero")
print(" (10) Corresponding number w/o leading zero + Full month name")
print(" (11) Abbreviated month name + Corresponding number w/o leading zero")
print(" (12) Corresponding number w/o leading zero + Abbreviated month name\n")

month_folders = formats[int(input("Enter an option #: ")) - 1]

def get_info(name):
    # return customer, year, month
    i1 = name.find("-")
    i2 = name.rfind("_")
    return name[8 : i1].upper(), name[i2 + 1 : i2 + 5], int(name[i2 + 5 : i2 + 7])

old_path = input("Enter current directory path:\n> ")#"TBD" #POS directory
new_path = input("Enter desired directory path:\n> ")
print("-----------------------------------------------------------------------------")
files = os.listdir(old_path)
folders = os.listdir(new_path)

moved = 0
skipped = 0

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
                
    dest = os.path.join(new_path, year, month_folders[month])
    # dest = os.path.join(new_path, custs[customer], year, month_folders[month])
    os.makedirs(dest, exist_ok=True)
    if not os.path.exists(os.path.join(dest, file)):
        shutil.move(os.path.join(old_path, file), os.path.join(dest, file))
        moved += 1
        print(f"{moved}/{len(files)} files moved.....{'%.2f'%(100*moved/len(files))}%")
    else:
        skipped += 1
   
print(f"\nFinished moving {moved} files!")
print(f"Skipped {skipped} duplicate files")