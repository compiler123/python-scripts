import re,os,sgmllib,string,sys,urllib

"""
This script is not perfect, but it does work majority of the time (when the format of the Wikipedia List of Episodes page uses the standard format).
Never rename files in the first attempt: always check the Output File completely first, ensure that all new names are accurate, and then do it.
Randomo tags like 720p may be mistakenly interpreted as S07E20, so you may need to manually remove them.
You may need to adjust the following constants to get proper results.
"""

title_column_offset = -1
season_number_offset = -1

def toint(x):
	try: return int(x)
	except: return 0
class MyParser(sgmllib.SGMLParser):
	def __init__(self,verbose=0):
		sgmllib.SGMLParser.__init__(self, verbose)
		self.status = 0
		self.namelist = {}
		self.invalidfilename = "[\\\/\:\*\?\"\<\>\|]"
		self.seriesname = "Unknown Series"
		self.season = 0
		self.episodenumber = 0
	def parse(self, data):
		self.feed(data)
		self.close()
	def start_table(self,attr):
		for key,value in attr:
			if key=="class" and "wikitable" in value.split() and self.status==0:
				self.status = 10
				self.titles = []
				self.column = []
				self.season+=1
	def end_table(self):
		if self.status==10:
			self.status = 0
			self.titles = []
	def start_title(self,attr):
		if self.status==0:
			self.status=1
			self.buffer=""
	def end_title(self):
		if self.status==1:
			self.seriesname = re.sub(self.invalidfilename,"",re.findall("^List of (.*) episodes \- Wikipedia\, the free encyclopedia$",self.buffer)[0])
			self.seriesname = self.seriesname.replace(" (2009 TV series)","")
			self.status=0
	def start_tr(self,attr):
		if self.status==10:
			self.status = 20
			for key,value in attr:
				if key=="class" and value=="vevent":
					self.status = 30
	def end_tr(self):
		if self.status==20:
			self.status = 10
			x = False # Whether or not Title appears in the column list
			for i in range(len(self.titles)):
				if self.titles[i]=="Title":
					self.titleindex = i+title_column_offset
					x = True
			#if not x: self.season = 0
		if self.status==30:
			self.status = 10
			if type==0:
				self.episodenumber += 1
				#key = "S%02dE%02d" % (toint(self.season-1),toint(self.column[self.titleindex-1]))
				key = "S%02dE%02d" % (toint(self.season)+season_number_offset,self.episodenumber)
			if type==1: key = toint(self.column[0])
			if len(self.column)>0 and key not in self.namelist:
				self.namelist[key] = re.sub("\[[0-9]+\]","",re.sub(self.invalidfilename,"",self.column[self.titleindex]).split("\n")[0])
			self.column = []
	def start_th(self,attr):
		if self.status==20:
			self.status = 21
			self.buffer = ""
	def end_th(self):
		if self.status==21:
			self.status = 20
			if "Volume" not in self.buffer:
				self.titles.append(self.buffer)
			self.episodenumber = 0
	def start_td(self,attr):
		#if self.status==20: self.status = 30
		if self.status==30:
			self.status = 31
			self.buffer = ""
	def end_td(self):
		if self.status==31:
			self.status = 30
			self.column.append(self.buffer)
	def handle_data(self,data):
		#print self.status
		if self.status==1: self.buffer+=data
		if self.status==21: self.buffer+=data
		if self.status==31: self.buffer+=data
	def rename(self,confirm=0):
		pwd = os.getcwd()
		list = os.listdir(pwd)
		for item in list:
			if os.path.isdir(item) or item==self: continue
			e = item.lower().split(".")[-1]
			if e not in ("avi","mkv","rm","rmvb","mp4","srt"): continue
			if type==1:
				x = sorted(map(int,re.findall("[0-9]+",item.replace("."+e,""))))
				z = self.seriesname
				for y in x: z+=" %03d" % (y)
				z+=" -"
				i = 1
				for y in x:
					if y not in self.namelist: continue
					if i==1:
						z+=" "+self.namelist[y]
						i+=1
					else: z+="; "+self.namelist[y]
				z+="."+e
				print item+"\n"+z
				if confirm==1:
					try: os.rename(item,z)
					except: pass
					print "Renaming",item,"to",z
				print
			if type==0:
				print item
				item2 = item
				item = item.replace("."+e,"")
				item = item.replace(" Episode ","x")
				z = self.seriesname
				n = {}
				x = map(string.upper,re.findall("([sS]?[0-9]+ ?[eEXx\.\-] ?[0-9]+)",item))
				for key in x:
					y = "S%02dE%02d" % tuple(map(int,re.findall("S?([0-9]+) ?[EX\.\-] ?([0-9]+)",key)[0]))
					try: n[y] = self.namelist[y]
					except: pass
					item = item.replace(y,"")
				x = map(int,re.findall("[0-9]+",item))
				for i in x:
					key = "S%02dE%02d" % (toint(i)/100,toint(i)%100)
					try: n[key] = self.namelist[key]
					except: pass
					item = item.replace(key,"")
				for key in sorted(n): z+=" "+key
				z+=" -"
				i = 1
				for key in sorted(n):
					if i==1:
						z+=" "+n[key]
						i+=1
					else: z+="; "+n[key]
				z+="."+e
				print z
				if confirm==1:
					try: os.rename(item2,z)
					except: pass
					print "Renaming",item2,"to",z
				print
					
			
if __name__=="__main__":
	self = os.path.basename(__file__)
	file_cache = ".".join(self.split(".")[0:-1])+" - Cache.txt"
	file_output = ".".join(self.split(".")[0:-1])+" - Output.txt"
	print "EpisodeNamer [SourceCode]\n"
	print "Indexing types : 0 = Seasonal (eg - S01E01,S01E02,...,S02E01,S02E02,...); 1 = Numerical (eg - 000,001,...,127,128,...; requires that the first column contain the absolute episode number)."
	while True:
		try:
			print "Enter the type of indexing that you wish to use (default = 0) :",
			type = raw_input()
			if type=="": type = 0
			type = int(type)
			if type in (0,1): break
		except: pass
	while True:
		print "Enter the Television Series Name or the Wikipedia URL where the required episode list can be found (default = use the same data as before, assuming that it is available) :",
		url = raw_input()
		if url=="":
			if os.path.exists(file_cache):
				f = open(file_cache,"r"); data = f.read(); f.close();
			else: continue
		else:
			if re.match("^http\:\/\/en\.wikipedia\.org\/wiki\/.*$",url)==None:
				url = "http://en.wikipedia.org/wiki/List_of_"+re.sub(" ","_",url)+"_episodes";
			class MyOpener(urllib.FancyURLopener):
				version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"
			myurlopen = MyOpener()
			print "Downloading data from the internet ...",
			try:
				webpage = myurlopen.open(url);
				data = webpage.read();
				webpage.close();
				if "Wikipedia does not have an article with this exact name." in data:
					raise Exception()
			except:
				print "error"
				continue
			print "done"
			f = open(file_cache,"w"); f.write(data); f.close();
		break
	print "Enter 'yes' if you actually wish to rename the files :",
	action = raw_input()
	if action=="yes": action = 1
	else: action = 0
	
	sys.stdout = open(file_output,"w")
	myparser = MyParser()
	myparser.parse(data)
	for key in sorted(myparser.namelist.keys()): print key, myparser.namelist[key]
	print
	myparser.rename(action)
	sys.stdout = sys.__stdout__
	
	os.system("pause")
