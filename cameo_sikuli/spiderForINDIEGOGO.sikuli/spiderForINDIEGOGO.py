import os
import sys
import re
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
strBaseResFolderPath = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res"
#open chrome
def openChrome():
    type("d", KeyModifier.WIN)
    wait("1456281338394.png", 300)
    click("1456281338394.png")
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
# delete origin text
def delOriginText():
    type("a", KeyModifier.CTRL)
    sleep(1)
    type(Key.BACKSPACE)
    sleep(1)
# paste text by using clipboard
def pasteClipboardText(strText=None):
    toolkit = Toolkit.getDefaultToolkit()
    clipboard = toolkit.getSystemClipboard()
    clipboard.setContents(StringSelection(u""+strText), None)
    sleep(1)
    type("v", KeyModifier.CTRL)
    sleep(1)
#roll to page end
def rollToPageEnd():
    type(Key.END)
    wait("1456062534102.png", 300)
# open all project
def unfoldCategoryPage():
    rollToPageEnd()
    type(Key.PAGE_UP)
    wait("1456215300454.png", 300)
    while(exists("1456064164365.png")):
        click("1456064164365.png")
        waitVanish("1456215300454.png", 300)
        sleep(5)
        rollToPageEnd()
        type(Key.PAGE_UP)
        wait("1456215300454.png", 300)
#unfold (updates comments backers) showmore
def unfoldUCBShowmore():
    while(not exists("1456062534102.png")):
        type(Key.PAGE_DOWN)
        sleep(1)
        if exists("1456873668385.png"):
            click("1456873668385.png")
            waitVanish("1456873668385.png", 300)
            sleep(2)
    type(Key.HOME)
    wait("1456873739809.png", 300)
#type url on chrome
def typeUrlOnChrome(strUrlText=None):
    click("1455955040522.png")
    sleep(1)
    delOriginText()
    pasteClipboardText(strText=strUrlText)
    sleep(1)
    type(Key.ENTER)
# go to explore page
def goExplorePage():
    typeUrlOnChrome(strUrlText="https://www.indiegogo.com/explore")
    wait("1455771252801.png", 300)
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
#choose folder at save progress
def typeFolderPath(strFolderPath=None):
    wait(Pattern("1456054857857.png").targetOffset(10,0), 300)
    click(Pattern("1456054857857.png").targetOffset(10,0))
    sleep(1)
    delOriginText()
    pasteClipboardText(strText=strFolderPath)
    sleep(1)
    type(Key.ENTER)
    sleep(1)
