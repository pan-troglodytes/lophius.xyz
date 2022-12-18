#!/usr/bin/python3
'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''
import html #escape html code
import mysql.connector #connect to mysql database
import cgi # recieve inputs from html form
import datetime # get date of form submissions
import re #regular expressions
from pytz import timezone # specify timezone
from dotenv import dotenv_values # hide sensitive data
snowfallgardenSocialPath = "/var/www/lophius.xyz/snowfallgarden/social.html"
snowfallgardenSocialEntryPath = "/var/www/lophius.xyz/snowfallgarden/social-entry.html"
snowfallgardenSocialEntryWebsitePath = "/var/www/lophius.xyz/snowfallgarden/social-entry-website.html"
snowfallgardenSocialEntryForkofPath = "/var/www/lophius.xyz/snowfallgarden/social-entry-forkof.html"
snowfallgardenSocialEntryCommentPath = "/var/www/lophius.xyz/snowfallgarden/social-entry-comment.html"
with open(snowfallgardenSocialPath ,"r") as f1, open(snowfallgardenSocialEntryPath ,"r") as f2, open(snowfallgardenSocialEntryWebsitePath ,"r") as f3, open(snowfallgardenSocialEntryForkofPath ,"r") as f4, open(snowfallgardenSocialEntryCommentPath ,"r") as f5:
    websiteTemplate = f1.read()
    entryTemplate = f2.read()
    websiteAttrTemplate = f3.read()
    forkofTemplate = f4.read()
    commentTemplate = f5.read()

websiteTemplate= websiteTemplate[:len(websiteTemplate)-1]
entryTemplate= entryTemplate[:len(entryTemplate)-1]
websiteAttrTemplate= websiteAttrTemplate[:len(websiteAttrTemplate)-1]
forkofTemplate= forkofTemplate[:len(forkofTemplate)-1]
commentTemplate= commentTemplate[:len(commentTemplate)-1]

form = cgi.FieldStorage()
dbLogin = dotenv_values()
db = mysql.connector.connect(
    host = dbLogin["SNOWFALL_HOST"],
    user = dbLogin["SNOWFALL_USER"],
    passwd = dbLogin["SNOWFALL_PASSWD"],
    database = dbLogin["SNOWFALL_DATABASE"]
)
tableName = "Snowflakes";
mycursor = db.cursor()
mycursor.execute("select * from "+tableName+"")
for i in mycursor:
    snowflakeId = i[0]
    forkof = None
    if (i[1] != None):
        forkof=i[1]
    name = html.escape(i[2])
    comment = None
    if (i[3] != None):
        comment=html.escape(i[3])
    website = None
    if (i[4] != None):
        website=i[4]
    snowflake = str(i[5]).replace("b'","").replace("'","")
    date = i[6].strftime("%-H:%M %-d %B %Y")
    allowDemo = i[7]

    snowflakeSource = re.search('data:image\/png;base64,[a-zA-Z0-9\/\+]*=*',snowflake)

    newEntry = entryTemplate
    newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_ID-->",html.escape(snowflakeId))
    if forkof != None:
        newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_FORKOF-->",forkofTemplate.replace("<!--%ATTRIBUTE-->",html.escape(forkof)))
    newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_NAME-->",name)
    if website != None:
        newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_WEBSITE-->",websiteAttrTemplate.replace("<!--%ATTRIBUTE-->",html.escape(website)))
    newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_SNOWFLAKE-->",html.escape(snowflake))
    newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_IMAGESOURCE-->",html.escape(snowflakeSource[0]))
    if comment != None:
        newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_COMMENT-->", commentTemplate.replace("<!--%ATTRIBUTE-->",comment))
    if int(allowDemo) == 1 :
        newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_DEMO-->", html.escape(snowflakeId))
    else:
        newEntry = newEntry.replace("<!--%SNOWFALL_ENTRY_DEMO-->", "fail")



    websiteTemplate = websiteTemplate.replace("<!--%SNOWFALL_ENTRY-->",newEntry)



print("Content-type:text/html\r\n\r\n")
print(websiteTemplate);
