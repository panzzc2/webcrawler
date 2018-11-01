'''
Created on Sep 17, 2014

@author: Phuah Chee Chong
'''
# -*- coding: utf-8 -*-
#import urllib2, html5lib
import urllib3, lxml.html, re, requests, xmlrpc, urllib.parse as urlparse
from _ast import Str

###_________________________________________________________________________________####

def produceAddressURL(currentQuery):
    '''
        input (str="name dd-mm-yyyy-dd-mm-yyyy numberOfPage Key")
        output (list=list of article URL)
        
        at first generates the url for the searche engine using typical patterns
        then realizes a query on Liberation.fr and return the output html5 page to a list
        finally parses the html page to extract links to liberation articles
        
    '''

#     item = currentQuery.rstrip().split(' ')
#     name      = item[0] # pattern
    date      = currentQuery.split('-') # date
#     nbP       = int(item[2]) # nb of pages
#     speakerID = item[3] # keyName
    
#     if len(date) != 6:
#         print ('check date ' + date + '\n')
#         exit();
    
    urlList = list()
    
    # http://ww1.utusan.com.my/utusan/search.asp?paper=um&dd=02&mm=11&yy=1998&query=Search&stype=dt
  
    urlList.append('http://ww1.utusan.com.my/utusan/search.asp?paper=um&dd=' + date[0] + '&mm=' + date[1] + '&yy=' + date[2] + '&query=Search&stype=dt')



    # ___ pour le test ___ #
    #~ urlList = ['http://www.liberation.fr/recherche/?q=sarkozy&period=custom&period_start_day=1&period_start_month=4&period_start_year=2012&period_end_day=2&period_end_month=4&period_end_year=2012&editorial_source=&paper_channel=&sort=-publication_date_time&page=1', 'http://www.liberation.fr/recherche/?q=sarkozy&period=custom&period_start_day=1&period_start_month=4&period_start_year=2012&period_end_day=2&period_end_month=4&period_end_year=2012&editorial_source=&paper_channel=&sort=-publication_date_time&page=2']



    allReturnedURL = list()
    
    for url in urlList :
        # ce sont les urlQuery soumises au moteur de recherche
                
        try : 
            #urllib2.urlopen(url).getcode() != 200:
            http = urllib3.PoolManager()

            #f = http.request('GET', url)
            f = http.urlopen('GET', url)
            data = f.data
            f.close()
        
            doc = lxml.html.document_fromstring(data)
            #text2 = doc.xpath('//div[@id="body-content"]/div[@class="wrapper line"]/div[@class="grid-2-1 main-content line"]/div[@class="mod"]/section[@class="timeline"]/div[@class="day"]/ul/li/*/h2/a/@href')
           
            #______ url des articles retournés par la requête ________#
            for returnedUrl in doc.xpath('//div[@class="search"]//ul//a') :
                #if not re.match('^http' , returnedUrl ):
                
                # return the search page in the form of [url, title, category, published date]
                url = 'http://ww1.utusan.com.my' + str(returnedUrl.attrib.get('href'))
                if "&sec=" not in url:
                    category = urlparse.urlparse(url).path
                    category = category.split('/', 3)
                    category = [category[2]]
                else:
                    category = urlparse.parse_qs(url)['sec']
                allReturnedURL.append([url, str(returnedUrl.text_content()), category[0].replace('_', ' '), str(date[0]) + str(date[1]) + str(date[2]) ] )
                    
                    
        except urllib3.exceptions.HTTPError:
            #~ print('error ' +  str(e.code))
            break
    
    #~ if args.verbose:
    #~ print len(allReturnedURL)
    
    
    
    #~ exit()
    # if verbose 2
    #~ for i in allReturnedURL :
        #~ print i
        
    #~ return (allReturnedURL    , urlList[0])
    return allReturnedURL
        
        
###______________________________________________________________________________####

def cleanResultFile(url):
    ''' input : str(one url)
    output : str (utf8 text of the article) 
    '''
    # we need to check if article has already been crawled.
    try :
            http = urllib3.PoolManager()

            #f = http.request('GET', url)
            f = http.urlopen('GET', url)
            data = f.data
            f.close()
        
            doc = lxml.html.document_fromstring(data) # Removes all html tags
            text = doc.xpath('//div[@class="fullstory"]//p')
            
            combinedSentences = ""
            
            for i in text:
                if re.search("<!--", i.text_content()):
                    continue;
            
                combinedSentences = combinedSentences + " " + i.text_content()
            
            return combinedSentences
        
    except requests.exceptions.Timeout:
        #~ if verbose :
        print ('probleme de timeout')
        return 'error_server_timeout'
        
    
    

