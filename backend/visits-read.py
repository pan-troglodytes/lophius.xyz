#!/usr/bin/python3
'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''
import cgi # recive inpouts from html form
import mysql.connector #connect to mysql database
from dotenv import dotenv_values # hide sensitive data

# display html file
f = open("/var/www/lophius.xyz/solar-system.html","r")
website = f.read()

form = cgi.FieldStorage()
dbLogin = dotenv_values()
db = mysql.connector.connect(
    host = dbLogin["VISITS_HOST"],
    user = dbLogin["VISITS_USER"],
    passwd = dbLogin["VISITS_PASSWD"],
    database = dbLogin["VISITS_DATABASE"]
)
mycursor = db.cursor()
mycursor.execute("select * from Visits")
mycursor.fetchall()
visitors = mycursor.rowcount
visitorMessage = ", visitor " + str(visitors)
print("Content-type:text/html\r\n\r\n")
print(website.replace("<!--%VISITORNO-->", visitorMessage)) 
