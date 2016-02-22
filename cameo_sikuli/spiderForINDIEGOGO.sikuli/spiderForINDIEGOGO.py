import os
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
    sleep(2)
    wait("1456062534102.png", 20)
# open all project
def unfoldCategoryPage():
    rollToPageEnd()
    type(Key.PAGE_UP)
    sleep(2)
    while(exists("1456064164365.png")):
        click("1456064164365.png")
        sleep(2)
        rollToPageEnd()
        type(Key.PAGE_UP)
        sleep(2)
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
#download category pages
def downloadCategoryPages():
    openChrome()
    goExplorePage()
    lstCategory = ["1456056808652.png", "1456056829765.png", "1456056869120.png", "1456056881941.png", "1456056899968.png", "1456056915334.png",
                   "1456056944840.png", "1456056959389.png", "1456056975659.png", "1456057003039.png", "1456057017893.png",
                   "1456057041383.png", "1456057054505.png", "1456057067400.png", "1456057080829.png", "1456057092683.png",
                   "1456057109594.png", "1456057129967.png", "1456057146233.png", "1456057158719.png", "1456057181012.png",
                   "1456057197956.png", "1456057210885.png", "1456057240923.png"]
    intCatId = 0
    #category loop    
    for cat in lstCategory:
        while(not exists(cat)):
            click("1455955269605.png")
            sleep(2)
            type(Key.PAGE_DOWN)
            sleep(5)
        click(cat)
        wait("1456057987950.png", 20)
        wait("1456064495796.png", 20)
        unfoldCategoryPage()
        sleep(2)
        strFolder = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res\source_html\INDIEGOGO"
        strFilename = str(intCatId) + ".html"
        saveCurrentPage(strFolderPath=strFolder, strFilename=strFilename)
        goExplorePage()
        sleep(2)
        intCatId = intCatId+1
#download project pages
def downloadProjectPages():
    lstCategoryName = ["Community", "Dance"]
    strBaseResFolderPath = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res" 
    strUrlListFilePathTemplate = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\%s\%s_proj_url_list.txt"
    strCategoryPathTemplate = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s"
    openChrome()
    goExplorePage()
    for strCategoryName in lstCategoryName:
        #mkdir
        strCategoryPath = strCategoryPathTemplate % (strCategoryName)
        if not os.path.exists(strCategoryPath):
            os.mkdir(strCategoryPath)
        strUrlListFilePath = strUrlListFilePathTemplate % (strCategoryName, strCategoryName)
        urlListFile = open(strUrlListFilePath, "r")
        intProjId = 0
        for strUrlLine in urlListFile:
            #continue point 
            if(intProjId < 391):
                intProjId = intProjId+1 #skip
                continue
            typeUrlOnChrome(urlText=strUrlLine)
            wait("1455944265378.png", 20)
            click("1455955269605.png")
            sleep(2)
            while(not exists("1455892865719.png")):
                type(Key.PAGE_DOWN)
                sleep(2)
            type(Key.DOWN)
            sleep(2)
            type(Key.DOWN)
            sleep(5)
            if(not exists("1455892865719.png")):
                type(Key.UP)
                sleep(2)
                type(Key.UP)
                sleep(5)
            click("1455892865719.png")
            wait("1455973105407.png", 20)
            saveCurrentPage(strFolderPath=strCategoryPath, strFilename=str(intProjId) + ".html")
            intProjId = intProjId+1
        urlListFile.close()
#main entry point
if __name__ == "__main__":
    #downloadCategoryPages()
    downloadProjectPages()
    
        