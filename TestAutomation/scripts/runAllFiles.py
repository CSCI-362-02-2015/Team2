#import statements
import os
import webbrowser
import json
import time
from pprint import pprint

from selenium import webdriver # pip install selenium
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageChops

#main gets top parent of folder and runs all other functions
def main():
    topParent = getTopParent()
    saveFile = "testCaseResults_{0}.html".format(getTimeStamp())    
    
    list_testFileNames = getTests(topParent)
    htmlStr = runTestCases(topParent, list_testFileNames)
    createResults(topParent, saveFile, htmlStr)
    openHtml(topParent, saveFile)

#get unique timestamp for file name
def getTimeStamp():
    timeStamp = ""
    
    currentTime = time.localtime()[:6]
    
    for element in currentTime:
        if(len(str(element)) == 4):
            timeStamp += str(element)
        else:
            timeStamp += "{0:0>2}".format(str(element))
    return timeStamp      

#gets a list of testCase fileNames
def getTests(topParent):
    fileStr = topParent + "testCases"
    return os.listdir(fileStr)

#calls "doTest()" for testCases and oracles
def runTestCases(topParent, fileNameList):
    def wait_until_load():
        def page_has_loaded(): return driver.execute_script('return document.readyState;') == 'complete'
        time.sleep(1)
        count = 0
        while not(page_has_loaded() or count==10):
            time.sleep(0.25)
            count+=1

    def doTest(file_path, file_name):
        data = []
        with open(file_path) as data_file:
            text = data_file.read().replace("\n", '').replace("\t", ' ').encode('unicode-escape')
            # print text
            data = json.loads(text, strict=False)
        
        tc_id = data["id"]
        tc_title = data["title"]
        tc_req = data["req"]
        tc_comp = data["component"]
        tc_method = data["method"]
        tc_testVal = data["testVal"]
        tc_oracle = '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mstyle displaystyle="true" scriptlevel="0"><mrow class="MJX-TeXAtom-ORD">' + data["oracle"][6:] + '</mstyle></math>'
        tc_oracle  = " ".join(tc_oracle.encode('unicode-escape').split()).replace("> <", "><").replace("\'","\"")

        result_path = topParent + "temp/testResults/%s" % tc_oracle
        input_box = driver.find_element_by_id("MathInput")
        output_box = driver.find_element_by_id("outputBox")
        input_box.clear() #clear input box
        input_box.send_keys(tc_testVal) #type testcase into box
        input_box.send_keys(Keys.RETURN) #hit enter
        wait_until_load()
        result = " ".join(output_box.text.encode('unicode-escape').split()).replace("> <", "><").replace("<!-- \u2212 -->","").replace('&ndash;', '-')
        tc_result = "Passed" if tc_oracle == result else "Failed" # UNCOMMENT TO TEST, COMMENT TO SAVE ORACLES
        
        def html_to_string(inSTR):
            return inSTR.replace('<', '&lt;').replace('>', '&gt;')

        html = '<div class="accordion-inner" id="tc_{0}">'+ \
                    '<div class="accordion" id="tcAccordion{0}">'+ \
                        '<div class="accordion-group">' + \
                            '<div class="accordion-heading">'+ \
                                '<a class="accordion-toggle" data-toggle="collapse" data-parent="#tcAccordion{0}" href="#tcDetailsPanel{0}">'+ \
                                    '<div class="row">'+ \
                                        '<div class="col-lg-3">'+ \
                                            '<p id="tc_id{0}">{0}</p>'+ \
                                        '</div>'+ \
                                        '<div class="col-lg-6">'+ \
                                            '<p id="tc_title{0}">{1}</p>'+ \
                                        '</div>'+ \
                                        '<div class="col-lg-3">'+ \
                                            '<p id="tc_status{0}">{2}</p>'+ \
                                        '</div>'+ \
                                    '</div>'+ \
                                '</a>'+ \
                            '</div>'+ \
                            '<div id="tcDetailsPanel{0}" class="background-color-blanchedalmond accordion-body collapse">'+ \
                                '<div class="accordion-inner divShading-beige" id="tcDetails{0}">'+ \
                                    '<div class="row">'+ \
                                        '<div class="col-lg-12 txt-align-center">'+ \
                                            '<p id="tc_req{0}"><strong>Requirement:</strong>{3}</p>'+ \
                                        '</div>'+ \
                                    '</div>'+ \
                                    '<div class="row">'+ \
                                        '<div class="col-lg-4 txt-align-center">'+ \
                                            '<p id="tc_req{0}"><strong>Test Component:</strong>{5}</p>'+ \
                                        '</div>'+ \
                                        '<div class="col-lg-4 txt-align-center">'+ \
                                            '<p id="tc_req{0}"><strong>Test Value:</strong>{4}</p>'+ \
                                        '</div>'+ \
                                        '<div class="col-lg-4 txt-align-center">'+ \
                                            '<p id="tc_req{0}"><strong>Method:</strong>{6}</p>'+ \
                                        '</div>'+ \
                                    '</div>'+ \
                                    '<div class="row">'+ \
                                        '<div class="col-lg-12">'+ \
                                            '<p><strong>Oracle:</strong>{7}</p>'+ \
                                        '</div>'+ \
                                    '</div>'+ \
                                    '<div class="row">'+ \
                                        '<div class="col-lg-12">'+ \
                                            '<p><strong>Result:</strong>{8}</p>'+ \
                                        '</div>'+ \
                                    '</div>'+ \
                                '</div>'+ \
                            '</div>'+ \
                        '</div>'+ \
                    '</div>'+ \
                '</div>'
        return html.format(tc_id, tc_title, tc_result, tc_req, tc_testVal, tc_comp, tc_method, html_to_string("%r"%tc_oracle), html_to_string("%r"%result))

    driver = webdriver.Firefox()
    skeleton_file_path = topParent + "project/src/skeleton.html"
    driver.get("file:///" + skeleton_file_path) #navigate to skeleton file
    wait_until_load()
    htmlStr = ""
    for file_name in fileNameList:
        file_path = topParent + "testCases/" + file_name
        htmlStr += doTest(file_path, file_name)
    driver.quit()
    return htmlStr


