#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib
import MySQLdb
import time

#import Twilio rest API client for use
from twilio.rest import TwilioRestClient
# put your own credentials here
ACCOUNT_SID = "[your id]"
AUTH_TOKEN = "[your token]"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

r = urllib.urlopen('http://www.hypetrak.com').read()
soup = BeautifulSoup(r,"html.parser")
articles = soup.find_all("div", class_ = "article")
details = soup.find_all("p", class_ = "entry-category")
detailTitles = soup.find_all("h2", class_ = "entry-title")

db = MySQLdb.connect(host="[server ip]",    # your host, usually localhost
                     user="[server username]",         # your username
                     passwd="[server password]",  # your password
                     db="[database name]")
cur = db.cursor()

#parallel arrays to store links and titles
links = []
titles = []
vidLinks = []
vidTitles = []

#populate normal articles and links
counter = 0
for element in articles:
    links.append(articles[counter].a["href"])
    titles.append(articles[counter].a["title"].encode('utf-8'))
    counter+=1

 #replace with whatever rappers you want to search for
keyword = 'Drake'
keyword2 = 'Kanye West'
keyword3 = 'Logic'
keyword4 = 'Earl Sweatshirt'
keyword5 = 'B.O.B'
foundStuff = False

counter = 0
for element in titles:
    if keyword in titles[counter] or keyword2 in titles[counter] or keyword3 in titles[counter] or keyword4 in titles[counter] or keyword5 in titles[counter]:
        foundStuff = True
        newURL = urllib.urlopen(links[counter]).read()
        currentSoup = BeautifulSoup(newURL,"html.parser")
        mainInfo = currentSoup.find("div", class_ = "entry-content")
        mainInfoContent = mainInfo.find('p').getText()
        #print ':::Title::: ', titles[counter], '::: '
        try:
            cur.execute("INSERT INTO relevantArticles (Timestamp, Title, Link) VALUES (%s, %s, %s)", (int(time.time()), titles[counter], links[counter]))
            db.commit()
            client.messages.create(
            	to="2149387008",
            	from_="4693400427",
            	body="New Article! " + titles[counter]
            )
            client.messages.create(
            	to="2149387008",
            	from_="4693400427",
            	body=links[counter]
            )
            print 'Successfully Added:', titles[counter], links[counter]
        except MySQLdb.Error, e:
            pass
            print 'Did NOT Add:', titles[counter], links[counter]

    else:
        pass
    counter+=1

if foundStuff == False:
    pass

#populate music vid details
counter = 0
for element in details:
    if (details[counter].find('a').getText().encode('utf-8') == 'Music Videos'):
        vidLinks.append(detailTitles[counter].a["href"])
        vidTitles.append(detailTitles[counter].find('a').getText().encode('utf-8'))
    counter+=1

#insert music video info into database for weekly email retrieval and for permanent keeping
counter = 0
for element in vidLinks:
    try:
        cur.execute("INSERT INTO musicVids (Timestamp, Title, Link) VALUES (%s, %s, %s)", (int(time.time()), vidTitles[counter], vidLinks[counter]))
        db.commit()
    except MySQLdb.Error, e:
        pass
    counter +=1

db.close()
