'''
Created on Oct 1, 2014

@author: Phuah Chee Chong
'''

import re

def convertUTF8(textToConvert):
    
        f = open('cleaning/utf8-encoding.txt')
        charEncodingPairs = f.readlines()
        f.close()
        
        for charEncodingPair in charEncodingPairs:
            if not charEncodingPair.startswith("#"):
                charEncodingList = charEncodingPair.split("/")
                utf8Char = charEncodingList[0]
                utf8Encoding = charEncodingList[1]
                
                convertedText = re.sub(utf8Encoding, utf8Char, textToConvert)
            
        return convertedText
    
    
def convertMonthToEnglish(textToConvert):

    f = open('cleaning/months.txt')
    monthsList = f.readlines()
    f.close()
    
    for monthPair in monthsList:
        if not monthPair.startswith("#"):
            monthPairSplit = monthPair.split("/")
            monthInMalay = monthPairSplit[0].rstrip()
            monthInEnglish = monthPairSplit[1].rstrip()
            
            textToConvert = re.sub(monthInMalay, monthInEnglish, textToConvert)
        
    return textToConvert