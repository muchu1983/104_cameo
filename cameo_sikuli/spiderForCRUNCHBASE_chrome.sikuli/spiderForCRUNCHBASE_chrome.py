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
dicPng = {
    "chrome_home":"chrome_home.png",
    "chrome_stop": "chrome_stop.png",
    "chrome_reload":"chrome_reload.png",
    "chrome_download_finished":"chrome_download_finished.png",
    "page_your_interruption":"page_your_interruption.png",
    "page_proxy_error":"page_proxy_error.png",
    "os_right_save_as":"os_right_save_as.png",
    "os_save_btn":"os_save_btn.png",
    "page_search":"page_search.png",
    "page_filter_btn":"page_filter_btn.png",
        
}
lstStrCategoryName = [
    "animals", "art", "comic", "community", "dance",
    "design", "education", "environment", "fashion",
    "film", "food", "gaming", "health", "music", "photography",
    "politics", "religion", "small_business", "sports",
    "technology", "theatre", "transmedia", "video_web", "writing"
]
sysClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
strBaseResFolderPath = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res"
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
    dicRegion["regNW"].waitVanish(dicPng["chrome_stop"], 10)
    dicRegion["regNW"].wait(dicPng["chrome_reload"], 300)
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
#roll to page end
def rollToPageEnd():
    type(Key.END)
    dicRegion["regLeft"].wait(dicPng["page_end_about"], 300)
#type url on chrome
def typeUrlOnChrome(strUrlText=None):
    type("l", Key.CTRL)
    wait(0.5)
    delOriginText()
    pasteClipboardText(strText=strUrlText)
    wait(0.5)
    type(Key.ENTER)
    wait(0.5)
    dicRegion["regNW"].waitVanish(dicPng["chrome_stop"], 30)
    dicRegion["regNW"].wait(dicPng["chrome_reload"], 300)
    wait(5)
    #recheck for server may redirect to home page
    dicRegion["regNW"].waitVanish(dicPng["chrome_stop"], 30)
    dicRegion["regNW"].wait(dicPng["chrome_reload"], 300)
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
    dicRegion["regNW"].waitVanish(dicPng["chrome_stop"], 30)
    dicRegion["regNW"].wait(dicPng["chrome_reload"], 300)
    checkAndPauseBeforeSave()
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
    dicRegion["regNW"].waitVanish(dicPng["chrome_stop"], 30)
    dicRegion["regNW"].wait(dicPng["chrome_reload"], 300)
    checkAndPauseBeforeSave()
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
def goSearchPage():
    openChrome()
    typeUrlOnChrome(strUrlText="https://www.crunchbase.com/app/search/companies")
    dicRegion["regUp"].wait(dicPng["page_search"], 300)
    dicRegion["regNW"].waitVanish(dicPng["chrome_stop"], 30)
    dicRegion["regNW"].wait(dicPng["chrome_reload"], 300)
#download explore pages
def downloadSearchPages():
    goSearchPage()
    dicRegion["regNW"].click(dicPng["page_filter_btn"])
    strSearchFolderPath = strBaseResFolderPath + r"\source_html\CRUNCHBASE"
    if not os.path.exists(strSearchFolderPath):
        os.mkdir(strSearchFolderPath)
    saveCurrentPage(strFolderPath=strSearchFolderPath, strFilename="search.html")
#main entry point
if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        downloadSearchPages()
        popup(u"spider action completed. ^.^y")
    except FindFailed, ff:
        print(str(ff))
        popup(u"spider cant find png error! timestamp: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception, ex:
        print(str(ex))
        popup(u"spider unknow error! timestamp: %s"%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    finally:
        exit()