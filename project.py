#!/usr/bin/env python
# coding: utf-8

# 1.2 Ebay Amazon Gift Cards

# a) use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm".

# In[9]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import re 
import time


# In[118]:


url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&LH_Sold=1&rt=nc&_pgn=1"
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get(url, headers = headers).text
with open(f'amazon_gift_card_01.htm','w') as file:
    file.write(page)
file.close()


# b) take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

# In[123]:


url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&LH_Sold=1&rt=nc&_pgn="
for i in range(1,10):
    filename = 'amazon_gift_card_{:02d}.htm'.format(i+1)
    search_page = requests.get(f'{url}{i+1}', headers = headers).text
    with open(filename,'w') as file:
        file.write(search_page)
    file.close()
    time.sleep(10)


# c) write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object.

# In[265]:


for i in range(0,10):
    filename = 'amazon_gift_card_{:02d}.htm'.format(i+1)
    with open(filename,'r') as file:
        html = file.read()
        soup = BeautifulSoup(html,'html.parser')


# d) using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item.

# In[7]:


title = []
price =[]
freight = []
freight1 = ''
for i in range(0,10):
    filename = 'amazon_gift_card_{:02d}.htm'.format(i+1)
   
    with open(filename,'r') as file:
        html = file.read()
        soup = BeautifulSoup(html,'html.parser')
        
        titles = soup.find_all("div", class_='s-item__title')
        for a in titles:
            if a.text is None:
                title1 = 'None'
            else: 
                title1 = a.text
            title.append(title1.replace("New Listing",""))
        
        prices = soup.find_all("span", class_='s-item__price')
        for b in prices:
            if b.text is None:
                price1 = '0'
            else: 
                price1 = b.text
            price.append(price1)
        
        details = soup.find_all('div', class_='s-item__details')
        for item in details:
            freights = item.find_all("span", class_='s-item__shipping')
            
            for c in freights:
                if len(c) == 0:
                    freight1 = 'free shipping'
                else:
                    freight1 = c.text
            freight.append(freight1)

info = zip(title, price, freight)        
print(list(info))        


# e) using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value.

# In[51]:


#title_price = ""
list_title_price = []
for i in range(0,610):
    title_price = re.findall(r'\d+', title[i])
    if len(title_price) == 0:
        title_price = 0
    else:
        title_price = title_price[0]
    list_title_price.append(str(title_price))
    
string_price =', '.join(list_title_price)

list_title_int = []
list_a = re.findall(r'\d+', string_price)
for i in list_a:
    int_price = int(i)
    list_title_int.append(int_price)

#int_price = ""
list_price_int = []
for l in range(0,610):
    int_price = re.findall(r'\d+', price[l])
    if len(int_price) == 0:
        int_price = 0
    else:
        int_price= int_price[0]
    list_price_int.append(float(int_price))

#int_freight = ""
list_freight_int = []
for o in range(0,610):
    int_freight = re.findall(r'/d+', freight[0])
    if len(int_freight) == 0:
        int_freight = 0
    else: 
        int_freight = int_freight[0]
    list_freight_int.append(float(int_freight))
len(list_freight_int)

counter = 0
rank = []
for v in range(0,610):
    if list_title_int[v] < list_price_int[v]+ list_freight_int[v]:
        counter += 1
        rank.append(v)
rank1 = ' '.join(str(e) for e in rank)
print(f'number of over value sale:{counter}\n')
print(f'over priced gift card name:\n') 
for i in rank:
    print(title[i])


# f) What fraction of Amazon gift cards sells above face value? Why do you think this is the case?

# In[54]:


fraction = "{:.1%}".format(counter/610)
print(f'fraction:{fraction}')
print(f'The reason {fraction} of the gift card were sold above face vaule could be bought by negligence. Otherwise, there could be other benefits or motivations involved in the transcations, because in common sense, no one would purchase cash equivalent products for less than what one would spend.' )


# (2.2) fctables.com

# a) Following the steps we discussed in class and write code that automatically logs into the website fctables.com Links to an external site..

# In[55]:


from bs4 import BeautifulSoup
import requests
import time

URL = "https://www.fctables.com/user/login/"
session_requests = requests.session()
headers = {'User-Agent': 'Mozilla/5.0'}
res = session_requests.post(URL, 
                            data = {'login_action': '1',
                            'login_username': 'zlwan',
                            'login_password': '12345',
                            'user_remeber': '1',
                            'submit': '1'},
                            headers = headers,
                            timeout = 15)
print(f'Status Code:{res.status_code}')


# b) Verify that you have successfully logged in:  use the cookies you received during log in and write code to access https://www.fctables.com/tipster/my_bets/ Links to an external site..  Check whether the word “Wolfsburg” appears on the page.  Don’t look for your username to confirm that you are logged in (it won’t work) and use this page’s content instead.

# In[58]:


cookies = session_requests.cookies.get_dict()

page2 = session_requests.get(url='https://www.fctables.com/tipster/my_bets/', cookies=cookies)
        
doc2 = BeautifulSoup(page2.content, 'html.parser')
       

print(f'Page involve username: {bool(doc2.findAll(text = "zlwan"))}') # your username here
bet = doc2.findAll("a")
Wolfs = bet

def sanity_check(Wolfs):
    if 'Wolfsburg' in Wolfs:
        return True
    else:
        return False

maybe = sanity_check('Wolfsburg')
print(f'Page invlove bet on Wolfsburg: {maybe}')


# In[ ]:




