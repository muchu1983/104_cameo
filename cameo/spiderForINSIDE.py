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
from cameo.localdb import LocalDbForINSIDE
"""
抓取 硬塞的 html 存放到 source_html 
"""
class SpiderForINSIDE:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.strWebsiteDomain = u"https://www.inside.com.tw/"
        self.dicSubCommandHandler = {
            "index":self.downloadIndexPage,
            "tag":self.downloadTagPage,
            "news":self.downloadNewsPage
        }
        self.utility = Utility()
        self.db = LocalDbForINSIDE()
        self.driver = None
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return ("- INSIDE -\n"
                "useage:\n"
                "index - download entry page of INSIDE \n"
                "tag - download not obtained tag page \n"
                "news [tag_page1_url] - download not obtained news [of given tag_page1_url] \n")
    
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
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\INSIDE"
        if not os.path.exists(strIndexHtmlFolderPath):
            os.mkdir(strIndexHtmlFolderPath) #mkdir source_html/INSIDE/
        #硬塞的 首頁
        self.driver.get("http://www.inside.com.tw")
        #儲存 html
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        self.utility.overwriteSaveAs(strFilePath=strIndexHtmlFilePath, unicodeData=self.driver.page_source)
        
    #找出下一頁 tag 的 url
    def findNextTagPageUrl(self):
        strNextTagPageUrl = None
        elesNextPageA = self.driver.find_elements_by_css_selector("div.nav-previous a")
        if len(elesNextPageA) == 1:
            strNextTagPageUrl = elesNextPageA[0].get_attribute("href")
        return strNextTagPageUrl
        
    #下載 tag 頁面
    def downloadTagPage(self, uselessArg1=None):
        logging.info("download tag page")
        strTagHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\INSIDE\\tag"
        if not os.path.exists(strTagHtmlFolderPath):
            os.mkdir(strTagHtmlFolderPath) #mkdir source_html/INSIDE/tag/
        #取得 Db 中尚未下載的 Tag 名稱
        lstStrNotObtainedTagPage1Url = self.db.fetchallNotObtainedTagPage1Url()
        for strNotObtainedTagPage1Url in lstStrNotObtainedTagPage1Url:
            #re 找出 tag 名稱
            strTagNamePartInUrl = re.match("^https://www.inside.com.tw/category/(.*)$", strNotObtainedTagPage1Url).group(1)
            strTagName = re.sub(u"/", u"__", strTagNamePartInUrl)
            #tag 第0頁
            intPageNum = 0
            time.sleep(random.randint(2,5)) #sleep random time
            self.driver.get(strNotObtainedTagPage1Url)
            #儲存 html
            strTagHtmlFilePath = strTagHtmlFolderPath + u"\\%d_%s_tag.html"%(intPageNum, strTagName)
            self.utility.overwriteSaveAs(strFilePath=strTagHtmlFilePath, unicodeData=self.driver.page_source)
            #tag 下一頁
            strNextTagPageUrl = self.findNextTagPageUrl()
            while strNextTagPageUrl: # is not None
                time.sleep(random.randint(2,5)) #sleep random time
                intPageNum = intPageNum+1
                self.driver.get(strNextTagPageUrl)
                #儲存 html
                strTagHtmlFilePath = strTagHtmlFolderPath + u"\\%d_%s_tag.html"%(intPageNum, strTagName)
                self.utility.overwriteSaveAs(strFilePath=strTagHtmlFilePath, unicodeData=self.driver.page_source)
                #tag 再下一頁
                strNextTagPageUrl = self.findNextTagPageUrl()
            #更新tag DB 為已抓取 (isGot = 1)
            self.db.updateTagStatusIsGot(strTagPage1Url=strNotObtainedTagPage1Url)
            logging.info("got tag %s"%strTagName)
            
    #下載 news 頁面 (strTagPage1Url == None 會自動找尋已下載完成之 tag，但若未先執行 parser tag 即使 tag 已下載完成亦無法下載 news)
    def downloadNewsPage(self, strTagPage1Url=None):
        if strTagPage1Url is None:
            #未指定 tag
            lstStrObtainedTagPage1Url = self.db.fetchallCompletedObtainedTagPage1Url()
            for strObtainedTagPage1Url in lstStrObtainedTagPage1Url:
                self.downloadNewsPageWithGivenTagName(strTagPage1Url=strObtainedTagPage1Url)
        else:
            #有指定 tag 名稱
            self.downloadNewsPageWithGivenTagName(strTagPage1Url=strTagPage1Url)
            
    #下載 news 頁面 (指定 tag 第一頁 url)
    def downloadNewsPageWithGivenTagName(self, strTagPage1Url=None):
        logging.info("download news page with tag %s"%strTagPage1Url)
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\INSIDE\\news"
        if not os.path.exists(strNewsHtmlFolderPath):
            os.mkdir(strNewsHtmlFolderPath) #mkdir source_html/INSIDE/news/
        #取得 DB 紀錄中，指定 strTagName tag 的 news url
        lstStrNewsUrl = self.db.fetchallNewsUrlByTagPage1Url(strTagPage1Url=strTagPage1Url)
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
                strNewsName = re.match("^http://www.inside.com.tw/[\d]{4}/[\d]{2}/[\d]{2}/(.*)$", strNewsUrl).group(1)
                #限縮 news.html 檔名
                strNewsName = self.limitStrLessThen128Char(strStr=strNewsName)
                strNewsHtmlFilePath = strNewsHtmlFolderPath + u"\\%s_news.html"%strNewsName
                self.utility.overwriteSaveAs(strFilePath=strNewsHtmlFilePath, unicodeData=self.driver.page_source)
                #更新news DB 為已抓取 (isGot = 1)
                self.db.updateNewsStatusIsGot(strNewsUrl=strNewsUrl)
            
    #限縮 字串長度低於 128 字元
    def limitStrLessThen128Char(self, strStr=None):
        if len(strStr) > 128:
            logging.info("limit str less then 128 char")
            return strStr[:127] + u"_"
        else:
            return strStr