# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from selenium import webdriver
import os
import time
import logging
import re
import random
from cameo.utility import Utility
from cameo.localdb import LocalDbForTECHORANGE
"""
抓取 科技報橘 html 存放到 source_html 
"""
class SpiderForTECHORANGE:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.strWebsiteDomain = u"http://buzzorange.com/techorange"
        self.dicSubCommandHandler = {
            "index":self.downloadIndexPage,
            "tag":self.downloadTagPag,
            "news":self.downloadNewsPage
        }
        self.utility = Utility()
        self.db = LocalDbForTECHORANGE()
        self.driver = None
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return ("- TECHORANGE -\n"
                "useage:\n"
                "index - download entry page of TECHORANGE \n"
                "tag - download not obtained tag page \n"
                "news [tag] - download not obtained news [of given tag] \n")
    
    #取得 selenium driver 物件
    def getDriver(self):
        chromeDriverExeFilePath = "cameo_res\\chromedriver.exe"
        driver = webdriver.Chrome(chromeDriverExeFilePath)
        return driver
        
    #初始化 selenium driver 物件
    def initDriver(self):
        if self.driver is None:
            self.driver = self.getDriver()
        
    #終止 selenium driver 物件
    def quitDriver(self):
        self.driver.quit()
        self.driver = None
        
    #執行 spider
    def runSpider(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        self.initDriver() #init selenium driver
        self.dicSubCommandHandler[strSubcommand](strArg1)
        self.quitDriver() #quit selenium driver
        
    #下載 index 頁面
    def downloadIndexPage(self, uselessArg1=None):
        logging.info("download index page")
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE"
        if not os.path.exists(strIndexHtmlFolderPath):
            os.mkdir(strIndexHtmlFolderPath) #mkdir source_html/TECHORANGE/
        #科技報橘首頁
        self.driver.get("https://buzzorange.com/techorange/")
        #儲存 html
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        self.utility.overwriteSaveAs(strFilePath=strIndexHtmlFilePath, unicodeData=self.driver.page_source)
        
    #下載 tag 頁面
    def downloadTagPag(self, uselessArg1=None):
        logging.info("download tag page")
        strTagHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE\\tag"
        if not os.path.exists(strTagHtmlFolderPath):
            os.mkdir(strTagHtmlFolderPath) #mkdir source_html/TECHORANGE/tag/
        strTagWebsiteDomain = self.strWebsiteDomain + u"/tag"
        #取得 Db 中尚未下載的 Tag 名稱
        lstStrNotObtainedTagName = self.db.fetchallNotObtainedTagName()
        for strNotObtainedTagName in lstStrNotObtainedTagName:
            #略過名稱太長的 tag
            if len(strNotObtainedTagName) > 60:
                continue
            strTagUrl = strTagWebsiteDomain + u"/" + strNotObtainedTagName
            #tag 第0頁
            intPageNum = 0
            time.sleep(random.randint(2,5)) #sleep random time
            self.driver.get(strTagUrl)
            #儲存 html
            strTagHtmlFilePath = strTagHtmlFolderPath + u"\\%d_%s_tag.html"%(intPageNum, strNotObtainedTagName)
            self.utility.overwriteSaveAs(strFilePath=strTagHtmlFilePath, unicodeData=self.driver.page_source)
            #tag 下一頁
            elesNextPageA = self.driver.find_elements_by_css_selector("div.nav-links a.next.page-numbers")
            while len(elesNextPageA) != 0:
                time.sleep(random.randint(2,5)) #sleep random time
                intPageNum = intPageNum+1
                strTagUrl = elesNextPageA[0].get_attribute("href")
                self.driver.get(strTagUrl)
                #儲存 html
                strTagHtmlFilePath = strTagHtmlFolderPath + u"\\%d_%s_tag.html"%(intPageNum, strNotObtainedTagName)
                self.utility.overwriteSaveAs(strFilePath=strTagHtmlFilePath, unicodeData=self.driver.page_source)
                #tag 再下一頁
                elesNextPageA = self.driver.find_elements_by_css_selector("div.nav-links a.next.page-numbers")
            #更新tag DB 為已抓取 (isGot = 1)
            self.db.updateTagStatusIsGot(strTagName=strNotObtainedTagName)
            logging.info("got tag %s"%strNotObtainedTagName)
            
    #限縮 字串長度低於 128 字元
    def limitStrLessThen128Char(self, strStr=None):
        if len(strStr) > 128:
            logging.info("limit str less then 128 char")
            return strStr[:127] + u"_"
        else:
            return strStr
            
    #下載 news 頁面 (strTagName == None 會自動找尋已下載完成之 tag，但若未先執行 parser tag 即使 tag 已下載完成亦無法下載 news)
    def downloadNewsPage(self, strTagName=None):
        if strTagName is None:
            #未指定 tag
            lstStrObtainedTagName = self.db.fetchallCompletedObtainedTagName()
            for strObtainedTagName in lstStrObtainedTagName:
                self.downloadNewsPageWithGivenTagName(strTagName=strObtainedTagName)
        else:
            #有指定 tag 名稱
            self.downloadNewsPageWithGivenTagName(strTagName=strTagName)
            
    #下載 news 頁面 (指定 tag 名稱)
    def downloadNewsPageWithGivenTagName(self, strTagName=None):
        logging.info("download news page with tag %s"%strTagName)
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE\\news"
        if not os.path.exists(strNewsHtmlFolderPath):
            os.mkdir(strNewsHtmlFolderPath) #mkdir source_html/TECHORANGE/news/
        #取得 DB 紀錄中，指定 strTagName tag 的 news url
        lstStrNewsUrl = self.db.fetchallNewsUrlByTagName(strTagName=strTagName)
        intDownloadedNewsCount = 0#紀錄下載 news 頁面數量
        timeStart = time.time() #計時開始時間點
        timeEnd = None #計時結束時間點
        for strNewsUrl in lstStrNewsUrl:
            #檢查是否已下載
            if not self.db.checkNewsIsGot(strNewsUrl=strNewsUrl):
                if intDownloadedNewsCount%10 == 0: #計算下載10筆news所需時間
                    timeEnd = time.time()
                    timeCost = timeEnd - timeStart
                    logging.info("download 10 news cost %f sec"%timeCost)
                    timeStart = timeEnd
                intDownloadedNewsCount = intDownloadedNewsCount+1
                time.sleep(random.randint(2,5)) #sleep random time
                self.driver.get(strNewsUrl)
                #儲存 html
                strNewsName = re.match("^https://buzzorange.com/techorange/[\d]{4}/[\d]{2}/[\d]{2}/(.*)/$", strNewsUrl).group(1)
                strNewsName = self.limitStrLessThen128Char(strStr=strNewsName) #將名稱縮短小於128字完
                strNewsHtmlFilePath = strNewsHtmlFolderPath + u"\\%s_news.html"%strNewsName
                self.utility.overwriteSaveAs(strFilePath=strNewsHtmlFilePath, unicodeData=self.driver.page_source)
                #更新news DB 為已抓取 (isGot = 1)
                self.db.updateNewsStatusIsGot(strNewsUrl=strNewsUrl)
            