'''
Created on 29 Oct 2014

@author: Rakhi
'''
import urllib3, lxml.html, re, requests, xmlrpc, urllib.parse as urlparse, time

def produceAddressURL(currentQuery):
    '''
        input (str="name dd-mm-yyyy-dd-mm-yyyy numberOfPage Key")
        output (list=list of article URL)
        
        at first generates the url for the searche engine using typical patterns
        then realizes a query on Liberation.fr and return the output html5 page to a list
        finally parses the html page to extract links to liberation articles
        
    '''

    date      = currentQuery.split('-') # date
    pageExists = 1
    page = 0
    
    allReturnedURL = list()

    while pageExists != 0:
        try : 
            #urllib2.urlopen(url).getcode() != 200:
            http = urllib3.PoolManager()
    
            #f = http.request('GET', url)
            f = http.urlopen('GET', 'http://www.thesundaily.my/archive/'+date[2]+ date[1]+'?page='+str(page))
            data = f.data
            f.close()
        
            doc = lxml.html.document_fromstring(data)
    
            if doc.xpath('//div[@id="content"]//h2[@class="node-title"]//a'):
                
                print(currentQuery + " Collecting links for page " + str(page+1))
            #////section[@class="timeline"]/div[@class="day"]/ul/li/*/h2/a/@href          
                    #______ url des articles retournés par la requête ________#
                    
                        # collecting url on first page
                for returnedUrl in doc.xpath('//div[@id="content"]//h2[@class="node-title"]//a') :
                    #if not re.match('^http' , returnedUrl ):
                    
                    # return the search page in the form of [url, title, category, published date]
                    url = 'http://www.thesundaily.my' + str(returnedUrl.attrib.get('href'))
                    if "&sec=" not in url:
                        category = urlparse.urlparse(url).path
                        category = category.split('/', 3)
                        category = [category[2]]
                    else:
                        category = urlparse.parse_qs(url)['sec']
                    allReturnedURL.append([url, str(returnedUrl.text_content()), category[0].replace('_', ' '), str(date[0]) + str(date[1]) + str(date[2]) ] )
                    
                page += 1
                        
                    
                        
            else:
                pageExists = 0
                        
                        
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
            text = doc.xpath('//div[@id="content"]//div[@class="content"]//p')
            articleAuthorList = doc.xpath('//div[@class="submitted"]//div[@class="article-byline"]')
            articleDateList = doc.xpath('//div[@class="submitted"][1]')
            
            combinedSentences = ""
                
            for author in articleAuthorList:
                author = author.text_content()
                
            for articleDate in articleDateList:
                try:
                    articleDate = articleDate.text_content().strip()
                    articleDate = time.strptime(articleDate, "Posted on %d %B %Y - %I:%M%p")
                    
                except:
                    
                    articleDate = ""
            
                        
            for i in text:
                combinedSentences = combinedSentences + " " + i.text_content() + "<*p>"
            

            allContentInfo.append([combinedSentences, author, articleDate, articleKeywords])
            
            return allContentInfo
        
    except requests.exceptions.Timeout:
        #~ if verbose :
        print ('probleme de timeout')
        return 'error_server_timeout'
        
    
    

