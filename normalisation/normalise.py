'''
Created on Sep 30, 2014

@author: Phuah Chee Chong

This file normalises the articles by calling perl scripts

1. Remove unwanted characters and combine all days of month into text file
2. Expand abbrevations
'''
import subprocess, xml.etree.ElementTree as ET

def normalise(yr, mn, source):
#     sources = []
#     
#     xmldocRequest = ET.parse(input)
#     rootRequest = xmldocRequest.getroot()
#     
#     for s in rootRequest:
#         sources.append(s.get('source'))
# 
#     for source in sources:
#     
    for mn in range(int(mn), int(mn)+1):
        print("1. Cleaning Unwanted Characters...")
        pipe = subprocess.call(["perl", "normalisation/1_cleanUnwantedChars.pl", str(str(yr)), str(mn).zfill(2), str(source)])
        
        print("2. Expanding Abbreviations...")
        pipe = subprocess.call(["perl", "normalisation/2_expand_abb.pl", str(yr), str(mn).zfill(2), str(source)])
        
        print("3. Splitting Sentences...")
        pipe = subprocess.call(["perl", "normalisation/3_split_snt.pl", str(yr), str(mn).zfill(2), str(source)])
        
        print("4. Removing Punctuations...")
        pipe = subprocess.call(["perl", "normalisation/4_remove_pnc.pl", str(yr), str(mn).zfill(2), str(source)])
        
        print("5. Appending <s></s> tags...") 
        pipe = subprocess.call(["perl", "normalisation/5_append_sos.pl", str(yr), str(mn).zfill(2), str(source)])