#rightclick on image to save current page
def rightClickSaveCurrentPage(onImage=None, strFolderPath=None, strFilename=None):
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
    rightClick(onImage)
    wait("1456245315336.png", 300)
    click("1456245315336.png")
    wait("1455955227414.png", 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    click(Pattern("1455959876192.png").targetOffset(36,0))
    sleep(1)
    delOriginText()
    sleep(1)
    pasteClipboardText(strText=strFilename)
    sleep(1)
    click("1455955227414.png")
    sleep(1)
    wait("1456247446257.png", 300)#wait save complete
#ask chrome save current page
def saveCurrentPage(strFolderPath=None, strFilename="default.html"):
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
    type("s", KeyModifier.CTRL)
    wait("1455955227414.png", 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    click(Pattern("1455959876192.png").targetOffset(36,0))
    sleep(1)
    delOriginText()
    sleep(1)
    pasteClipboardText(strText=strFilename)
    sleep(1)
    click("1455955227414.png")
    sleep(1)
    wait("1456247446257.png", 300)#wait save complete
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
        typeUrlOnChrome(strUrlText=strCategoryUrl)
        waitVanish("1456214096530.png", 300)
        wait("1456214122362.png", 300)
        unfoldCategoryPage()
        saveCurrentPage(strFolderPath=strCategoryFolderPath, strFilename="category.html")
    catUrlListFile.close()
#download project pages
def downloadProjectPages(strTargetCategory=None):
    strProjUrlListFilePathTemplate = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\%s\project_url_list.txt"
    strProjectsFolderPathTemplate = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s\projects"   
    strProjectsFolderPath = strProjectsFolderPathTemplate % (strTargetCategory)
    if not os.path.exists(strProjectsFolderPath):
        os.mkdir(strProjectsFolderPath)#mkdir source_html/INDIEGOGO/Category/pojects/
    strProjUrlListFilePath = strProjUrlListFilePathTemplate % (strTargetCategory)
    projUrlListFile = open(strProjUrlListFilePath, "r") 
    for strProjUrl in projUrlListFile:
        strProjName = re.search("^https://www.indiegogo.com/projects/(.*)/.{4}$", strProjUrl).group(1)
        openChrome()
        typeUrlOnChrome(strUrlText=strProjUrl)
        wait("1456229536809.png", 300)
        sleep(5)
        strProjDetailsFilename = strProjName+"_details.html"
        strProjDetailsFilePath = strProjectsFolderPath + r"/" + strProjDetailsFilename
        if not os.path.exists(strProjDetailsFilePath):#check detail.html
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
            wait("1456229635107.png", 300)
            #save see more details
            rightClickSaveCurrentPage(onImage="1456229635107.png", strFolderPath=strProjectsFolderPath, strFilename=strProjDetailsFilename)
            #close details
            click("1456232782492.png")
            wait("1456229579631.png", 300)
            type(Key.HOME)       
            wait("1456229536809.png", 300)
        strProjStoryFilename = strProjName+"_story.html"
        strProjStroyFilePath = strProjectsFolderPath + r"/" + strProjStoryFilename
        if not os.path.exists(strProjStroyFilePath):#check story.html
            #save story
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjStoryFilename)
        strProjUpdatesFilename = strProjName+"_updates.html"
        strProjUpdatesFilePath = strProjectsFolderPath + r"/" + strProjUpdatesFilename        
        if not os.path.exists(strProjUpdatesFilePath):#check updates.html
            #save updates
            wait("1456232941269.png", 300)
            click("1456232941269.png")
            wait("1456232962072.png", 300)
            unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjUpdatesFilename)
        strProjCommentsFilename = strProjName+"_comments.html"
        strProjCommentsFilePath = strProjectsFolderPath + r"/" + strProjCommentsFilename                
        if not os.path.exists(strProjCommentsFilePath):#check comments.html
            #save comments
            wait("1456232986275.png", 300)
            click("1456232986275.png")
            wait("1456233002434.png", 300)
            unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjCommentsFilename)
        strProjBackersFilename = strProjName+"_backers.html"
        strProjBackersFilePath = strProjectsFolderPath + r"/" + strProjBackersFilename                        
        if not os.path.exists(strProjBackersFilePath):#check backers.html
            #save backers
            wait("1456233023222.png", 300)
            click("1456233023222.png")
            wait("1456233041235.png", 300)
            unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjBackersFilename)
        strProjGalleryFilename = strProjName+"_gallery.html"
        strProjGalleryFilePath = strProjectsFolderPath + r"/" + strProjGalleryFilename
        if (not os.path.exists(strProjGalleryFilePath)) and exists("1456828715470.png"):#check gallery.html
            #save gallery
            wait("1456828715470.png", 300)
            click("1456828715470.png")
            wait("1456828751430.png", 300)
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjGalleryFilename)
    projUrlListFile.close()
#download individuals pages
def downloadIndividualsPages(strTargetCategory=None):
    strIndividualsUrlListFilePathTemplate = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\%s\individuals_url_list.txt"
    strIndividualsFolderPathTemplate = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s\profiles"
    strIndividualsFolderPath = strIndividualsFolderPathTemplate % (strTargetCategory)
    if not os.path.exists(strIndividualsFolderPath):
        os.mkdir(strIndividualsFolderPath)#mkdir source_html/INDIEGOGO/Category/profiles/
    strIndividualsUrlListFilePath = strIndividualsUrlListFilePathTemplate % (strTargetCategory)
    individualsUrlListFile = open(strIndividualsUrlListFilePath, "r") 
    for strIndividualsUrl in individualsUrlListFile:
        strIndividualsId = re.search("^https://www.indiegogo.com/individuals/(.*)$", strIndividualsUrl).group(1)
        openChrome()
        typeUrlOnChrome(strUrlText=strIndividualsUrl)
        wait("1456297470021.png", 300)
        strIndividualsProfileFilename = strIndividualsId+"_profile.html"
        strIndividualsProfileFilePath = strIndividualsFolderPath + r"/" + strIndividualsProfileFilename
        if not os.path.exists(strIndividualsProfileFilePath):#check profile.html
            saveCurrentPage(strFolderPath=strIndividualsFolderPath, strFilename=strIndividualsProfileFilename)
        strIndividualsCampaignsFilename = strIndividualsId+"_campaigns.html"       
        strIndividualsCampaignsFilePath = strIndividualsFolderPath + r"/" + strIndividualsCampaignsFilename        
        if not os.path.exists(strIndividualsCampaignsFilePath):#check campaigns.html        
            wait("1456297490082.png", 300)
            click("1456297490082.png")
            wait("1456297519988.png", 300)        
            saveCurrentPage(strFolderPath=strIndividualsFolderPath, strFilename=strIndividualsCampaignsFilename)
    individualsUrlListFile.close()
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
    if lstStrArgs[1] == "individuals":
        #lstStrArgs[2] is target category arg
        downloadIndividualsPages(strTargetCategory=lstStrArgs[2])