import requests
from bs4 import BeautifulSoup
from sys import exit, argv
from konlpy.tag import Hannanum #KoNLPy is a Python package for Korean natural language processing.
from support import lastpage_determiner, file_finder #what I wrote.
from googletrans import Translator #googletranslator module
import pandas
import time
import csv

#check if command line arguments are in proper form.
if not len(argv) == 2:
    print("Usage: bluehouse.py #int")
    exit(1)
    
#chekcing command line argument
try:
    num = int(argv[1])
except ValueError:
    print("Must provide integer")
    exit(4)
    
#checking the number
if num < 1:
    print("provide a integer bigger than 0")
    exit(5)

#getting/ saving latest page.
latest = open('latestpage.txt','r')
page0 = latest.read()
page0 = lastpage_determiner(page0) #from support.py
latest.close()
if page0 is not None: #to save the page accessible.
    with open('latestpage.txt','w') as number:
        number.write(page0)

#where the data of words going to be saved
data ={} 

# scraping data from html pages.
for i in range(num):
    page1 = str(int(page0)-i)
    #print(page1, end = '') #not needed
    page = 'https://www1.president.go.kr/articles/{}'.format(page1)
    #get the page.
    response = requests.get(page)
    #there may be cases the page is deleted. and 404.
    if response.status_code != 200:
        print('the page could not load = {}'.format(page))
        continue
    #response의 응답 객체가 나옴. 밑에 soup 가 html content를 parser로 파싱 설정! (response object, parsed with soup)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    textd = ''
    words = [] #class="text left cb text_wrap motion fadeIn visible"
    html = soup.find('div', {'class' :'text left cb text_wrap motion'}) # i am keep not getting the one I want.
    if html is None:
        print('it is not getting data')
        exit(3)
    #Only the Text
    textd = html.text
    
    han = Hannanum()
    words = han.nouns(textd)
    
    #make dictionary of how many times each word comes up.
    for w in words:
        if len(w) > 1: #if it is one word, deleted! not so important. #####******
            if w in data:
                data[w] += 1
            else:
                data[w] = 1
    #get date
    if i ==0:
        newestd = soup.find('span', {'class' :'ci cs_date motion'})
        newestd = newestd.text
    if i == (num -1):
        oldestd = soup.find('span', {'class' :'ci cs_date motion'})
        oldestd = oldestd.text
        
    
#this gives me a list ex.[('뉴딜', 7), ('대통령', 4), ('“한국판', 4)...]
top = [[k, v] for k,v in sorted(data.items(),  key=lambda kv: kv[1], reverse=True)]

#top 10 words
top10 = top[:10]

#google translate module used
    #10 KOREAN word list.

word10 = []
for i in range(10):
    word10.append(top10[i][0])

#this is the translator
translator= Translator()
#returns list object of translated
a = translator.translate(word10, dest='en')

#getting one by one.
i = 0
for translated in a:
    top10[i].append(translated.text)
    i += 1
#prints a data table.
df = pandas.DataFrame(data = top10, columns = ['Word', 'Number of Times', 'English Translation'])
print(df.to_string())

#csv file add
time = time.strftime('%Y%m%d', time.localtime(time.time())) 
filename1 = '{}.csv'.format(time)
if file_finder(time):
    with open(filename1, 'a+') as file:
        writer = csv. writer(file)
        writer.writerow(['Word', 'Number of Times', 'English Translation'])
        for stuff in top10:
            writer.writerow([stuff[0],stuff[1],stuff[2]])
        writer.writerow(['From {} to {}'.format(oldestd, newestd)])
else:
    with open(filename1, 'w') as file:
        writer = csv. writer(file)
        writer.writerow(['Word', 'Number of Times', 'English Translation'])
        for stuff in top10:
            writer.writerow([stuff[0],stuff[1],stuff[2]])
        writer.writerow(['From {} to {}'.format(oldestd, newestd)])
        
print('Pages From {} to {}'.format(oldestd, newestd))

if file_finder(time) and len(argv) == 2:
    print('Top 10 keywords saved into file: {}'.format(filename1))
else:
    print('Sorry, file not saved.')




