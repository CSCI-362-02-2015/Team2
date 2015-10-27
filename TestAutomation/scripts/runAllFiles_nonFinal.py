#import statements
import os
import webbrowser
import json
import time
from pprint import pprint

htmlStr = ''
topParent = getTopParent()

def main():    
    saveFile = "testCaseResults_{0}.html".format(getTimeStamp())    
    
    list_testFileNames = getTests()
    list_oracleFileNames = getOracles()
    
    runTestCase(list_testFileNames, list_oraclsFileNames)
    createResults(saveFile)
    openHtml(saveFile)

def getTimeStamp():
    timeStamp = ""
    
    currentTime = time.localtime()[:6]
    
    for element in currentTime:
        if(len(str(element)) == 4):
            timeStamp += str(element)
        else:
            timeStamp += "{0:0>2}".format(str(element))
    return timeStamp    
             

def createResults(saveFile):
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
                                                '<h5 id="heading_id">ID</h5>' +
					    '</div>' +
					    '<div class="col-lg-7">' +
                                                '<h5 id="heading_title">Title</h5>' +
					    '</div>' +
					    '<div class="col-lg-3">' +
                                                '<h5 id="heading_status">Status</h5>' +
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

def getTests():
    fileStr = topParent + "testCases"

    '''get test cases as a comma delimited list'''
    return os.listdir(fileStr)
    
def getOracles():
    fileStr = topParent + "oracles"

    '''get oracles as a comma delimited list'''
    return os.listdir(fileStr)
    
def runTestCase(fileNameList, oracleList):
    for fileName, oracleName in zip(fileNameList, oracleList):
        result = doTest(fileName, oracleName)

def doTests(fileName, oracleName):
    tc_id = ''
    tc_title = ''
    tc_req = ''
    tc_testVal = ''
    tc_oracle = ''
    tc_result = ''
    
    infile = open(fileName, 'r')
    #parse JSON file

    htmlStr += '<div class="accordion-inner" id="tc_{0}"><div class="accordion" id="tcAccordion{0}"><div class="accordion-group"><div class="accordion-heading"><a class="accordion-toggle" data-toggle="collapse" data-parent="#tcAccordion{0)" href="#tcDetailsPanel{0}"><div class="row"><div class="col-lg-2"><p id="tc_id{0}">{0}</p></div><div class="col-lg-7"><p id="tc_title{0}">{1}</p></div><div class="col-lg-3"><p id="tc_status{0}">{2}</p></div></div></a></div><div id="tcDetailsPanel{0}" class="accordion-body collapse"><div class="accordion-inner divShading-beige" id="tcDetails{0}"><div class="row"><div class="col-lg-12"><p id="tc_req{0}"><strong>Requirement: </strong>{3}</p></div></div><div class="row"><div class="col-lg-3 col-lg-offset-3"><p id="tc_testVal{0}"><strong>Test Value: </strong>{4}</p></div><div class="col-lg-3"><p id="tc_oracle{0}"><strong>Oracle: </strong>{5}</p></div></div></div></div></div></div></div>'.format(tc_id, tc_title, tc_result, tc_req, tc_testVal, tc_oracle)

def openHtml(fileName):
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
