#import statements
import os
import webbrowser
import json
import time
from pprint import pprint

def main():
    topParent = getTopParent()
    saveFile = "testCaseResults_{0}.html".format(getTimeStamp())    
    
    list_testFileNames = getTests(topParent)
    list_oracleFileNames = getOracles(topParent)
    htmlStr = runTestCase(topParent, list_testFileNames, list_oracleFileNames)
    createResults(topParent, saveFile, htmlStr)
    openHtml(topParent, saveFile)

def getTimeStamp():
    timeStamp = ""
    
    currentTime = time.localtime()[:6]
    
    for element in currentTime:
        if(len(str(element)) == 4):
            timeStamp += str(element)
        else:
            timeStamp += "{0:0>2}".format(str(element))
    return timeStamp    
             



def getTests(topParent):
    fileStr = topParent + "testCases"
    '''get test cases as a comma delimited list'''
    return os.listdir(fileStr)
    
def getOracles(topParent):
    fileStr = topParent + "oracles"

    '''get oracles as a comma delimited list'''
    return os.listdir(fileStr)
    
def runTestCase(topParent, fileNameList, oracleList):
    htmlStr = ""
    for fileName, oracleName in zip(fileNameList, oracleList):
        htmlStr += doTest(topParent + "testCases\\" + fileName, oracleName)
    return htmlStr

def doTest(fileName, oracleName):
    '''
    data = []
    with open(fileName) as data_file:
        for line in data_file:
            data.append(json.loads(line))
    
    tc_id = data["id"]
    tc_title = data["title"]
    tc_req = data["req"]
    tc_testVal = data["testVal"]
    tc_oracle = "x"
    tc_result = "Passed" 
    '''
    tc_id = "001"
    tc_title = "One Variable and Positive Literal"
    tc_req = ""
    tc_testVal = "x + 2"
    tc_oracle = "x + 2"
    tc_result = "Passed" 

    return '<div class="accordion-inner" id="tc_{0}"><div class="accordion" id="tcAccordion{0}"><div class="accordion-group"><div class="accordion-heading"><a class="accordion-toggle" data-toggle="collapse" data-parent="#tcAccordion{0}" href="#tcDetailsPanel{0}"><div class="row"><div class="col-lg-2"><p id="tc_id{0}">{0}</p></div><div class="col-lg-7"><p id="tc_title{0}">{1}</p></div><div class="col-lg-3"><p id="tc_status{0}">{2}</p></div></div></a></div><div id="tcDetailsPanel{0}" class="accordion-body collapse"><div class="accordion-inner divShading-beige" id="tcDetails{0}"><div class="row"><div class="col-lg-12"><p id="tc_req{0}"><strong>Requirement: </strong>{3}</p></div></div><div class="row"><div class="col-lg-3 col-lg-offset-3"><p id="tc_testVal{0}"><strong>Test Value: </strong>{4}</p></div><div class="col-lg-3"><p id="tc_oracle{0}"><strong>Oracle: </strong>{5}</p></div></div></div></div></div></div></div>'.format(tc_id, tc_title, tc_result, tc_req, tc_testVal, tc_oracle)

def createResults(topParent, saveFile, htmlStr):
    fileStr = topParent + "reports"

    outFile = open(fileStr + "\\" + saveFile, 'w')

    outFile.write(
            '<!DOCTYPE html>' +
            '<html>' +
                '<head>' +
                    '<title>Page Title</title>' +
                    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.4/flatly/bootstrap.min.css" />' +
                    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" />' +
                    '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>' +
                    '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>' +
                '</head>' +
                '<body>' +
                    '<div class="container">' +
                        '<div id="top"></div>' +
			'<div id="mid">' +
                            '<div class="accordion-group">' +
                                '<div class="accordion-heading">' +
                                    '<a class="">' +
                                        '<div class="row center">' +
                                            '<div class="col-lg-2">' +
                                                '<h5 id="heading_id"><strong>ID</strong></h5>' +
					    '</div>' +
					    '<div class="col-lg-7">' +
                                                '<h5 id="heading_title"><strong>Title</strong></h5>' +
					    '</div>' +
					    '<div class="col-lg-3">' +
                                                '<h5 id="heading_status"><strong>Status</strong></h5>' +
					    '</div>' +
					'</div>' +
				    '</a>' +
                                '</div>' +
                                '<div id="aclDetailsCollapse" class="accordion-body">' +
                                    htmlStr +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div id="bottom"></div>' +
                    '</div>' +
                '</body>' +
            '</html>')

def openHtml(topParent, fileName):
    fileStr = topParent + "reports"
    url = 'file://' + os.path.realpath(fileStr + '\\' + fileName)
    browser = 2

    webbrowser.open(url, new=browser, autoraise=False)

def getTopParent():
    '''get current directory'''	
    str_dirPath = os.path.dirname(os.path.realpath(__file__))

    '''get top parent'''
    return str_dirPath[:(str_dirPath.index("scripts"))]
        

main()
