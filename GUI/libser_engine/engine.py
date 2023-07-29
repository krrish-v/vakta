
import requests
from bs4 import BeautifulSoup
from libser_engine.utils import payload
from libser_engine.utils.exception import GoogleCaptcha, GoogleCookiePolicies
import re
import urllib3

class Extract:

	#____________________________________________
	# duckduckgo.com
	#-------------------------------------------
	def duckduckgo_search(self, qury: str):
		
		self.qury = qury
		self.paylod, self.cookie = payload.Headers().duckduckgo_parm()

		link = []
		try:
			self.link = 'https://html.duckduckgo.com/html/?t=ffab&q=' + self.qury  + '&ia=software'
			req = requests.get(self.link, headers=self.paylod, allow_redirects=False, timeout=10)
			self.data = req.text
			status = req.status_code

            # data extrcation from search page
			if status == 200:
				soup = BeautifulSoup(self.data, 'html.parser')

				for link_ in soup.find_all('a', href=True):
					lnks = link_['href']

					try:
						q = lnks.split('=')[1]
						w = q.split('&rut')[0]
						escp = payload.escape_codes
						for e in escp:
							if e in w:
								w = w.replace(e, escp[e])
						link.append(w)
					
					except: None
                
				filter_link = []
				# removing a similar link
				for k in link:
					if 'duckduckgo.com'not in k:
						if k not in filter_link:
							filter_link.append(k)
				
				return filter_link
			
			elif status == 403: return False

		except: return False

	#______________________________________
	# google.com
	#-------------------------------------
	def google_search(self, target, total, filetype):
		
		self.word = target
		self.filetype = filetype
		self.counter = 50
		self.quantity = "100"
		self.agent = payload.Headers().user_agent()

		urllib3.disable_warnings()

		documents = []
		num = 50 if total > 50 else total

		url_base = f"https://www.google.com"
		#cookies = {"CONSENT": "YES+srp.gws"}

		header = payload.Headers().google_parm()
		
		try:
				
			url = url_base + f"/search?num="+self.quantity+"&start=" + str(self.counter) + "&hl=en&meta=&q=filetype:"+self.filetype+ ' ' + self.word
			response = requests.get(url, headers=header, timeout=5, verify=False, allow_redirects=False)
			
			text = response.text
			content = response.content
			
			if response.status_code == 302 and ("htps://www.google.com/webhp" in text or "https://consent.google.com" in text):
				return [] #raise GoogleCookiePolicies()
			if "detected unusual traffic" in text:
				return [] #raise GoogleCaptcha()
			
			soup = BeautifulSoup(content, features="lxml")
			#print(soup)
			
			for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
				link = re.split(":(?=http)",link["href"].replace("/url?q=",""))

				filtered_link = link[0].split('&sa=')[0]
				if '.pdf' in filtered_link:
					documents.append(filtered_link)

			return documents

		except: return [] #It's left over... but it stays there'''



class accumulate:

	def __init__(self, query, filetype):
		self.query = query
		self.filetype = filetype

		self.extract = Extract()

	def google(self):
		
		try: self.link =  self.extract.google_search(self.query, 40, self.filetype)
		except: self.link = []
	
		return self.link
	
	def duckgo(self):
		query = self.query + ' filetype:' + self.filetype
		
		try: self.link = self.extract.duckduckgo_search(query)
		except: self.link = False

		data = []
		
		if self.link is not False:
			for i in self.link:

				if '.pdf' in i:
					data.append(i)
		
			return data
				
		else: return []

	def all(self):
		list1 = self.google()
		if not list1:
			list1 = self.duckgo()

		return list1
