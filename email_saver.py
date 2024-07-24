# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 16:26:41 2024

@author: kevinh
"""

import win32com.client as w32
import os

def get_folder(path, parent):
    if len(path) == 1:
        return parent.Folders[path[0]]
    
    else:
        return get_folder(path[1:], parent.Folders[path[0]])

outlook = w32.Dispatch("Outlook.Application").GetNamespace("MAPI")
recip = outlook.CreateRecipient(input("Enter shared email address: "))
recip.Resolve()

if recip.Resolved:
    print("**ATTENTION: THIS PROGRAM DOES NOT SAVE FORWARDED MESSAGES**")
    print("------------------------------------------------------------\n")
    save_location = input("Please enter the full path to the desired save folder below:\n> ")#.replace("\\", "/")##"/Users/yinj/OneDrive - Corporativo Bimbo, S.A. de C. V/Desktop/pos_temp"
    
    inbox = outlook.GetSharedDefaultFolder(recip, 6)
    bigdaddy = inbox.Parent
    sources = []
    src = " "
    f = 1
    
    print("\nPlease enter the paths to the desired source folders\n(e.g. //A/B/C/D where D is the desired source folder's name and //A/B/C is its location in properties)")
    print("------------------------------------------------------------------------------------------------------")
    while src != "":
        src = input(f"Enter source folder #{f} or press ENTER if done:\n> ")
        sources.append(src)
        f += 1
    sources.pop(-1)
    summary = [0, 0, 0, 0]
    for s in sources:
        len1 = len(os.listdir(save_location))
        source = get_folder(s.split(os.sep)[3:], bigdaddy)
        messages = source.Items
        total = len(messages)
        
        saved = 0
        fwd = 0
        skipped = []
        dupes = []
        for m in messages:
            if m.Subject[-4:] == ".ext":
                skipped.append(m.Subject)
            elif "right subject" in m.Subject and m.SenderName.upper() == "real sender":
                if os.path.exists(os.path.join(save_location, f"{m.Subject}.msg")):
                    dupes.append(m.Subject)
                else:
                    m.SaveAs(os.path.join(save_location, f"{m.Subject}.msg"), 3)
                    saved += 1
                    print(f"{saved}/{total} messages saved.....{'%.2f'%(100*saved/total)}%")
            elif m.SenderName != "fake sender":
                skipped.append(m.Subject)
            else:
                fwd += 1
        
        len2 = len(os.listdir(save_location))
        
        summary[0] += (len2 - len1)
        summary[1] += fwd
        summary[2] += len(dupes)
        summary[3] += len(skipped)
        print(f"Finished saving {len2 - len1} messages!\n")
        print(f"Filtered out {fwd} forwarded messages\n")
        print(f"Filtered out {len(dupes)} duplicate messages:")
        for i in range(len(dupes)):
            print(f" {i+1}. {dupes[i]}")
        print("")
        print(f"Skipped {len(skipped)} messages:")
        for i in range(len(skipped)):
            print(f" {i+1}. {skipped[i]}")
        print("")
            
    print("Summary:")
    print(f"Successfully saved {summary[0]} messages")
    print(f"Filtered out {summary[1]} forwarded messages")
    print(f"Filtered out {summary[2]} duplicate messages")
    print(f"Skipped {summary[3]} messages")
    
    freqs = {"C3":131, "C#3":139, "D3":147, "D#3":156, "E3":165, "F3":175, "F#3":185, "G3":196, "G#3":208, "A3":220, "A#3":233, "B3":247, 
             "C4":262, "C#4":277, "D4":294, "D#4":311, "E4":330, "F4":349, "F#4":370, "G4":392, "G#4":415, "A4":440, "A#4":466, "B4":494, 
             "C5":523, "C#5":554, "D5":587, "D#5":622, "E5":659, "F5":698, "F#5":740, "G5":784, "G#5":831, "A5":880, "A#5":932, "B5":988, }
  
    song = ["C4", "D4", "C4", "A3", "A3", "A3", "G3", "A3", "A#3", "A3"]
    for note in song:
        winsound.Beep(freqs[note], 500)
        
else:
    print("Recipient could not be resolved")