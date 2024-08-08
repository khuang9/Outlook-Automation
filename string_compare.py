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

def strip_punc(s):
    punctuation = ["-", "_", ".", ","]
   
    for p in punctuation:
        s = s.replace(p, "")
   
    return s

def strip_num(s):
    for n in range(48, 58):
        s = s.replace(chr(n), "")
   
    return s

def process_words(orig, compare, strip_puncs, strip_nums):
    removed = 0
    orig = strip_dupes(strip_spaces(orig))
    compare = strip_dupes(strip_spaces(compare))
   
    if strip_puncs:
        orig = strip_punc(orig)
        compare = strip_punc(compare)
       
    if strip_nums:
        orig = strip_num(orig)
        compare = strip_num(compare)
   
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
           
    if min_len == 0:
        return 0
    else:
        return matches/min_len
   
def match_degree(orig, compare, strip_puncs=False, strip_nums=False):
    if orig != compare:
        penalty = -0.01
    else:
        penalty = 0
       
    orig, compare, removed = process_words(orig, compare, strip_puncs, strip_nums)
    sim = similarity(orig, compare)
    rem = 1 - removed/(removed + len(compare))
   
    return (sim + rem)/2 + penalty