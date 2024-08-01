# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:49:21 2024

@author: kevinh
"""

def get_range(selection):
    selected = []
    done = {}
    selection = selection.replace(" ", "").split(",")
    for i in range(len(selection)):
        selection[i] = selection[i].split("-")
        try:
            int(selection[i][0])
            int(selection[i][-1])
        except ValueError:
            print("Invalid range! Try again")
            return
        else:
            if int(selection[i][0]) > int(selection[i][-1]):
                print("Invalid range! Try again")
                return
            else:
                for val in range(int(selection[i][0]), int(selection[i][-1]) + 1):
                    if val not in done:
                        selected.append(val)
                        done[val] = 1
                       
    return selected