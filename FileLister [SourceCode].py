
# FileLister [SourceCode]

import os, re

def size(x):
	x = float(x)
	if x<1024: return "%.3f B" % (x)
	x/=1024;
	if x<1024: return "%.3f KB" % (x)
	x/=1024;
	if x<1024: return "%.3f MB" % (x)
	x/=1024;
	if x<1024: return "%.3f GB" % (x)
	x/=1024;
	return "%.3f TB" % (x)

def filelist(pwd):
	global id
	try: list = sorted(os.listdir(pwd))
	except: return
	data = "<div id='subdir"+str(id)+"' style='display:none;'><ul>"
	stats = [id,0,0,0] # files, dirs, size
	id += 1
	for item in list:
		fullpath = pwd+os.sep+item
		if fullpath in exclude: continue
		if os.path.isdir(fullpath):
			try: x,y = filelist(fullpath)
			except: continue
			stats[1]+=y[1]
			stats[2]+=1
			stats[3]+=y[3]
			data+="<li class='dir'>"
			data+="<a onClick=\"toggle('subdir"+str(y[0])+"');\">"+item+" <e>("+str(y[1])+" file(s), "+str(y[2])+" folder(s), "+size(y[3])+")</e></a>"
			data+=x
		else:
			try: y = os.path.getsize(fullpath)
			except: y = 0
			data+="<li>"
			data+=item+" <e>("+size(y)+")</e>"
			stats[1]+=1
			stats[3]+=y
		data+="</li>"
	if stats[1]==0 and stats[2]==0:
		data+="<li><e>(directory empty)</e></li>"
	data+="</ul></div>"
	return (data,stats)

if __name__=="__main__":
	exclude = [ os.getcwd()+os.sep+os.path.basename(__file__) , os.getcwd()+os.sep+os.getcwd().split(os.sep)[-1]+" [FileLister][SourceCode].html" ]
	id = 0
	title = os.getcwd().split(os.sep)[-1]+" [FileLister][SourceCode]"
	data,stats = filelist(os.getcwd())
	print "FileTagger [SourceCode]\n"
	print "Writing directory index to '"+exclude[1]+"' ...",
	f = open(exclude[1],"w")
	f.write("""
<html><head>
<title>"""+title+"""</title>
<style>* { font-family:'Tahoma'; font-size:12px; } h { font-weight:bold; font-size:16px; } a { color:black; font-weight:bold; cursor:pointer; } e { color:gray; } li { list-style:none; } li.dir { list-style:disc outside none; }</style>
<script>function toggle(id){ e = document.getElementById(id); if(e) e.style.display = (e.style.display!='block'?'block':'none'); }</script>
</head><body>
<ul><li class='dir'><a onClick="toggle('subdir"""+str(stats[0])+"""');">"""+os.getcwd()+" <e>("+str(stats[1])+" file(s), "+str(stats[2])+" folder(s), "+size(stats[3])+")</e></a>")
	f.write(data)
	f.write("</li></ul>\n<script>toggle('subdir0')</script></body></html>")
	f.close()
	print "done\n"
	os.system("pause")
