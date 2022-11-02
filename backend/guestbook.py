#!/usr/bin/python3
'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''
import os 
import html #escape html code
import mysql.connector #connect to mysql database
import urllib.parse 
import cgi # recive inpouts from html form
import re #regular expressions
import datetime # get date of form submissions
from pytz import timezone # specify timezone
from dotenv import dotenv_values # hide sensitive data
# display html file
with open("/var/www/lophius.xyz/guestbook.html","r") as f1, open("/var/www/lophius.xyz/guestbook-message.html","r") as f2, open("/var/www/lophius.xyz/guestbook-message-attribute.html","r") as f3, open("/var/www/lophius.xyz/guestbook-message-attribute-link.html","r") as f4:
    websiteTemplate = f1.read()
    messageTemplate = f2.read()
    attributeTemplate = f3.read()
    attributeLinkTemplate = f4.read()

# remove trailing newline chars
websiteTemplate= websiteTemplate[:len(websiteTemplate)-1]
messageTemplate= messageTemplate[:len(messageTemplate)-1]
attributeTemplate = attributeTemplate[:len(attributeTemplate)-1]
attributeLinkTemplate= attributeLinkTemplate[:len(attributeLinkTemplate)-1]


form = cgi.FieldStorage()
dbLogin = dotenv_values()
db = mysql.connector.connect(
    host = dbLogin["GUESTBOOK_HOST"],
    user = dbLogin["GUESTBOOK_USER"],
    passwd = dbLogin["GUESTBOOK_PASSWD"],
    database = dbLogin["GUESTBOOK_DATABASE"]
)
mycursor = db.cursor()

if form.getvalue("message") and form.getvalue("name"):
    message = form.getvalue("message")
    name = form.getvalue("name")
    email = None
    showEmail = False
    website = None
    style = "message-style1"
    if form.getvalue("email"):
        email = form.getvalue("email")
    if form.getvalue("show-email"):
        if (form.getvalue("show-email")) == "on" and re.search("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", form.getvalue("email")):
            showEmail = True
    if form.getvalue("website") and re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", form.getvalue("website")):
        website = form.getvalue("website")
    if form.getvalue("message-style"):
        if form.getvalue("message-style") == "message-style2" or form.getvalue("message-style") == "message-style3":
            style = form.getvalue("message-style")
    mycursor.execute("select * from Messages where Message = %s and Name = %s", (message, name))
    mycursor.fetchall()
    if mycursor.rowcount == 0:
        date = datetime.datetime.now(timezone('GMT'))
        dateFormatted = str(date.year)+"-"+str(date.month)+"-"+str(date.day)+" "+str(date.hour)+":"+str(date.minute)+":"+str(date.second)
        mycursor.execute("insert into Messages(Name, Message, Email, ShowEmail, Website, Style, Date) values (%s, %s, %s, %s, %s, %s, %s)", (name, message, email, showEmail, website, style, date))
        db.commit();


num = mycursor.execute("select * from Messages")
websitesQuantity = 0

for i in mycursor:
    name = html.escape(i[0])
    message = html.escape(i[1])
    email = i[2]
    if email != None:
        email = html.escape(i[2])
    emailShow = i[3]
    website = i[4]
    if website != None:
        website = html.escape(i[4])
    style = html.escape(i[5])
    date = i[6].strftime("%-H:%M %-d %B %Y")

    messageNew = messageTemplate

    name = attributeTemplate.replace("<!--%ATTRIBUTE-->", name)
    date = attributeTemplate.replace("<!--%ATTRIBUTE-->", date)

    messageNew = messageNew.replace("<!--%STYLE-->", style)
    messageNew = messageNew.replace("<!--%NAME-->", name)
    messageNew = messageNew.replace("<!--%MESSAGE-->", message)
    messageNew = messageNew.replace("<!--%DATE-->", date)

    if (website != None):
        website = attributeLinkTemplate.replace("<!--%ATTRIBUTE_LINK-->", website)
        messageNew = messageNew.replace("<!--%WEBSITE-->", website)
        websitesQuantity = websitesQuantity + 1
     
    if (email != None and emailShow  == 1):
        email = attributeTemplate.replace("<!--%ATTRIBUTE-->", email)
        messageNew = messageNew.replace("<!--%EMAIL-->", email)
    
    websiteTemplate = websiteTemplate.replace("<!--%NEW_MESSAGE-->", messageNew)
    
websiteTemplate = websiteTemplate.replace("<!--%WEBSITESNO-->", str(websitesQuantity))

print("Content-type:text/html\r\n\r\n")
print(websiteTemplate)
