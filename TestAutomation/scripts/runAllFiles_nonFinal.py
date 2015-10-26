def main():
    saveFile = "testCaseResults"
    appendToHtmlStr = ''
    
    createResults(saveFile)
    list_testFileNames = getTests()
    list_oracleFileNames = getOracles()
    runTestCase(list_testFileNames)
    appendToHtml(appendToHtmlStr)

def createResults(saveFile):

    outFile = open(saveFile, 'w')

    outFile.write(
            "<!DOCTYPE html>" +
            "<html>" +
                "<head>" +
                    "<title>Page Title</title>" +
                    "<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.4/flatly/bootstrap.min.css" />" +
                    "<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" />" +
                    "<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>" +
                    "<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>" +
                "</head>" +
                "<body></body>" +
            "</html>")

def getTests():
    f
    
def getOracles():
    f
    
def runTestCase(fileNameList):
    for(fileName in fileNameList):
        result = doTest(fileName)

def doTests(fileName):
    tc_id = ''
    tc_title = ''
    tc_req = ''
    tc_testVal = ''
    tc_oracle = ''
    
    infile = open(fileName, 'r')
    #parse JSON file

    appendToHtmlStr += 
    
def appendToHtml(appendStr):
    f
    
        
        

main()
