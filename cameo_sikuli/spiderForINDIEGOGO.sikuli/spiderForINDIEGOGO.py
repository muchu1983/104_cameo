import os
import sys
import re
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
sysClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
strBaseResFolderPath = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res"
#open chrome
def openChrome():
    type("d", KeyModifier.WIN)
    wait("localpng_chrome_logo.png", 300)
    click("localpng_chrome_logo.png")
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
# delete origin text
def delOriginText():
    type("a", KeyModifier.CTRL)
    wait(0.5)
    type(Key.BACKSPACE)
    wait(0.5)
# paste text by using clipboard
def pasteClipboardText(strText=None):
    sysClipboard.setContents(StringSelection(u""+strText), None)
    wait(0.5)
    type("v", KeyModifier.CTRL)
    wait(0.5)
#roll to page end
def rollToPageEnd():
    type(Key.END)
    wait("1456062534102.png", 300)
# open all project
def unfoldCategoryPage():
    rollToPageEnd()
    for uptime in range(6):
        type(Key.UP)
    wait("1456215300454.png", 300)
    while(exists("1457250780994.png")):
        click("1457250780994.png")
        waitVanish("1456215300454.png", 300)
        wait(5)
        rollToPageEnd()
        for uptime in range(6):
            type(Key.UP)
            wait(0.5)
        wait("1456215300454.png", 300)
#unfold (updates comments backers) showmore
def unfoldUCBShowmore():
    while(not exists("1456062534102.png")):
        type(Key.PAGE_DOWN)
        wait(0.5)
        if exists("1457668772685.png"):
            click("1457668772685.png")
            waitVanish("1457668772685.png", 300)
            wait(2)
    type(Key.HOME)
    wait("1456873739809.png", 300)
#type url on chrome
def typeUrlOnChrome(strUrlText=None):
    click("localpng_url_text_bar.png")
    wait(0.5)
    delOriginText()
    pasteClipboardText(strText=strUrlText)
    wait(0.5)
    type(Key.ENTER)
    wait(0.5)
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
# go to explore page
def goExplorePage():
    typeUrlOnChrome(strUrlText="https://www.indiegogo.com/explore")
    wait("1455771252801.png", 300)
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
#choose folder at save progress
def typeFolderPath(strFolderPath=None):
    wait(Pattern("localpng_foldername_input_bar.png").targetOffset(10,0), 300)
    click(Pattern("localpng_foldername_input_bar.png").targetOffset(10,0))
    wait(0.5)
    delOriginText()
    pasteClipboardText(strText=strFolderPath)
    wait(0.5)
    type(Key.ENTER)
    wait(0.5)
