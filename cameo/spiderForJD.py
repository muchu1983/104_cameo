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
import random
import urllib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from cameo.utility import Utility
from cameo.localdb import LocalDbForJD
"""
抓取 京東眾籌 html 存放到 source_html 
"""
class SpiderForJD:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.strWebsiteDomain = u"http://z.jd.com"
        self.dicSubCommandHandler = {
            "index":self.downloadIndexPage,
            "category":self.downloadCategoryPage,
            "project":self.downloadProjectPage,
            "funder":self.downloadFunderPage
        }
        self.utility = Utility()
        self.db = LocalDbForJD()
        self.driver = None
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return (
            "- JD -\n"
            "useage:\n"
            "index - download category index page of JD \n"
            "category - download not obtained category page \n"
            "project [category_page_1_url] - download not obtained project [of given category_page_1_url] \n"
            "funder [category_page_1_url] - download not obtained funder [of given category_page_1_url] \n"
        )
    
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
        time.sleep(5)
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
        logging.info("download category index page")
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD"
        if not os.path.exists(strIndexHtmlFolderPath):
            os.mkdir(strIndexHtmlFolderPath) #mkdir source_html/JD/
        #JD category index 頁面
        self.driver.get("http://z.jd.com/sceneIndex.html")
        #儲存 html
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        self.utility.overwriteSaveAs(strFilePath=strIndexHtmlFilePath, unicodeData=self.driver.page_source)
        
    #檢查是否有下一頁 category
    def hasNextCategoryPage(self):
        isHasNextCategoryPage = False
        elesNextPageA = self.driver.find_elements_by_css_selector("div.pagesbox div.ui-page a.next")
        if len(elesNextPageA) > 0:
            isHasNextCategoryPage = True
        return isHasNextCategoryPage
        
    #下載 category 頁面
    def downloadCategoryPage(self, uselessArg1=None):
        logging.info("download category page")
        strCategoryHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD\\category"
        if not os.path.exists(strCategoryHtmlFolderPath):
            os.mkdir(strCategoryHtmlFolderPath) #mkdir source_html/JD/category/
        #取得 Db 中尚未下載的 category url
        lstStrNotObtainedCategoryPage1Url = self.db.fetchallNotObtainedCategoryUrl()
        for strNotObtainedCategoryPage1Url in lstStrNotObtainedCategoryPage1Url:
            #category 頁面
            try:
                #取出 category 名稱
                strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strNotObtainedCategoryPage1Url)
                #category 第0頁
                intPageNum = 0
                time.sleep(random.randint(2,5)) #sleep random time
                self.driver.get(strNotObtainedCategoryPage1Url)
                #儲存 html
                strCategoryHtmlFilePath = strCategoryHtmlFolderPath + u"\\%d_%s_category.html"%(intPageNum, strCategoryName)
                self.utility.overwriteSaveAs(strFilePath=strCategoryHtmlFilePath, unicodeData=self.driver.page_source)
                #category 下一頁
                while self.hasNextCategoryPage():
                    time.sleep(random.randint(5,8)) #sleep random time
                    intPageNum = intPageNum+1
                    #點擊下一頁
                    self.driver.find_element_by_css_selector("div.pagesbox div.ui-page a.next").click()
                    #儲存 html
                    strCayegoryHtmlFilePath = strCategoryHtmlFolderPath + u"\\%d_%s_category.html"%(intPageNum, strCategoryName)
                    self.utility.overwriteSaveAs(strFilePath=strCayegoryHtmlFilePath, unicodeData=self.driver.page_source)
                #更新 category DB 為已抓取 (isGot = 1)
                self.db.updateCategoryStatusIsGot(strCategoryPage1Url=strNotObtainedCategoryPage1Url)
                logging.info("got category %s"%strCategoryName)
            except Exception as e:
                logging.warning(str(e))
                logging.warning("selenium driver crashed. skip get category: %s"%strNotObtainedCategoryPage1Url)
            finally:
                self.restartDriver() #重啟
            
    #下載 project 頁面 (strCategoryPage1Url == None 會自動找尋已下載完成之 category)
    def downloadProjectPage(self, strCategoryPage1Url=None):
        if strTopicPage1Url is None:
            #未指定 topic
            lstStrObtainedTopicUrl = self.db.fetchallCompletedObtainedTopicUrl()
            for strObtainedTopicUrl in lstStrObtainedTopicUrl:
                self.downloadNewsPageWithGivenTopicUrl(strTopicPage1Url=strObtainedTopicUrl)
        else:
            #有指定 topic url
            self.downloadNewsPageWithGivenTopicUrl(strTopicPage1Url=strTopicPage1Url)
            
    #下載 news 頁面 (指定 topic url)
    def downloadNewsPageWithGivenTopicUrl(self, strTopicPage1Url=None):
        logging.info("download news page with topic %s"%strTopicPage1Url)
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\news"
        if not os.path.exists(strNewsHtmlFolderPath):
            os.mkdir(strNewsHtmlFolderPath) #mkdir source_html/TECHCRUNCH/news/
        #取得 DB 紀錄中，指定 strTopicPage1Url topic 的 news url
        lstStrNewsUrl = self.db.fetchallNewsUrlByTopicUrl(strTopicPage1Url=strTopicPage1Url)
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
                    #儲存 html
                    strNewsName = re.match("^https://techcrunch.com/[\d]{4}/[\d]{2}/[\d]{2}/(.*)/$", strNewsUrl).group(1)
                    strNewsHtmlFilePath = strNewsHtmlFolderPath + u"\\%s_news.html"%strNewsName
                    self.utility.overwriteSaveAs(strFilePath=strNewsHtmlFilePath, unicodeData=self.driver.page_source)
                    #更新news DB 為已抓取 (isGot = 1)
                    self.db.updateNewsStatusIsGot(strNewsUrl=strNewsUrl)
                except:
                    logging.warning("selenium driver crashed. skip get news: %s"%strNewsUrl)
                finally:
                    self.restartDriver() #重啟 
            
    #下載 funder 頁面 (strCategoryPage1Url == None 會自動找尋已下載完成之 category)
    def downloadFunderPage(self, strCategoryPage1Url=None):
        if strTopicPage1Url is None:
            #未指定 topic
            lstStrObtainedTopicUrl = self.db.fetchallCompletedObtainedTopicUrl()
            for strObtainedTopicUrl in lstStrObtainedTopicUrl:
                self.downloadNewsPageWithGivenTopicUrl(strTopicPage1Url=strObtainedTopicUrl)
        else:
            #有指定 topic url
            self.downloadNewsPageWithGivenTopicUrl(strTopicPage1Url=strTopicPage1Url)
            
    #下載 news 頁面 (指定 topic url)
    def downloadNewsPageWithGivenTopicUrl(self, strTopicPage1Url=None):
        logging.info("download news page with topic %s"%strTopicPage1Url)
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\news"
        if not os.path.exists(strNewsHtmlFolderPath):
            os.mkdir(strNewsHtmlFolderPath) #mkdir source_html/TECHCRUNCH/news/
        #取得 DB 紀錄中，指定 strTopicPage1Url topic 的 news url
        lstStrNewsUrl = self.db.fetchallNewsUrlByTopicUrl(strTopicPage1Url=strTopicPage1Url)
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
                    #儲存 html
                    strNewsName = re.match("^https://techcrunch.com/[\d]{4}/[\d]{2}/[\d]{2}/(.*)/$", strNewsUrl).group(1)
                    strNewsHtmlFilePath = strNewsHtmlFolderPath + u"\\%s_news.html"%strNewsName
                    self.utility.overwriteSaveAs(strFilePath=strNewsHtmlFilePath, unicodeData=self.driver.page_source)
                    #更新news DB 為已抓取 (isGot = 1)
                    self.db.updateNewsStatusIsGot(strNewsUrl=strNewsUrl)
                except:
                    logging.warning("selenium driver crashed. skip get news: %s"%strNewsUrl)
                finally:
                    self.restartDriver() #重啟 