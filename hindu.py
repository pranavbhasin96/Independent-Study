import bs4 as bs
import urllib2
import time
import re

base_add = "http://www.thehindu.com/archive/web/2017/"
month = ["01","02","03"]
marchday = []
janday = []
febday = []
before = {}
after = {}
beforeCount = 175
afterCount = 105
for i in xrange(1,25):
	marchday.append(str(i))
for i in xrange(1,29):
	febday.append(str(i))
for i in xrange(20,32):
	janday.append(str(i))
for i in month:
	lol=None
	if i=="01":
		lol = janday
	elif i=="02":
		lol=febday
	else:
		lol=marchday
	for j in lol:
		add = base_add + i + "/" + j + "/"
		print "address: ", add
		response  = urllib2.urlopen(add)
		html = response.read()
		soup = bs.BeautifulSoup(html, 'html.parser')
		section = soup.find("h2", id = "uttar pradesh 2017")
		if section == None:
			continue
		section = section.parent.parent.parent
		archive = section.find("ul", class_ = "archive-list")
		for a in archive.find_all('a', href=True):
			# print a['href'],
			temp1 = urllib2.urlopen(a['href'])
			temp2 = temp1.read()
			contentPage = bs.BeautifulSoup(temp2, 'html.parser')
			author = contentPage.find("a", class_="auth-nm")
			articleData = ""
			authorName = None
			if author == None:
				authorName = "Hindu"
			else:
				authorName = (author.get_text().encode("ascii","ignore").strip("\n"))
			print authorName
			allContentContainer = contentPage.find("div", id=re.compile("^content-body"))
			allContent = allContentContainer.find_all("p")
			for each in allContent:
				articleData = articleData + ' ' + each.get_text().encode("ascii","ignore")
			if(i=="03" and (int)(j)>8):
				fd = open("./After/"+str(afterCount)+".txt","w")
				fd.write(authorName+'\n')
				fd.write(articleData)
				afterCount+=1
			else:
				fd = open("./Before/"+str(beforeCount)+".txt","w")
				fd.write(authorName+'\n')
				fd.write(articleData)
				beforeCount+=1
			time.sleep(1)
