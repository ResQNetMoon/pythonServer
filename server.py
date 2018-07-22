import http
from random import randint
from re import sub, findall
ort = randint(8080,9090)
print("Port: {}".format(ort))
server = http.WebServer(port=ort)
server.init()
htmlExtension = ['html','htm','phtml']
textExtension = ['txt','js','css','sass','tpl']
def getExtension(name):
#	print(name)
	try:
		ext = findall(r'\w+\.$', name)[0].lower()
	except IndexError:
		return ''
	else:
		return ext
@server.connection_handler
def on_connect(conn,addr,data):
	IP = addr[0]
	Path = sub(r"^\/", './', data['requestPath'])
	if Path == './':
		Path = "index.html"
	try:
		f = open("www/"+Path)
		htmlTo = f.read()
		f.close()
	except FileNotFoundError:
		htmlTo = "<center><h1>404 Not Found</h1></center>"
	except IsADirectoryError:
		pjoin(Path, 'index.html')
		f = open("www/"+Path)
		htmlTo = f.read()
		f.close()
	ext = getExtension(Path)
	if ext.lower() in textExtension:
		html = htmlTo
	elif ext.lower() in htmlExtension:
		html = http.parser.Lex(htmlTo)
	else:
		#print(ext)
		try:
			f = open("www/"+Path)
		except FileNotFoundError:
			html = "404"
			return http.parser.httpPreparse(html)
		html = f.read()
		f.close()
		htmlTo = http.parser.Lex(html)
		#print(htmlTo)
	return http.parser.httpPreparse(htmlTo)
server.start()