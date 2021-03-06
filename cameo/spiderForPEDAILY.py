# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import time
import logging
import re
import pdb
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from cameo.utility import Utility
from cameo.localdb import LocalDbForPEDAILY
"""
抓取 投資界 html 存放到 source_html 
"""
class SpiderForPEDAILY:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.strWebsiteDomain = u"http://news.pedaily.cn"
        self.dicSubCommandHandler = {
            "index":self.downloadIndexPage,
            "category":self.downloadCategoryPage,
            "news":self.downloadNewsPage
        }
        self.utility = Utility()
        self.db = LocalDbForPEDAILY()
        self.driver = None
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return ("- PEDAILY -\n"
                "useage:\n"
                "index - download entry page of PEDAILY \n"
                "category - download not obtained category page \n"
                "news [category] - download not obtained news [of given category] \n")
    
    #取得 selenium driver 物件
    def getDriver(self):
        chromeDriverExeFilePath = "cameo_res\\chromedriver.exe"
        driver = webdriver.Chrome(chromeDriverExeFilePath)
        #phantomjsDriverExeFilePath = "cameo_res\\phantomjs.exe"
        #driver = webdriver.PhantomJS(phantomjsDriverExeFilePath)
        return driver
        
    #初始化 selenium driver 物件
    def initDriver(self):
        if self.driver is None:
            self.driver = self.getDriver()
        
    #終止 selenium driver 物件
    def quitDriver(self):
        self.driver.quit()
        self.driver = None
        
    #重啟 selenium driver 物件
    def restartDriver(self):
        self.quitDriver()
        self.initDriver()
        
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
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\PEDAILY"
        if not os.path.exists(strIndexHtmlFolderPath):
            os.mkdir(strIndexHtmlFolderPath) #mkdir source_html/PEDAILY/
        #投資界新聞首頁
        self.driver.get("http://news.pedaily.cn/")
        #儲存 html
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        self.utility.overwriteSaveAs(strFilePath=strIndexHtmlFilePath, unicodeData=self.driver.page_source)
        
    #檢查是否有下一頁
    def getNextCategoryPageHref(self, isCurrentFirstPage=False):
        elesNextPageA = self.driver.find_elements_by_css_selector("div.page-list a.next")
        strNextPageAHref = None
        #pedaily 的 上一頁與下一頁的 css 語法均相同: div.page-list a.next
        #若無下一頁則 下一頁會變成 div.page-list span.next
        if isCurrentFirstPage:
            strNextPageAHref = elesNextPageA[0].get_attribute("href")
        elif len(elesNextPageA) == 2: 
            strNextPageAHref = elesNextPageA[-1].get_attribute("href")
        if strNextPageAHref and "http://news.pedaily.cn/" in strNextPageAHref:
            return strNextPageAHref
        else:
            return None
        
    #下載 category 頁面
    def downloadCategoryPage(self, uselessArg1=None):
        logging.info("download category page")
        strCategoryHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\PEDAILY\\category"
        if not os.path.exists(strCategoryHtmlFolderPath):
            os.mkdir(strCategoryHtmlFolderPath) #mkdir source_html/PEDAILY/category/
        #取得 Db 中尚未下載的 category 名稱
        lstStrNotObtainedTCategoryName = self.db.fetchallNotObtainedCategoryName()
        for strNotObtainedTCategoryName in lstStrNotObtainedTCategoryName:
            strCategoryUrl = self.strWebsiteDomain + u"/" + strNotObtainedTCategoryName
            #category 頁面
            time.sleep(random.randint(2,5)) #sleep random time
            self.driver.get(strCategoryUrl)
            intCategoryPageIndex = 0
            #儲存 html
            strCategoryHtmlFilePath = strCategoryHtmlFolderPath + u"\\%d_%s_category.html"%(intCategoryPageIndex, strNotObtainedTCategoryName)
            self.utility.overwriteSaveAs(strFilePath=strCategoryHtmlFilePath, unicodeData=self.driver.page_source)
            #取得下一頁的 url
            strNextPageAHref = self.getNextCategoryPageHref(isCurrentFirstPage=True)
            while strNextPageAHref: #檢查是否有下一頁
                intCategoryPageIndex = intCategoryPageIndex + 1
                self.driver.get(strNextPageAHref)
                time.sleep(random.randint(5,10)) #sleep random time
                strCategoryHtmlFilePath = strCategoryHtmlFolderPath + u"\\%d_%s_category.html"%(intCategoryPageIndex, strNotObtainedTCategoryName)
                self.utility.overwriteSaveAs(strFilePath=strCategoryHtmlFilePath, unicodeData=self.driver.page_source)
                strNextPageAHref = self.getNextCategoryPageHref()
            #更新tag DB 為已抓取 (isGot = 1)
            self.db.updateCategoryStatusIsGot(strCategoryName=strNotObtainedTCategoryName)
            logging.info("got category %s"%strNotObtainedTCategoryName)
            
    #下載 news 頁面 (strCategoryName == None 會自動找尋已下載完成之 category)
    def downloadNewsPage(self, strCategoryName=None):
        if strCategoryName is None:
            #未指定 category
            lstStrObtainedCategoryName = self.db.fetchallCompletedObtainedCategoryName()
            for strObtainedCategoryName in lstStrObtainedCategoryName:
                self.downloadNewsPageWithGivenCategoryName(strCategoryName=strObtainedCategoryName)
        else:
            #有指定 category 名稱
            self.downloadNewsPageWithGivenCategoryName(strCategoryName=strCategoryName)
            
    #下載 news 頁面 (指定 category 名稱)
    def downloadNewsPageWithGivenCategoryName(self, strCategoryName=None):
        logging.info("download news page with category %s"%strCategoryName)
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\PEDAILY\\news"
        if not os.path.exists(strNewsHtmlFolderPath):
            os.mkdir(strNewsHtmlFolderPath) #mkdir source_html/PEDAILY/news/
        #取得 DB 紀錄中，指定 strCategoryName category 的 news url
        lstStrNewsUrl = self.db.fetchallNewsUrlByCategoryName(strCategoryName=strCategoryName)
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
                time.sleep(random.randint(5,9)) #sleep random time
                try:
                    self.driver.get(strNewsUrl)
                    #儲存 html (記錄 news 儲放的 xxx.pedaily.cn server 名稱)
                    strNewsServerName = re.match("^http://([a-z]*).pedaily.cn/.*/([0-9]*).shtml$", strNewsUrl).group(1)
                    strNewsName = re.match("^http://([a-z]*).pedaily.cn/.*/([0-9]*).shtml$", strNewsUrl).group(2)
                    strNewsHtmlFilePath = strNewsHtmlFolderPath + u"\\%s_%s_news.html"%(strNewsName, strNewsServerName)
                    self.utility.overwriteSaveAs(strFilePath=strNewsHtmlFilePath, unicodeData=self.driver.page_source)
                    #更新news DB 為已抓取 (isGot = 1)
                    self.db.updateNewsStatusIsGot(strNewsUrl=strNewsUrl)
                except:
                    logging.warning("selenium driver crashed. skip get news: %s"%strNewsUrl)
                finally:
                    self.restartDriver() #重啟 
            