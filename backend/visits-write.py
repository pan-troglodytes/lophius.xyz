#!/usr/bin/python3
'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''
import cgi # recive inpouts from html form
import mysql.connector #connect to mysql database
import datetime # get date of form submissions
from pytz import timezone # specify timezone
from dotenv import dotenv_values # hide sensitive data

form = cgi.FieldStorage()
dbLogin = dotenv_values()
db = mysql.connector.connect(
    host = dbLogin["VISITS_HOST"],
    user = dbLogin["VISITS_USER"],
    passwd = dbLogin["VISITS_PASSWD"],
    database = dbLogin["VISITS_DATABASE"]
)
mycursor = db.cursor()

print("Content-type:text/html\r\n\r\n")
# display html file
f = open("/var/www/lophius.xyz/index.html","r")
print(f.read())
if form.getvalue("enter"):
    date = datetime.datetime.now(timezone('GMT'))
    dateFormatted = str(date.year)+"-"+str(date.month)+"-"+str(date.day)+" "+str(date.hour)+":"+str(date.minute)+":"+str(date.second)
    mycursor.execute("insert into Visits(Visit) values (\""+str(dateFormatted)+"\")")
    db.commit();
    print('<meta http-equiv="refresh" content="0; url = https://lophius.xyz/solar-system.html">')
