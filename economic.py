import bs4 as bs
import urllib2
import time

base_add = "https://economictimes.indiatimes.com/archivelist/year-2017,month-"
keywords = ["polls","election","Congress","BJP","Modi","Rahul","Amit","Hardik","Election","Polls","vote","Vote",
			"politics","EVM","Evm","evm","exit poll","constituencies","AAP"]
month = ["11","12"]
base_add2 = ",starttime-"
base_add3 = ".cms"
novday = []
decday = []
beforeCount = 365
afterCount = 146
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
for i in xrange(43060,43070):
	novday.append(str(i))
for i in xrange(43070, 43101):
	decday.append(str(i))
for i in month:
	lol = None
	if i=="11":
		lol = novday
	else:
		lol = decday
	for j in lol:
		add = base_add+i+base_add2+j+base_add3
		print "address:", add
		response = urllib2.Request(add, headers = hdr)
		page = urllib2.urlopen(response)
		html = page.read()
		soup = bs.BeautifulSoup(html, 'html.parser')
		listOfArticles = soup.find_all("ul", class_="content")
		links1 = listOfArticles[0].find_all("a")
		links2 = listOfArticles[1].find_all("a")
		links = []
		links.extend(links1)
		links.extend(links2)
		listOfLinks = []
		for each in links:
			flag = 0
			if "Gujarat" in each.string:
				# print each.string
				for key in keywords:
					if key in each.string:
						flag = 1
			if flag == 1:
				listOfLinks.append(each['href'])
		article_add = "https://economictimes.indiatimes.com"
		for each in listOfLinks:
			temp1 = article_add+each
			temp2 = urllib2.Request(temp1, headers=hdr)
			temp3 = urllib2.urlopen(temp2)
			contentPage = temp3.read()
			contentPageHTML = bs.BeautifulSoup(contentPage, 'html.parser')
			# print contentPageHTML.prettify()
			if contentPageHTML.find("div",class_="errBlock") != None:
				continue
			authorName = None
			author = contentPageHTML.find("div", class_="author")
			if author == None:
				author = contentPageHTML.find("div", class_="publisher flt")
				authorName = author.get_text().encode("ascii","ignore").strip("|")
			else:
				author = author.find("a")
				authorName = author.get_text().encode("ascii","ignore")
			content = ""
			allContent = contentPageHTML.find("div",class_="section1")
			stringContent = str(allContent.get_text().encode("ascii","ignore").replace('\n','')).replace('\t','').replace('    ','')
			print authorName
			if i=="12" and (int)(j)>43083:
				fd = open("./After/"+str(afterCount)+".txt","w")
				fd.write(authorName+'\n')
				fd.write(stringContent)
				afterCount+=1
			else:
				fd = open("./Before/"+str(beforeCount)+".txt","w")
				fd.write(authorName+'\n')
				fd.write(stringContent)
				beforeCount+=1
