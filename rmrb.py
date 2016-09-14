import urllib
import re
import datetime
import json
import zlib
import smtplib
from email.mime.text import MIMEText



def send_mail(content):
    #me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = datetime.datetime.now().strftime('%Y-%m/%d')
    msg['From'] = 'rmrb321@sina.cn'
    msg['To'] = "rmrb321@yeah.net"
    try:
        server = smtplib.SMTP()
        server.connect('smtp.sina.cn')
        server.login('rmrb321@sina.cn','123rmrb')
        server.sendmail('rmrb321@sina.cn',"rmrb321@yeah.net",msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

def tmp():
    today = datetime.datetime.now().strftime('%Y-%m/%d')
    #today='2016-09/11'
    print today
    urlbase = r'http://paper.people.com.cn/rmrb/html/%s/'%(today)
    print urlbase
    banlist = re.compile('nbs.D110000renmrb_\d{2}.htm')
    #banlist = re.compile('nbs.D110000renmrb_01.htm')
    ban_url_set=set()

	html = urllib.urlopen(r'%snbs.D110000renmrb_01.htm'%(urlbase)).read()
	l = re.findall(banlist,html)
	#print html
	for ll in l:
		ban_url_set.add(ll)
		print ban_url_set

	article_list = re.compile(r'nw.D110000renmrb_\d{8}_\d{1,2}-\d{2}.htm')
	content_url_set = set()
	for ban_url in ban_url_set:
		ban_page = urllib.urlopen(urlbase+ban_url).read()
		l = re.findall(article_list,ban_page)
		for ll in l:
			content_url_set.add(ll)
		print content_url_set
		print len(content_url_set)


	content_list=[]


	for content_url in content_url_set:
		content_page = urllib.urlopen(urlbase+content_url).read()
		results = re.findall(re.compile(r'<title>(.*?)</title>.*?<!--enpcontent-->(.*?)<!--/enpcontent-->',re.M|re.S),content_page)
		if results:
			title=results[0][0]
			content=results[0][1]
			content_list.append(json.dumps({'title':title,'content':content,'date':content_url[17:23],'ban':content_url[-6:-4]}))


	body = "###".join(content_list)
	print len(body)
	send_mail(body)
	print 'sent mail'
