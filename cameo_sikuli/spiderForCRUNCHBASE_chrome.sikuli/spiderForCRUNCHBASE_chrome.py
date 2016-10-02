# -*- coding: utf-8 -*-
"""
Copyright (C) 2016, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import sys
import re
import logging
import datetime
import random
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
sys.path.append("cameo_sikuli\\jyson-1.0.2.jar")
from com.xhaus.jyson import JysonCodec as jyson

screen = Screen()
dicRegion = {
    "regUp":Region(0,0,screen.getW(),screen.getH()/2),
    "regDown":Region(0,screen.getH()/2,screen.getW(),screen.getH()/2),
    "regLeft":Region(0,0,screen.getW()/2,screen.getH()),
    "regRight":Region(screen.getW()/2,0,screen.getW()/2,screen.getH()),
    "regNE":Region(screen.getW()/2,0,screen.getW()/2,screen.getH()/2),
    "regSE":Region(screen.getW()/2,screen.getH()/2,screen.getW()/2,screen.getH()/2),
    "regSW":Region(0,screen.getH()/2,screen.getW()/2,screen.getH()/2),
    "regNW":Region(0,0,screen.getW()/2,screen.getH()/2),
    "regCenter":Region(screen.getW()/4,screen.getH()/4,screen.getW()/2,screen.getH()/2)
}

dicDevelPng = {
    "chrome_home":"chrome_home.png",
    "chrome_stop":"chrome_stop.png",
    "chrome_reload":"chrome_reload.png",
    "chrome_download_finished":"chrome_download_finished.png",
    "page_your_interruption":"page_your_interruption.png",
    "page_proxy_error":"page_proxy_error.png",
    "os_right_save_as":"os_right_save_as.png",
    "os_save_btn":"os_save_btn.png",
    "page_search_btn":"page_search_btn.png",
    "page_filter_btn":"page_filter_btn.png",
    "page_filter_funded_company_btn":"page_filter_funded_company_btn.png",
    "page_filter_funded_companies_btn":"page_filter_funded_companies_btn.png",
    "page_filter_funded_categories_btn":"page_filter_funded_categories_btn.png",
    "page_filter_funded_categories_2_btn":"page_filter_funded_categories_2_btn.png",
    "page_category_target_btn":Pattern("page_category_target_btn.png").targetOffset(-100,40), #Pattern targetOffset(-100,40)
    "page_query_input":Pattern("page_query_input.png").targetOffset(-100,0), #Pattern targetOffset(-100,0)
    "page_sidebar_end":Pattern("page_sidebar_end.png").similar(0.80)
}

dicRunningPng = { #running_XXX.png
    "chrome_home":"running_chrome_home.png", #ex: running_chrome_home.png
    "chrome_stop":"running_chrome_stop.png",
    "chrome_reload":"running_chrome_reload.png",
    "chrome_download_finished":"running_chrome_download_finished.png",
    "page_your_interruption":"running_page_your_interruption.png",
    "page_proxy_error":"running_page_proxy_error.png",
    "os_right_save_as":"running_os_right_save_as.png",
    "os_save_btn":"running_os_save_btn.png",
    "page_search_btn":"running_page_search_btn.png",
    "page_filter_btn":"running_page_filter_btn.png",
    "page_filter_funded_company_btn":"running_page_filter_funded_company_btn.png",
    "page_filter_funded_companies_btn":"running_page_filter_funded_companies_btn.png",
    "page_filter_funded_categories_btn":"running_page_filter_funded_categories_btn.png",
    "page_filter_funded_categories_2_btn":"running_page_filter_funded_categories_2_btn.png",
    "page_category_target_btn":Pattern("running_page_category_target_btn.png").targetOffset(-100,40), #Pattern targetOffset(-100,40)
    "page_query_input":Pattern("running_page_query_input.png").targetOffset(-100,0), #Pattern targetOffset(-100,0)
    "page_sidebar_end":Pattern("running_page_sidebar_end.png").similar(0.80)
}

#dicPng = dicDevelPng
dicPng = dicRunningPng
sysClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
#strBaseResFolderPath = u"C:\\Users\\muchu\\Desktop\\caseWorkspace\\003-卡米爾scrapy\\CAMEO_git_code\\cameo_res"
strBaseResFolderPath = u"C:\\Users\\Administrator\\Desktop\\pyWorkspace\\CAMEO_git_code\\cameo_res"
#open chrome
def openChrome():
    #close prev chrome
    if dicRegion["regNW"].exists(dicPng["chrome_home"]):
        type("w", Key.CTRL)
    wait(5)
    #re-open new chrome
    App.open("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    wait(5)#wait to running
    dicRegion["regNW"].wait(dicPng["chrome_home"], 300)
    dicRegion["regNW"].click(dicPng["chrome_home"])
    waitChromeLoadingFinished()

#wait chrome loading finished
def waitChromeLoadingFinished():
    wait(3)
    while dicRegion["regNW"].exists(dicPng["chrome_stop"], 2):
        logging.info(str(dicRegion["regNW"].exists(dicPng["chrome_stop"], 2)))
        logging.info("wait chrome loading...")
        wait(1)
    dicRegion["regNW"].wait(dicPng["chrome_reload"], 300)
    logging.info("chrome loading finished.")

# delete origin text
def delOriginText():
    type("a", Key.CTRL)
    wait(0.5)
    type(Key.BACKSPACE)
    wait(0.5)

# paste text by using clipboard
def pasteClipboardText(strText=None):
    sysClipboard.setContents(StringSelection(u""+strText), None)
    wait(0.5)
    type("v", Key.CTRL)
    wait(0.5)

#type url on chrome
def typeUrlOnChrome(strUrlText=None):
    type("l", Key.CTRL)
    wait(0.5)
    delOriginText()
    pasteClipboardText(strText=strUrlText)
    wait(0.5)
    type(Key.ENTER)
    wait(0.5)
    waitChromeLoadingFinished()
    wait(5)
    #recheck for server may redirect to home page
    waitChromeLoadingFinished()
    wait(0.5)

#choose folder at save progress
def typeFolderPath(strFolderPath=None):
    wait(0.5)
    type(Key.TAB)
    wait(0.5)
    type("d", Key.ALT)
    wait(0.5)
    delOriginText()
    pasteClipboardText(strText=strFolderPath)
    wait(0.5)
    type(Key.ENTER)
    wait(0.5)

# type in filename at save progress
def typeFilename(strFilename=None):
    wait(0.5)
    type(Key.TAB)
    wait(0.5)
    type("n", Key.ALT)
    wait(0.5)
    delOriginText()
    wait(0.5)
    pasteClipboardText(strText=strFilename)
    wait(0.5)

#rightclick on image to save current page
def rightClickSaveCurrentPage(onImage=None, strFolderPath=None, strFilename=None):
    logging.info("prepare to save " + strFilename)
    wait(10)
    waitChromeLoadingFinished()
    rightClick(onImage)
    dicRegion["regCenter"].wait(dicPng["os_right_save_as"], 300)
    dicRegion["regCenter"].click(dicPng["os_right_save_as"])
    dicRegion["regDown"].wait(dicPng["os_save_btn"], 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    wait(0.5)
    typeFilename(strFilename=strFilename)
    wait(0.5)
    type("s", Key.ALT)
    wait(0.5)
    hover(Location(100, 620))
    logging.info("save timestamp: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dicRegion["regSW"].wait(dicPng["chrome_download_finished"], 300)#wait save complete

#ask chrome save current page
def saveCurrentPage(strFolderPath=None, strFilename=None):
    logging.info("prepare to save " + strFilename)
    wait(10)
    waitChromeLoadingFinished()
    type("s", Key.CTRL)
    dicRegion["regDown"].wait(dicPng["os_save_btn"], 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    wait(0.5)
    typeFilename(strFilename=strFilename)
    wait(0.5)
    type("s", Key.ALT)
    wait(0.5)
    hover(Location(100, 620))
    logging.info("save timestamp: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dicRegion["regSW"].wait(dicPng["chrome_download_finished"], 300)#wait save complete

#fake random request confuse browser fingerpring algorithm
def fakeRandomRequest():
    wait(0.5)
    lstStrFakeReqUrl = [
        "https://translate.google.com.tw/",
        "http://24h.pchome.com.tw/",
        "https://tw.news.yahoo.com/",
        "https://trello.com/",
        "https://www.whatismyip.com/",
        "https://www.twitch.tv/hichocolate",
        "https://www.youtube.com/",
        "https://build.phonegap.com/",
        "https://tw.money.yahoo.com/currency"
    ]
    for intFakeTimes in range(random.randint(1,2)):
        strFakeUrl = lstStrFakeReqUrl[random.randint(0,len(lstStrFakeReqUrl)-1)]
        openChrome()
        typeUrlOnChrome(strUrlText=strFakeUrl)
        wait(5)
    wait(0.5)

# go to search page
def goSearchFundingRoundsPage():
    openChrome()
    typeUrlOnChrome(strUrlText="https://www.crunchbase.com/app/search/funding_rounds")
    dicRegion["regUp"].wait(dicPng["page_search_btn"], 300)
    waitChromeLoadingFinished()

#download explore pages
def downloadSearchFundingRoundsPage(strCategoryText=None):
    if strCategoryText == None: #no specify category
        #read category_list.json 
        strCategoryListFilePath = strBaseResFolderPath + u"\\parsed_result\\CRUNCHBASE\\category_list.json"
        jsonFile = open(strCategoryListFilePath, "r")
        dicCategoryList = jyson.loads(jsonFile.read(), encoding="utf-8")
        jsonFile.close()
        intMinRange = dicCategoryList.get("intMinRange", 1)
        intMaxRange = dicCategoryList.get("intMaxRange", 121)
        for intCategoryId in range(intMinRange, intMaxRange+1): #category loop
            strTargetCategoryText = dicCategoryList.get(str(intCategoryId), None)
            if strTargetCategoryText is not None:
                downloadSearchFundingRoundsPage(strCategoryText=strTargetCategoryText)
    else: #specify category
        logging.info("download category :%s"%strCategoryText)
        goSearchFundingRoundsPage()
        dicRegion["regUp"].click(dicPng["page_filter_btn"])
        wait(5)
        dicRegion["regUp"].click(dicPng["page_filter_funded_company_btn"])
        wait(5)
        dicRegion["regUp"].click(dicPng["page_filter_funded_companies_btn"])
        wait(5)
        dicRegion["regUp"].click(dicPng["page_filter_funded_categories_btn"])
        wait(5)
        dicRegion["regUp"].click(dicPng["page_filter_funded_categories_2_btn"])
        wait(5)
        dicRegion["regNE"].click(dicPng["page_query_input"])
        wait(5)
        pasteClipboardText(strText=strCategoryText)
        wait(5)
        dicRegion["regNE"].click(dicPng["page_category_target_btn"])
        wait(5)
        dicRegion["regLeft"].click(dicPng["page_search_btn"])
        wait(5)
        #create CRUNCHBASE folder
        strSearchFolderPath = strBaseResFolderPath + u"\\source_html\\CRUNCHBASE"
        if not os.path.exists(strSearchFolderPath):
            try:
                os.mkdir(strSearchFolderPath)
            except:
                logging.warning("folder already exists: %s"%strSearchFolderPath)
        intFundingRoundsPage = 1
        while dicRegion["regLeft"].exists(dicPng["page_search_btn"]) is not None:
            saveCurrentPage(strFolderPath=strSearchFolderPath, strFilename="%s_%d_funding_rounds.html"%(strCategoryText, intFundingRoundsPage))
            intFundingRoundsPage = intFundingRoundsPage+1
            hover(Location(screen.getW()/2, screen.getH()-100))
            wheel(Location(screen.getW()/2, screen.getH()-100), WHEEL_DOWN, 1)
            wait(1)
        else:
            saveCurrentPage(strFolderPath=strSearchFolderPath, strFilename="%s_%d_funding_rounds.html"%(strCategoryText, intFundingRoundsPage))
            type("w", Key.CTRL)

#download organization pages
def downloadOrganizationPage():
    #create organization folder
    strOrganizationFolderPath = strBaseResFolderPath + u"\\source_html\\CRUNCHBASE\\organization"
    if not os.path.exists(strOrganizationFolderPath):
        try:
            os.mkdir(strOrganizationFolderPath)
        except:
            logging.warning("folder already exists: %s"%strOrganizationFolderPath)
    #read organization_url_list.json
    strOrganizationUrlListFilePath = strBaseResFolderPath + u"\\parsed_result\\CRUNCHBASE\\organization\\organization_url_list.json"
    dicLstOrganizationUrl = None
    jsonFile = open(strOrganizationUrlListFilePath, "r")
    dicLstOrganizationUrl = jyson.loads(jsonFile.read(), encoding="utf-8")
    jsonFile.close()
    lstStrOrganizationUrl = dicLstOrganizationUrl.get("organization_url_list", [])
    for strOrganizationUrl in lstStrOrganizationUrl:#organization loop
        logging.info(u"download organization: %s"%strOrganizationUrl)
        openChrome()
        typeUrlOnChrome(strUrlText=strOrganizationUrl)
        strOrganizationName = re.match(u"^https://www.crunchbase.com/organization/(.*)$", strOrganizationUrl).group(1).strip()
        saveCurrentPage(strFolderPath=strOrganizationFolderPath, strFilename=u"%s_organization.html"%strOrganizationName)
        wait(5)
    else:
        type("w", Key.CTRL)

#main entry point
if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        lstStrArgs = sys.argv
        if lstStrArgs[1] == "search_funding_rounds":
            if len(lstStrArgs) == 3:
                #lstStrArgs[2] is target category arg
                downloadSearchFundingRoundsPage(strCategoryText=lstStrArgs[2])
            else:
                downloadSearchFundingRoundsPage(strCategoryText=None)
        elif lstStrArgs[1] == "organization":
            downloadOrganizationPage()
        logging.info(u"spider action completed. ^.^y timestamp: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except FindFailed, ff:
        print(str(ff))
        popup(u"spider cant find png error! timestamp: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception, ex:
        print(str(ex))
        popup(u"spider unknow error! timestamp: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    finally:
        exit()