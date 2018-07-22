from re import sub, findall,split
import http.UserModel as UserModel
def stringify(text):
	byte = sub(r"(\"|\')$", "", sub(r"^(\"|\')", "", text))
	return byte
def isMobile(user_agent):
	phones = '(iPhone,BlackBerry,Android,Meizu,MIUI,XiaoMi,Miui)'.replace(",", "|")
	return True if len(findall(phones,user_agent)) >= 1 else False
def reComp(text):
	data=text.replace('"', '\\"').replace("(", "\\(").replace("[", "\\[").replace(']', '\\]')
	data=data.replace("$", "\\$").replace("^", "\\^").replace(")", "\\)")
	data=data.replace("{", "\\{").replace("}", "\\}")
	return data
def FormatHttpRequest(requestText):
	requestText = requestText.split('\r\n')
	if findall('GET$', requestText[0]):
	#	print(requestText)
		requestText.pop(len(requestText)-1)
		requestText.pop(len(requestText)-1)
	#	print(requestText)
	json = {}
	first = True
	for event in requestText:
		data = event.split(': ')
		if first:
			first = False
			continue
		try:
			json[data[0]] = data[1]
		except IndexError:
			continue
	opr = requestText[0].split(' ')
	json['requestPath'] = opr[1]
	proto = opr[2].replace(' ', '').split('/')
	#print(proto)
	json['proto'] = {'version':proto[1], 'name':proto[0]}
	return json
	
def httpPreparse( html, httpOp="OK", code=200,server='Night',other="", content_type='text/html'):
	if other.strip() != "":
		other = "\r\n"+other
	return b"HTTP/1.1 "+str(code).encode('utf-8')+b" "+httpOp.encode("utf-8")+b"\r\nContent-Type: "+content_type.encode("utf-8")+b";\r\nServer: "+server.encode("utf-8")+other.encode("utf-8")+b"\r\n\r\n"+html.encode("utf-8")
	
def Lex(text):
	isThere = findall(r'\{\{.+\}\}', text)
	for event in isThere:
		data = sub(r'^\{\{\s*', '', sub(r'\s*\}\}$', '', event))
		try:
			digit = eval("UserModel."+data)
		except:
			digit = "Error in module or module not found"
		text = text.replace(event, digit)
	return text
