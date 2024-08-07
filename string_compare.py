# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:29:05 2024

@author: kevinh
"""

def strip_dupes(s):
    i = 0
   
    while i in range(len(s) - 1):
        if s[i] == s[i+1]:
            s = s[:i] + s[i+1:]
        else:
            i += 1
           
    return s


def strip_spaces(s):
    return s.replace(" ", "")


def process_words(orig, compare):
    removed = 0
    orig = strip_dupes(strip_spaces(orig))
    compare = strip_dupes(strip_spaces(compare))
   
    # might remove from longer one instead of compare (maybe)
    i = 0
    while i in range(len(compare) - 1):
        if compare[i] not in orig:
            compare = compare[:i] + compare[i+1:]
            removed += 1
        else:
            i += 1
           
    return orig, compare, removed


def similarity(orig, compare):
    matches = 0
   
    min_len = min(len(orig), len(compare))
    for i in range(min_len):
        if orig[i] == compare[i]:
            matches += 1
   
    return matches/min_len
   
def match_degree(orig, compare):
    if orig != compare:
        penalty = -0.01
    else:
        penalty = 0
       
    orig, compare, removed = process_words(orig, compare)
    sim = similarity(orig, compare)
    rem = 1 - removed/(removed + len(compare))
   
    return (sim + rem)/2 + penalty
  
