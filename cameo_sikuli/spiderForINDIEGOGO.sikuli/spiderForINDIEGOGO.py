#open chrome
def openChrome():
    type("d", KeyModifier.WIN)
    click("1455787318229.png")
    waitVanish("1455810570110.png", 10)
# delete origin text
def delOriginText():
    type("a", KeyModifier.CTRL);
    sleep(2)
    type(Key.BACKSPACE);
    sleep(2)
# open all project
def openAllProj():
    type(Key.END)
    type(Key.PAGE_UP)
    sleep(2)
    while(exists("1455785847618.png")): 
        click("1455785847618.png")
        sleep(5)
        type(Key.END)
        type(Key.PAGE_UP)
        sleep(2)
#type url on chrome
def typeUrlOnChrome(urlText=""):
    click("1455787143836.png")
    sleep(2)
    delOriginText()
    type(urlText)
    sleep(2)
    type(Key.ENTER)
# go to explore page
def goExplorePage():
    typeUrlOnChrome(urlText="https://www.indiegogo.com/explore")
    wait("1455771252801.png", 10)
    wait("1455773806049.png", 10)
#ask chrome save current page
def saveCurrentPage(filename="default.html"):
    type("s", KeyModifier.CTRL)    
    sleep(2)
    click(Pattern("1455856522474.png").targetOffset(47,0))
    sleep(2)
    delOriginText()
    sleep(2)
    type(filename)
    sleep(2)
    click("1455856561966.png")
    sleep(2)
#download category pages
def downloadCategoryPages():
    openChrome()
    goExplorePage()
    catDict = {"catList.png":"1455782552937.png",
               "1455773410389.png":"1455802574909.png",
               "1455773420042.png":"1455802697089.png",
               "1455773426115.png":"1455802726335.png",
               "1455773432582.png":"1455802759583.png",
               "1455773966059.png":"1455802933624.png",
               "1455773974586.png":"1455802961069.png",
               "1455773984147.png":"1455802992745.png",
               "1455773992388.png":"1455803028529.png",
               "1455773998962.png":"1455803059783.png",
               "1455774017612.png":"1455803088086.png",
               "1455774023732.png":"1455803115881.png",
               "1455774030264.png":"1455803143027.png",
               "1455774035660.png":"1455803611481.png",
               "1455774049342.png":"1455803655661.png",
               "1455774082464.png":"1455803693339.png",
               "1455774088058.png":"1455803720282.png",
               "1455774094195.png":"1455803782308.png",
               "1455774098534.png":"1455803804366.png",
               "1455774104142.png":"1455803830635.png",
               "1455774118219.png":"1455803858214.png",
               "1455774122818.png":"1455803877565.png",
               "1455774127133.png":"1455803897878.png",
               "1455774131360.png":"1455803925305.png"}
    catId = 0
    #category loop    
    for catK in catDict:
        click(catK)
        wait("1455773609785.png", 10)
        #openAllProj()
        sleep(2)
        filename = str(catId) + ".html"
        saveCurrentPage(filename)
        goExplorePage()
        sleep(2)
        catId = catId+1
#download project pages
def downloadProjectPages():
    #urlListFilePathList = ["E:\INDIEGOGO\Art\proj_url_list.txt"]
    urlListFilePathList = ["C:\Users\Administrator\Desktop\pyWorkspace\INDIEGOGO\Art\proj_url_list.txt"]
    openChrome()
    goExplorePage()
    for urlListFilePath in urlListFilePathList:
        urlListFile = open(urlListFilePath, "r")
        projId = 0
        for urlLine in urlListFile:
            if(projId < 245):
                projId = projId+1
                continue
            typeUrlOnChrome(urlText=urlLine)
            wait("1455944265378.png", 20)
            click("1455943547435.png")
            sleep(2)
            while(not exists("1455892865719.png")):
                type(Key.PAGE_DOWN)
                sleep(2)
            type(Key.DOWN)
            sleep(2)
            type(Key.DOWN)
            sleep(2)
            if(not exists("1455892865719.png")):
                type(Key.UP)
                sleep(2)
                type(Key.UP)
                sleep(2)
            click("1455892865719.png")
            wait("1455893048429.png", 10)
            saveCurrentPage(str(projId) + ".html")
            projId = projId+1
        urlListFile.close()
#main entry point
if __name__ == "__main__":
    #downloadCategoryPages()
    downloadProjectPages()