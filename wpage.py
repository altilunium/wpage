import sys
from bs4 import BeautifulSoup
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
import datetime
import lxml


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)



pname = sys.argv[1]
if pname == "-i":
	pname = input("Enter Wikipedia Article Name : ")
	subwiki = input("Enter Wikipedia Language (en/id) : ")
else:
	try:
		subwiki = sys.argv[2]
	except Exception as e:
		subwiki = 'id'

if subwiki == 'en':
	#url = "https://en.wikipedia.org/w/index.php?title=Special:Contributions/"+str(uname)+"&dir=prev&target=GeoWriter"
	url ="https://en.wikipedia.org/w/index.php?title="+str(pname)+"&dir=prev&action=history"
	baseurl = "https://en.wikipedia.org"
	lang = 'en'
else:
	#url = "https://id.wikipedia.org/w/index.php?title=Istimewa:Kontribusi_pengguna/"+str(uname)+"&dir=prev&limit=500"
	url = "https://id.wikipedia.org/w/index.php?title="+str(pname)+"&dir=prev&action=history"
	baseurl = "https://id.wikipedia.org"
	lang = 'id'





stop = False
wikiarticle = set()
byte_add = 0
byte_rem = 0
stage = 0
top_contrib = dict()



while not stop:

	stage += 500
	#print("Edit count : "+str(stage))

	


	#print(url)
	actualPayload = bytearray()
	response = requests.get(url)
	actualPayload = response.text
	soup = BeautifulSoup(actualPayload,'lxml')


	'''
	titles = soup.find_all("a",{"class":"mw-contributions-title"})
	titles_time = soup.find_all("a",{"class":"mw-changeslist-date"})
	bytescontrib = soup.find_all("span",{"class":"mw-diff-bytes"})
	'''


	next_url = soup.find("a",{"class":"mw-prevlink"})
	theList = soup.findAll("li",{"data-mw-revid":True})


	theList.reverse()
	for i in theList:
		c_user = i.find("a",{"class":"mw-userlink"})
		try:
			c_user = c_user.find("bdi")
		except Exception as e:
			continue

		c_byte = i.find("span",{"class":"mw-diff-bytes","data-mw-bytes":True})
		c_pos = i.find("span",{"class":"mw-plusminus-pos"})
		c_neg = i.find("span",{"class":"mw-plusminus-neg"})
		c_pts = 0
		if c_pos is None and c_neg is None:
			c_pos = i.find("strong",{"class":"mw-plusminus-pos"})
			c_neg = i.find("strong",{"class":"mw-plusminus-neg"})
		
		


		#print(c_neg.text)
		if c_neg :
			c_pts = c_neg.text.replace("−","-")
			#print(c_pts)
		elif c_pos:
			#print(c_pos.text)
			c_pts = c_pos.text
		else:
			continue

		if lang == 'en':
			c_pts = c_pts.replace(",","")
		else:
			c_pts = c_pts.replace(".","")


		#print(c_user.text)
		#print(c_byte["data-mw-bytes"])
		if c_user.text not in top_contrib:
			top_contrib[c_user.text] = int(c_pts)
			#print(c_pts)
			#print(int(c_pts))
			print(str(c_user.text) +" : "+str(top_contrib[c_user.text]))			
		else:
			old = top_contrib[c_user.text]
			top_contrib[c_user.text] += int(c_pts)
			print(str(c_user.text) +" : "+str(int(c_pts))+" ["+str(old)+"->"+str(top_contrib[c_user.text])+"]")
		

		links = i.find("span",{"class":"mw-history-histlinks"})
		links = links.findAll("a")
		if len(links) == 2:
			print(baseurl+str(links[1].attrs["href"]))
			print()

	parsed = urlparse.urlparse(url)
	try:
		x = parse_qs(parsed.query)['offset']
		x = x[0].split("|")
		x = x[0]
		dobj = datetime.datetime.strptime(x,'%Y%m%d%H%M%S')
		print(str(dobj)+" : "+str(len(top_contrib)) + " contributors")
	except Exception as e:
		None		

	



	

	'''
	titles.reverse()
	titles_time.reverse()
	counter = 0

	if len(titles) != len(titles_time):
		nodate = True
	for i in titles:
		if not nodate:
			print(str(titles_time[counter].text)+" : "+str(i.text))
		else:
			print(str(titles_time[counter].text)+" : "+str(i.text))
		print(baseurl+titles_time[counter].attrs["href"])
		print()
		counter += 1
	'''
		
	'''
	for i in bytescontrib:
		#print(i.text)
		a = i.text.replace("−","-")
		contrib = int(a)
		if contrib >= 0:
			byte_add += contrib
		else:
			byte_rem += contrib
	'''


	try :
		next_url = next_url.attrs["href"]
		url = baseurl + next_url
	except Exception as e:
		stop = True


'''
for i in wikiarticle:
	print(i)
'''

'''
print("Addition "+sizeof_fmt(byte_add))
print("Deletion "+sizeof_fmt(byte_rem))
'''

for i in sorted(top_contrib,key=top_contrib.get,reverse=False):
	print(str(i) +" : "+ str(top_contrib[i])) 
