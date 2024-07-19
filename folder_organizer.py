# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 12:03:19 2024

@author: kevinh
"""

import os, shutil

nums = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def month_format(month_chars, leading_zero=True, num_first=True, month_only=False, num_only=False):
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
            formatted.append(f"{num} {month}")
        else:
            formatted.append(f"{month} {num}")

    return formatted

m4n2 = month_format(9, num_first=False)
n2m4 = month_format(9)
m3n2 = month_format(3, num_first=False)
n2m3 = month_format(3)
m4n1 = month_format(9, leading_zero=False, num_first=False)
n1m4 = month_format(9, leading_zero=False)
m3n1 = month_format(3, leading_zero=False, num_first=False)
n1m3 = month_format(3, leading_zero=False)
m4 = month_format(9, month_only=True)
m3 = month_format(3, month_only=True)
n2 = month_format(0, num_only=True)
n1 = month_format(0, leading_zero=False, num_only=True)

formats = [m4, m3, n2, n1, m4n2, n2m4, m3n2, n2m3, m4n1, n1m4, m3n1, n1m3]

print("\nWhat month format would you like to follow:")
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
    i2 = name.rfind("_")
    return name[8 : i1].upper(), int(name[i2 + 1 : i2 + 5]), int(name[i2 + 5 : i2 + 7])

old_path = input("Enter current directory path (click on path bar and copy): ")#"TBD" #POS directory
new_path = input("Enter desired directory path: ")
print("-----------------------------------------------------------------------------")
files = os.listdir(old_path)

moved = 0
skipped = 0
# todo: use word checker to decide which customer folder to put into
#       will ask if correct folder before moving ofc
for file in files:
    customer, year, month = get_info(file)
   
    os.makedirs(f"{new_path}/{year}/{month_folders[month]}", exist_ok=True)
    if not os.path.exists(f"{new_path}/{year}/{month_folders[month]}/{file}"):
        shutil.move(f"{old_path}/{file}", f"{new_path}/{year}/{month_folders[month]}/{file}")
        moved += 1
    else:
        skipped += 1
    # os.makedirs(f"{new_path}/{customer}/{year}/{month_folders[month]}", exist_ok=True)
    # shutil.move(f"{old_path}/{file}", f"{new_path}/{customer}/{year}/{month_folders[month]}")
   
print(f"\nFinished moving {moved} files!")
print(f"Skipped {skipped} duplicate files")