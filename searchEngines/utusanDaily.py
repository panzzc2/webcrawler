'''
Created on Sep 17, 2014

@author: Phuah Chee Chong
'''
# -*- coding: utf-8 -*-
#import urllib2, html5lib
import urllib3, lxml.html, re, requests, xmlrpc, urllib.parse as urlparse, time, sys
from cleaning.cleanText import convertMonthToEnglish

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
  
    urlList.append('http://www.utusan.com.my/special/arkib')



    # ___ pour le test ___ #
    #~ urlList = ['http://www.liberation.fr/recherche/?q=sarkozy&period=custom&period_start_day=1&period_start_month=4&period_start_year=2012&period_end_day=2&period_end_month=4&period_end_year=2012&editorial_source=&paper_channel=&sort=-publication_date_time&page=1', 'http://www.liberation.fr/recherche/?q=sarkozy&period=custom&period_start_day=1&period_start_month=4&period_start_year=2012&period_end_day=2&period_end_month=4&period_end_year=2012&editorial_source=&paper_channel=&sort=-publication_date_time&page=2']



    allReturnedURL = list()
    allCatUrl = list()
    catCount = 0
    
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
            for returnedUrl in doc.xpath('//div[@class="menu menuTop menuTwo"]//ul//a') :
                #if not re.match('^http' , returnedUrl ):
                
                # return the search page in the form of [url, title, category, published date]
                url = 'http://www.utusan.com.my' + str(returnedUrl.attrib.get('href'))

                allCatUrl.append(url)
           
            print("Found %d categories" % len(allCatUrl))     
            
            for catURL in allCatUrl:
                
                articleCount = 0
                category = catURL.split('/', 4)
                if category[4] == "terkini" or category[3] == "video":
                    continue
                
                try : 
                    #urllib2.urlopen(url).getcode() != 200:
                    http = urllib3.PoolManager()
        
                    #f = http.request('GET', url)
                    f = http.urlopen('GET', catURL)
                    data = f.data
                    f.close()
                
                    doc = lxml.html.document_fromstring(data)
                    
                except urllib3.exceptions.HTTPError:
                    #~ print('error ' +  str(e.code))
                    break                          
                
                for returnedArticleUrl in doc.xpath('//div[@class="element teaser"]//h2//a') :
                    
                    url = 'http://www.utusan.com.my' + str(returnedArticleUrl.attrib.get('href')) # Getting attribute value

                    allReturnedURL.append([url, str(returnedArticleUrl.text_content()), category[4].replace('_', ' '), str(date[0]) + str(date[1]) + str(date[2]) ] )
                    
                    articleCount += 1
                    
                catCount += 1
                
                #if len(allReturnedURL) == 100:
                #    break
                
                print("%d Articles for category %d. %s" % (articleCount, catCount, category[4]))
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
    allContentInfo = list()
    # In case these are not found, provide empty string
    author = ""
    articleDate = ""
    articleKeywords = ""
    combinedSentences = ""
    # we need to check if article has already been crawled.
    try :
            http = urllib3.PoolManager()

            #f = http.request('GET', url)
            f = http.urlopen('GET', url)
            data = f.data
            f.close()
        
            doc = lxml.html.document_fromstring(data) # Removes all html tags
            text = doc.xpath('//div[@class="element article"]//div[@class="articleBody"]//p[@style="BD Bodytext" or @style="BD Body Text" or @style="BD Text"]')
            articleKeywordsList = doc.xpath('//meta[@name="keywords"]')
            articleAuthorList = doc.xpath('//div[@class="element article"]//div[@class="dateLine"]//span[@class="author"]')
            articleDateList = doc.xpath('//div[@class="element article"]//div[@class="dateLine"]//span[@class="date"]')
            
            for articleKeywords in articleKeywordsList:
                articleKeywords = articleKeywords.attrib.get('content')
            
            for author in articleAuthorList:
                author = author.text_content().replace("Daripada ", "")
            
            for articleDate in articleDateList:
                try:
                    articleDate = convertMonthToEnglish(articleDate.text_content())
                    articleDate = time.strptime(articleDate, "%d %B %Y %I:%M %p")
                    
                except:
                    
                    articleDate = ""      
            
            for i in text:
                if re.search("<!--", i.text_content()):
                    continue;
            
                combinedSentences = combinedSentences + " " + i.text_content() + "<*p>"
            
            allContentInfo.append([combinedSentences, author, articleDate, articleKeywords])
            
            return allContentInfo
        
    except requests.exceptions.Timeout:
        #~ if verbose :
        print ('probleme de timeout')
        return 'error_server_timeout'
        
    
    

