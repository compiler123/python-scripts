
# FileTagger [SourceCode]

default_tag = " [SourceCode]"

import os, re

def renamedir(pwd):
	list = os.listdir(pwd)
	for item in list:
		fullpath = pwd+os.sep+item
		if fullpath==self: continue
		if os.path.isdir(fullpath):
			renamedir(pwd+os.sep+item)
			continue
		try:
			if type==1:
				x = re.match("^(.*)(\.[A-Za-z0-9]+)$",item)
				x = pwd+os.sep+x.group(1)+tag+x.group(2)
			if type==0:
				x = re.match("^(.*)"+re.escape(tag)+"(\.[A-Za-z0-9]+)$",item)
				x = pwd+os.sep+x.group(1)+x.group(2)
			print "Renaming \""+fullpath+"\" to \""+x+"\" ...\n"
			os.rename(fullpath,x)
		except:
			error.append(fullpath)

if __name__=="__main__":
	self = os.getcwd()+os.sep+os.path.basename(__file__)
	error = []
	print "FileTagger [SourceCode]\n"
	print "Enter the tag you wish to append/remove (ENTER for default) :",
	x = raw_input()
	if x=="": tag = default_tag
	else: tag = x
	while True:
		try:
			print "Enter 1 if you wish to append the tag, 0 to remove it       :",
			x = int(raw_input())
			if x==1:
				type = 1
				break
			if x==0:
				type = 0
				break
		except: continue

	renamedir(os.getcwd())
	if len(error)>0:
		print "Errors encountered while renaming the following files : "
		for item in error: print item
	os.system("pause")