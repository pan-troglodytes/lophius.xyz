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

import struct # image things
import imghdr
import base64
def get_image_size(fname):
    with open(fname,'rb')as fhandle:
        head=fhandle.read(24)
        if len(head)!=24:
            return
        if imghdr.what(fname)=='png':
            check=struct.unpack('>i',head[4:8])[0]
            if check!=0x0d0a1a0a:
                return
            width,height=struct.unpack('>ii',head[16:24])
        elif imghdr.what(fname)=='gif':
            width,height=struct.unpack('<HH',head[6:10])
        elif imghdr.what(fname)=='jpeg':
            try:
                fhandle.seek(0)#Read0xffnext
                size=2
                ftype=0
                while not 0xc0<=ftype<=0xcf:
                    fhandle.seek(size,1)
                    byte=fhandle.read(1)
                    while ord(byte)==0xff:
                        byte=fhandle.read(1)
                    ftype=ord(byte)
                    size=struct.unpack('>H',fhandle.read(2))[0]-2
                #WeareataSOFnblock
                fhandle.seek(1,1)#Skip`precision'byte.
                height,width=struct.unpack('>HH',fhandle.read(4))
            except Exception:#IGNORE:W0703
                return
        else:
            return
    return width,height
print("<h1>it works!</h1>")
snowfallgardenPainterPath = "/var/www/lophius.xyz/snowfallgarden/paint.html"
with open(snowfallgardenPainterPath ,"r") as f1:
    websiteTemplate = f1.read()
websiteTemplate= websiteTemplate[:len(websiteTemplate)-1]
error = False
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
maxX = 65
maxY = 65
if form.getvalue("name") and form.getvalue("snowflake") and form.getvalue("id"):
    name = form.getvalue("name")
    snowflake = form.getvalue("snowflake")
    snowflakeId = form.getvalue("id")
    forkof = form.getvalue("forkof")
    #websiteTemplate = websiteTemplate.replace("<!--%TEST1-->", "<p>"+html.escape(name)+"</p>")
    #websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>"+html.escape(snowflake)+"</p>")
    website = None
    comment = form.getvalue("comment")
    if comment != None and len(comment) > 255:
        #websiteTemplate = websiteTemplate.replace("<!--%ERROR_NAME-->", formError.replace("<!--%ERROR-->","invalid name. your name cant be greater than 255 characters"))
        error = True
        websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>error, comment</p>")
    if len(form.getvalue("name")) > 255:
        #websiteTemplate = websiteTemplate.replace("<!--%ERROR_NAME-->", formError.replace("<!--%ERROR-->","invalid name. your name cant be greater than 255 characters"))
        error = True
        websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>error, name</p>")


    image64 = re.search('data:image\/png;base64,[a-zA-Z0-9\/\+]*=*',snowflake)
    if image64:
        
        
        f = open("/tmp/sf"+snowflakeId+".png", "wb")
        f.write(base64.b64decode(image64[0][22:]))
        f.close()
        dimensions = get_image_size("/tmp/sf"+snowflakeId+".png")
        if dimensions[0] > maxX or dimensions[1] > maxY:
            error = True
            websiteTemplate = websiteTemplate.replace("<!--%TEST2-->", "<p>too big</p>")

    else:
        websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>err</p>")
        error = True



    if re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))", snowflake.replace("https://snowfallgarden.lophius.xyz","")):
        websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>oof</p>")
        error = True


    blacklist = ["<script>", "<meta>","onafterprint", "onbeforeprint", "onbeforeunload", "onerror", "onhashchange", "onload", "onmessage", "onoffline", "ononline", "onpagehide", "onpageshow", "onpopstate", "onresize", "onstorage", "onunload", "onblur", "onchange", "oncontextmenu", "onfocus", "oninput", "oninvalid", "onreset", "onsearch", "onselect", "onsubmit", "onkeydown", "onkeypress", "onkeyup", "onclick", "ondblclick", "onmousedown", "onmousemove", "onmouseout", "onmouseover", "onmouseup", "onmousewheel", "onwheel", "ondrag", "ondragend", "ondragenter", "ondragleave", "ondragover", "ondragstart", "ondrop", "onscroll", "oncopy", "oncut", "onpaste", "onabort", "oncanplay", "oncanplaythrough", "oncuechange", "ondurationchange", "onemptied", "onnects)", "onended", "onerror", "onloadeddata", "onloadedmetadata", "onloadstart", "onpause", "onplay", "onplaying", "onprogress", "onratechange", "onseeked", "onseeking", "onstalled", "onsuspend", "ontimeupdate", "onvolumechange", "onwaiting", "ontoggle"]

    for i in blacklist:
        if re.search(re.escape(i), snowflake):
            websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>error, blacklist</p>")
            error = True

    if form.getvalue("website"):
        if re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", form.getvalue("website")):
            website = form.getvalue("website")
        else:
            #websiteTemplate = websiteTemplate.replace("<!--%ERROR_WEBSITE-->", formError.replace("<!--%ERROR-->","invalid website"))
            error = True
            websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>error, website</p>")

    mycursor.execute("select * from "+tableName+" where Name = %s and Snowflake = %s and Id = %s", (name, snowflake, snowflakeId))
    mycursor.fetchall()
    if mycursor.rowcount > 0:
        #websiteTemplate = websiteTemplate.replace("<!--%ERROR_DUPLICATE-->", formError.replace("<!--%ERROR-->","error! a guestbook entry of the exact same name and message already excists, a user cannot send duplicate messages"))
        error = True
        websiteTemplate = websiteTemplate.replace("<!--%TEST2-->","<p>error, rowcount</p>")

    if not error:
        date = datetime.datetime.now(timezone('GMT'))
        dateFormatted = str(date.year)+"-"+str(date.month)+"-"+str(date.day)+" "+str(date.hour)+":"+str(date.minute)+":"+str(date.second)
        mycursor.execute("insert into "+tableName+"(Id, Forkof, Name, Comment, Website, Snowflake, Date, AllowDemo) values (%s, %s, %s, %s, %s, %s, %s, %s)", (snowflakeId, forkof, name, comment, website, snowflake, date, 1))
        db.commit()
        websiteTemplate = websiteTemplate.replace("<!--%REDIRECT-->",'<meta http-equiv="refresh" content="0; url = https://snowfallgarden.lophius.xyz/social.html">')
print("Content-type:text/html\r\n\r\n")
print(websiteTemplate);