#rightclick on image to save current page
def rightClickSaveCurrentPage(onImage=None, strFolderPath=None, strFilename=None):
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
    rightClick(onImage)
    wait("localpng_right_click_save_as.png", 300)
    click("localpng_right_click_save_as.png")
    wait("localpng_save_btn.png", 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    click(Pattern("localpng_filename_input_bar.png").targetOffset(36,0))
    wait(0.5)
    delOriginText()
    wait(0.5)
    pasteClipboardText(strText=strFilename)
    wait(0.5)
    click("localpng_save_btn.png")
    wait(0.5)
    wait("1457673648130.png", 300)#wait save complete
#ask chrome save current page
def saveCurrentPage(strFolderPath=None, strFilename="default.html"):
    waitVanish("1456214096530.png", 300)
    wait("1456214122362.png", 300)
    type("s", KeyModifier.CTRL)
    wait("localpng_save_btn.png", 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    click(Pattern("localpng_filename_input_bar.png").targetOffset(36,0))
    wait(0.5)
    delOriginText()
    wait(0.5)
    pasteClipboardText(strText=strFilename)
    wait(0.5)
    click("localpng_save_btn.png")
    wait(0.5)
    wait("1457673648130.png", 300)#wait save complete
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
        strCategoryFilePath = strCategoryFolderPath + r"\category.html"
        if not os.path.exists(strCategoryFilePath):#check category.html
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
        #check html file exists
        isProjHtmlFileMissing = False
        strProjDetailsFilename = strProjName+"_details.html"
        strProjDetailsFilePath = strProjectsFolderPath + "\\" + strProjDetailsFilename
        if not os.path.exists(strProjDetailsFilePath):#check detail.html
            isProjHtmlFileMissing = True
        strProjStoryFilename = strProjName+"_story.html"
        strProjStroyFilePath = strProjectsFolderPath + "\\" + strProjStoryFilename
        if not os.path.exists(strProjStroyFilePath):#check story.html
            isProjHtmlFileMissing = True
        strProjUpdatesFilename = strProjName+"_updates.html"
        strProjUpdatesFilePath = strProjectsFolderPath + "\\" + strProjUpdatesFilename        
        if not os.path.exists(strProjUpdatesFilePath):#check updates.html
            isProjHtmlFileMissing = True
        strProjCommentsFilename = strProjName+"_comments.html"
        strProjCommentsFilePath = strProjectsFolderPath + "\\" + strProjCommentsFilename                
        if not os.path.exists(strProjCommentsFilePath):#check comments.html
            isProjHtmlFileMissing = True
        strProjBackersFilename = strProjName+"_backers.html"
        strProjBackersFilePath = strProjectsFolderPath + "\\" + strProjBackersFilename                        
        if not os.path.exists(strProjBackersFilePath):#check backers.html
            isProjHtmlFileMissing = True
        #open chrome 
        if isProjHtmlFileMissing:
            openChrome()
            typeUrlOnChrome(strUrlText=strProjUrl)
            wait("1456229536809.png", 300)
            wait(0.5)
        else:
            continue #skip this url
        if not os.path.exists(strProjDetailsFilePath):#check detail.html
            while(not exists("1456229579631.png")):
                type(Key.PAGE_DOWN)
                wait(0.5)
            click("1456229579631.png")
            wait("1456229635107.png", 300)
            #save see more details
            rightClickSaveCurrentPage(onImage="1456229635107.png", strFolderPath=strProjectsFolderPath, strFilename=strProjDetailsFilename)
            #close details
            click("1456232782492.png")
            wait("1456229579631.png", 300)
            type(Key.HOME)       
            wait("1456229536809.png", 300)
        if not os.path.exists(strProjStroyFilePath):#check story.html
            #save story
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjStoryFilename)
        if not os.path.exists(strProjUpdatesFilePath):#check updates.html
            #save updates
            wait("1456232941269.png", 300)
            click("1456232941269.png")
            wait("1456232962072.png", 300)
            unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjUpdatesFilename)
        if not os.path.exists(strProjCommentsFilePath):#check comments.html
            #save comments
            wait("1456232986275.png", 300)
            click("1456232986275.png")
            wait("1456233002434.png", 300)
            unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjCommentsFilename)
        if not os.path.exists(strProjBackersFilePath):#check backers.html
            #save backers
            wait("1456233023222.png", 300)
            click("1456233023222.png")
            wait("1457063099388.png", 300)
            unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjBackersFilename)
        #gallery may not exists
        strProjGalleryFilename = strProjName+"_gallery.html"
        strProjGalleryFilePath = strProjectsFolderPath + "\\" + strProjGalleryFilename            
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
        #check html exists
        isIndividualsHtmlFileMissing = False
        strIndividualsProfileFilename = strIndividualsId+"_profile.html"
        strIndividualsProfileFilePath = strIndividualsFolderPath + "\\" + strIndividualsProfileFilename
        if not os.path.exists(strIndividualsProfileFilePath):#check profile.html
            isIndividualsHtmlFileMissing = True
        strIndividualsCampaignsFilename = strIndividualsId+"_campaigns.html"       
        strIndividualsCampaignsFilePath = strIndividualsFolderPath + "\\" + strIndividualsCampaignsFilename        
        if not os.path.exists(strIndividualsCampaignsFilePath):#check campaigns.html  
            isIndividualsHtmlFileMissing = True
        #open chrome
        if isIndividualsHtmlFileMissing:
            openChrome()
            typeUrlOnChrome(strUrlText=strIndividualsUrl)
            wait("1456297470021.png", 300)
        if not os.path.exists(strIndividualsProfileFilePath):#check profile.html
            saveCurrentPage(strFolderPath=strIndividualsFolderPath, strFilename=strIndividualsProfileFilename)
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
    popup(u"spider action completed")