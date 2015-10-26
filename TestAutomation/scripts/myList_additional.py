'''import statements'''
import os
import webbrowser

'''function to iterate through list and create html code for each element'''
def listToHtmlString(list):
	size = len(list)
	str_Html = ""
	
	for i in range (0, size):
		str_Html += '<p>' + list[i] + '</p><br />'
	return str_Html

'''get current directory'''	
str_dirPath = os.path.dirname(os.path.realpath(__file__))

'''get top parent'''
str_topParent = str_dirPath[:(str_dirPath.index("\\") + 1)]

'''get files in parent directory as a comma delimited list'''
list_topDir = os.listdir(str_topParent)

'''build HTML string'''
str_html = '<!DOCTYPE html><html><head><title>Top Level Files</title></head><body>' + listToHtmlString(list_topDir) + '</body></html>'
		
'''open/create new Html file in current directory'''		
newFile = open(str_dirPath + "\\" + "fileContents.html", "w")
newFile.write(str_html)

'''open saved file in default browser (see note below)'''
browser = 2
url = 'file://' + os.path.realpath('fileContents.html')
webbrowser.open(url, new=browser)

'''note: this seems to work when "url" is an actual web address; "www.google.com"
for example. However, when using a local file, this opens it in a 
text editor instead of the browser. Not sure why; still researching.'''
