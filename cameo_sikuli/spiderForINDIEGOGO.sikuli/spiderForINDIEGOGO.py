import os
import sys
import re
strBaseResFolderPath = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res" 
#open chrome
def openChrome():
    type("d", KeyModifier.WIN)
    click("1455954509662.png")
    waitVanish("1455954531674.png", 20)
# delete origin text
def delOriginText():
    type("a", KeyModifier.CTRL);
    sleep(2)
    type(Key.BACKSPACE);
    sleep(2)
#roll to page end
def rollToPageEnd():
    type(Key.END)
    wait("1456062534102.png", 20)
# open all project
def unfoldCategoryPage():
    rollToPageEnd()
    type(Key.PAGE_UP)
    wait("1456215300454.png", 20)
    while(exists("1456064164365.png")):
        click("1456064164365.png")
        waitVanish("1456215300454.png", 20)
        rollToPageEnd()
        type(Key.PAGE_UP)
        wait("1456215300454.png", 20)
#type url on chrome
def typeUrlOnChrome(urlText=""):
    click("1455955040522.png")
    sleep(2)
    delOriginText()
    type(urlText)
    sleep(2)
    type(Key.ENTER)
# go to explore page
def goExplorePage():
    typeUrlOnChrome(urlText="https://www.indiegogo.com/explore")
    wait("1455771252801.png", 20)
    wait("1456057892065.png", 20)
    sleep(5)
#choose folder at save progress
def typeFolderPath(strFolderPath):
    wait(Pattern("1456054857857.png").targetOffset(10,0), 20)
    click(Pattern("1456054857857.png").targetOffset(10,0))
    sleep(2)
    delOriginText()
    type(strFolderPath)
    sleep(2)
    type(Key.ENTER)
    sleep(2)
#ask chrome save current page
def saveCurrentPage(strFolderPath=None, strFilename="default.html"):
    type("s", KeyModifier.CTRL)    
    wait("1456076542071.png", 20)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    click(Pattern("1455959876192.png").targetOffset(36,0))
    sleep(2)
    delOriginText()
    sleep(2)
    type(strFilename)
    sleep(2)
    click("1455955227414.png")
    sleep(2)
#download explore pages
def downloadExplorePages():
    openChrome()
    goExplorePage()
    strExploreFolderPath = strBaseResFolderPath + r"\source_html\INDIEGOGO"
    if not os.path.exists(strExploreFolderPath):
            os.mkdir(strExploreFolderPath)
    saveCurrentPage(strFolderPath=strExploreFolderPath, strFilename="explore.html")
#download category pages
def downloadCategoryPages():
    strCategoryUrlListFilePath = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\category_url_list.txt"
    catUrlListFile = open(strCategoryUrlListFilePath)
    for strCategoryUrl in catUrlListFile:#category loop
        strCategoryName = r"" + re.search("^https://www.indiegogo.com/explore/(.*)$" ,strCategoryUrl).group(1)
        strCategoryFolderPath = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s"%(strCategoryName)
        if not os.path.exists(strCategoryFolderPath):
            os.mkdir(strCategoryFolderPath) #mkdir category
        openChrome()
        typeUrlOnChrome(urlText=strCategoryUrl)
        wait("1456214032899.png", 20)
        waitVanish("1456214096530.png", 20)
        wait("1456214122362.png", 20)
        #unfoldCategoryPage()
        saveCurrentPage(strFolderPath=strCategoryFolderPath, strFilename="category.html")
    catUrlListFile.close()
#download project pages
def downloadProjectPages(strTargetCategory=None):
    strProjUrlListFilePathTemplate = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\%s\project_url_list.txt"
    strProjectsFolderPathTemplate = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s\projects"   
    strProjectsFolderPath = strProjectsFolderPathTemplate % (strTargetCategory)
    if not os.path.exists(strProjectsFolderPath):
        os.mkdir(strProjectsFolderPath)#mkdir source_html/INDIEGOGO/Category/pojects
    strProjUrlListFilePath = strProjUrlListFilePathTemplate % (strTargetCategory)
    projUrlListFile = open(strProjUrlListFilePath, "r") 
    for strProjUrl in projUrlListFile:
        strProjName = re.search("^https://www.indiegogo.com/projects/(.*)/.{4}$", strProjUrl).group(1)
        openChrome()
        typeUrlOnChrome(urlText=strProjUrl)
        wait("1456229536809.png", 20)
        sleep(5)
        while(not exists("1456229579631.png")):
            type(Key.PAGE_DOWN)
            sleep(2)
        type(Key.DOWN)
        sleep(2)
        type(Key.DOWN)
        sleep(5)
        if(not exists("1456229579631.png")):
            type(Key.UP)
            sleep(2)
            type(Key.UP)
            sleep(5)
        click("1456229579631.png")
        wait("1456229635107.png", 20)
        #save story with more details
        strProjStoryFilename = strProjName+"_story.html"
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjStoryFilename)
        #close details
        click("1456232782492.png")
        wait("1456229579631.png", 20)
        type(Key.HOME)
        
        wait("1456229536809.png", 20)
        #save updates
        click("1456232941269.png")
        wait("1456232962072.png", 20)
        strProjUpdatesFilename = strProjName+"_updates.html"
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjUpdatesFilename)
        #save comments
        click("1456232986275.png")
        wait("1456233002434.png", 20)
        strProjCommentsFilename = strProjName+"_comments.html"
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjCommentsFilename)
        #save backers
        click("1456233023222.png")
        wait("1456233041235.png", 20)
        strProjBackersFilename = strProjName+"_backers.html"
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjBackersFilename)
    projUrlListFile.close()
#download individuals pages
def downloadIndividualsPages():
    pass
#main entry point
if __name__ == "__main__":
    lstStrArgs = sys.argv
    if lstStrArgs[1] == "explore":
        downloadExplorePages()
    if lstStrArgs[1] == "category":
        downloadCategoryPages()
    if lstStrArgs[1] == "project": 
        #lstStrArgs[2] is target category arg
        downloadProjectPages(strTargetCategory=lstStrArgs[2])
    if lstStrArgs[1] == "individuals": #need arg2
        downloadIndividualsPages()