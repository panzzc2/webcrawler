'''
Created on Nov 2, 2014

@author: Phuah Chee Chong
'''

import datetime, os
from scripts.xmlHandler.xmlControl import *

def word_in (word, phrase):
    return word in phrase.split()

        
xmldocRequest = ET.parse("searchRange.xml")
rootRequest = xmldocRequest.getroot()

for s in rootRequest:
    
    keywordRoot = None
    source = s.get('source')
    iniStartY = s.get('startY')
    iniStartM = s.get('startM')
    iniStartD = s.get('startD')
    endY = s.get('endY')
    endM = s.get('endM')
    endD = s.get('endD')
    
    now = datetime.datetime.now()
        
    '''
    if no end date is specified, the current date will be used
    '''
    
    if endD == "":
        endD = now.day
        
    if endM == "":
        endM = now.month
    
    if endY == "":
        endY = now.year

    startDates = datetime.date(int(iniStartY), int(iniStartM), int(iniStartD))
    endDates = datetime.date(int(endY), int(endM), int(endD))
    day = datetime.timedelta(days=1)
    
    while (startDates <= endDates):
        
        strCurD = str(startDates.day)
        strCurD = strCurD.zfill(2) # Pads zero to the left
            
        strCurM = str(startDates.month)
        strCurM = strCurM.zfill(2)

        strCurY = str(startDates.year)
        
        currentQuery = strCurD + '-' + strCurM + '-' + strCurY
        
        dName = "../output/" + source + "/" + strCurY + "/" + strCurM
        fullDate = strCurD + strCurM  + strCurY
        
        xmldoc = openXMLFile(dName, fullDate)
        if (xmldoc != -1):
            root = xmldoc.getroot()
            for category in root.findall('category'):
                for article in category:
                    content = article.text
           
                    if(word_in ("jakarta", content.lower())):
                            
                        if(keywordRoot is None):
                            keywordRoot = ET.Element("selectedArticles", {"id":strCurD + strCurM  + strCurY, "source": source, "date=": strCurD + '-' + strCurM +'-' + strCurY})
                        
                        createArticleTag = ET.SubElement(keywordRoot, 'article', {'link': category.find("article").attrib['link'], 'title': category.find("article").attrib['title']})
                        createArticleTag.text = content
                        
                        tree = ET.ElementTree(keywordRoot)
                        tree.write(dName + "/" + fullDate +'Keywords.xml', xml_declaration=True, encoding='utf-8', method="xml")
                        print("Keyword FOUND!")
                        
                    else:
                        print("Keyword not found")
                    
        else:
            print(str(startDates) + " done!")
            startDates += day
            continue
            #print(xmldoc)
        print(str(startDates) + " done!")
        startDates += day
        