#creates results HTML file
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
                    '<style>' +
                            '.mdl-panel-title{font-weight:bold; text-decoration:underline; text-align:center;}' +
                            '.padding-left-25p{padding-left:25px;}' +
                            '.border-right-shaded{border-right:2px solid #e5e5e5;}' +
                            '.modal-85pct{width:85%;}' +
                            '.txt-align-center{text-align:center;}' +
                            '.overflow-hidden{overflow:hidden;}' +
                            '.font-size-large{font-size:large;}' +
                            '.float-right{float:right;}' +
                            '.margin-top-4p{margin-top:4px;}' +
                            '.margin-top-n15p{margin-top:-15px;}' +
                            '.background-color-aliceblue{background-color:aliceblue;}' +
                            '.accordion-heading{text-align:center;}' +
                            '.background-color-blanchedalmond{background-color:blanchedalmond;}' +
                    '</style>' +
                '</head>' +
                '<body>' +
                    '<div class="container">' +
                        '<div id="top">' +
                            '<nav class="navbar navbar-default">' +
                              '<div class="container-fluid">' +
                                    '<div class="navbar-header">' +
                                      '<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">' +
                                            '<span class="sr-only">Toggle navigation</span>' +
                                            '<span class="icon-bar"></span>' +
                                            '<span class="icon-bar"></span>' +
                                            '<span class="icon-bar"></span>' +
                                      '</button>' +
                                      '<a class="navbar-brand" href="#"><img class="margin-top-n15p" src="./project/src/logo.PNG"><img></a>' +
                                    '</div>' +
                                    '<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1"></div>' +
                              '</div>' +
                            '</nav>' +
                        '</div>' +
			'<div id="mid">' +
                            '<div class="accordion-group">' +
                                '<div class="accordion-heading background-color-aliceblue">' +                                    
                                    '<div class="row center">' +
                                        '<div class="col-lg-3">' +
                                            '<h5 id="heading_id"><strong>ID</strong></h5>' +
					'</div>' +
					'<div class="col-lg-6">' +
                                            '<h5 id="heading_title"><strong>Title</strong></h5>' +
					'</div>' +
					'<div class="col-lg-3">' +
                                            '<h5 id="heading_status"><strong>Status</strong></h5>' +
					'</div>' +
				    '</div>' +				    
                                '</div>' +
                                '<div id="aclDetailsCollapse" class="accordion-body">' +
                                    htmlStr +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div id="bottom"></div>' +
                    '</div>' +
                    '<div class="modal fade" id="mdlOracle" tabindex="-1" role="dialog" data-backdrop="static" data-keyboard="false">' +
                        '<div class="modal-dialog modal-85pct" role="document">' +
                            '<div class="modal-content">' +
                                '<div class="modal-header">' +
                                    '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
                                    '<h4 class="modal-title" id="mdlOracle_title"><span class="font-size-large label" id="mdlOracle_status"></span></h4>' +
                                '</div>' +
                                '<div class="modal-body">' +
                                    '<div class="row">' +
                                        '<div class="col-lg-6 border-right-shaded">' +
                                            '<h4 class="mdl-panel-title">Test:</h4>' +
                                            '<div class="overflow-hidden col-lg-11 padding-left-25p"><img id="mdlTest_img" src="" /></div>' +
					'</div>' +
					'<div class="col-lg-6">' +
                                            '<h4 class="mdl-panel-title">Oracle:</h4>' +
                                            '<div class="overflow-hidden col-lg-11 padding-left-25p"><img id="mdlOracle_img" src=""></div>' +
					'</div>' +
                                    '</div>' +
                                '</div>' +                       
                            '</div>' +
                        '</div>' +
                    '</div>' +
                    '<script>' +
                        '$("#mdlOracle").on("show.bs.modal", function (event) {' +
                            'var button = $(event.relatedTarget);' +
                            'var title = button.data("title");' +
                            'var img = button.data("img");' +
                            'var status = button.data("status");' +
                            'var statusLabel = status == "Passed" ? "label-success" : "label-danger";' +
                            '$("#mdlOracle_title").html(title + "&nbsp;&nbsp;&nbsp;" + $("#mdlOracle_title").html());' +
                            '$("#mdlOracle_img").attr("src", "../TestAutomation/oracles/" + img);' +
                            '$("#mdlTest_img").attr("src", "../TestAutomation/temp/testResults/" + img);' +
                            '$("#mdlOracle_status").text(status);' +
                            '$("#mdlOracle_status").addClass(statusLabel);' +
                        '});' +

                        '$("#mdlOracle").on("hide.bs.modal", function (event) {' + 
                            '$("#mdlOracle_title").html(\'<span class="font-size-large label" id="mdlOracle_status"></span>\');' + 		
                        '});' +
                    '</script>' +
                '</body>' +
            '</html>')

#opens HTML file in browser
def openHtml(topParent, fileName):
    fileStr = topParent + "reports"
    url = 'file://' + os.path.realpath(fileStr + '\\' + fileName)
    browser = 2

    webbrowser.open(url, new=browser, autoraise=False)

#gets working directory's top parent
def getTopParent():
    '''get current directory'''	
    str_dirPath = os.path.dirname(os.path.realpath(__file__))

    '''get top parent'''
    return str_dirPath[:(str_dirPath.index("scripts"))]
        

main()
