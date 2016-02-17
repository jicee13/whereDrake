import MySQLdb
import time
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


db = MySQLdb.connect(host=[server ip],    # your host, usually localhost
                     user=[username],         # your username
                     passwd=[passwd],  # your password
                     db=[database selected])
cur = db.cursor()



#send email here
#pull music videos from last 7 days from database
print cur.execute("SELECT Title, Link FROM musicVids WHERE (Timestamp <= %s AND Timestamp >= %s)", (int(time.time()),int(time.time()) - 604800))
db.commit()

#read in pre-written html files
f = open("html/firstHalf.html","r")
g = open("html/secondHalf.html","r")
htmlPage = f.read()

#format each title and link into table so when ser clikcs title, they're redirected to link
for row in cur :
   htmlPage+= '<tr><td><a href="' + row[1] + '">' + row[0].encode('utf-8') + '"</a></td></tr>'
htmlPage = htmlPage + g.read()

key = [api key]
sandbox = [mailgun sandbox key]
recipient = [recipient]

request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
request = requests.post(request_url, auth=('api', key), data={
    'from': [sender],
    'to': [reciever],
    'subject': [subject],
    'html': htmlPage
})

print 'Status: {0}'.format(request.status_code)
print 'Body:   {0}'.format(request.text)




db.close()
