# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:28:27 2024

@author: kevinh
"""

def colour(text, rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    
    col = "\x1b[38;2;" + f"{r};{g};{b}m"
    reset = "\x1b[0m"
    
    return f"{col}{text}{reset}"