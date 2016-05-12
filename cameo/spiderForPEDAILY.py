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
from cameo.localdb import LocalDbForPEDAILY
"""
抓取 投資界 html 存放到 source_html 
"""
class SpiderForPEDAILY:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.strWebsiteDomain = u"http://www.pedaily.cn"
        self.dicSubCommandHandler = {"index":self.downloadIndexPage,
                             "category":self.downloadCategoryPage,
                             "news":self.downloadNewsPage}
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
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\PEDAILY"
        if not os.path.exists(strIndexHtmlFolderPath):
            os.mkdir(strIndexHtmlFolderPath) #mkdir source_html/PEDAILY/
        #投資界首頁
        self.driver.get("http://www.pedaily.cn/")
        #儲存 html
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        self.utility.overwriteSaveAs(strFilePath=strIndexHtmlFilePath, unicodeData=self.driver.page_source)
        
    #click 加載更多
    def clickLoadMoreElement(self):
        try:
            eleLoadMoreBtn = self.driver.find_element_by_css_selector("div.box-loadmore a")
            strLoadMoreBtnStyle = eleLoadMoreBtn.get_attribute("style")
            while u"none" not in strLoadMoreBtnStyle:
                time.sleep(random.randint(2,5)) #sleep random time
                eleLoadMoreBtn.click()
                time.sleep(random.randint(2,5)) #sleep random time
                eleLoadMoreBtn = self.driver.find_element_by_css_selector("div.box-loadmore a")
                strLoadMoreBtnStyle = eleLoadMoreBtn.get_attribute("style")
        except NoSuchElementException:
            logging.info("selenium driver can't find the loadmore button.")
            return
        
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
            self.clickLoadMoreElement() #點開 加載更多 按鈕
            #儲存 html
            strCategoryHtmlFilePath = strCategoryHtmlFolderPath + u"\\%s_category.html"%(strNotObtainedTCategoryName)
            self.utility.overwriteSaveAs(strFilePath=strCategoryHtmlFilePath, unicodeData=self.driver.page_source)
            #更新tag DB 為已抓取 (isGot = 1)
            #self.db.updateCategoryStatusIsGot(strCategoryName=strNotObtainedTCategoryName)
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
                time.sleep(random.randint(2,5)) #sleep random time
                self.driver.get(strNewsUrl)
                #儲存 html (pedaily.cn 將 news 儲放在不同台的 server)
                #strNewsName = re.match("^http://www.bnext.com.tw/article/view/id/([0-9]*)$", strNewsUrl).group(1)
                #strNewsHtmlFilePath = strNewsHtmlFolderPath + u"\\%s_news.html"%strNewsName
                #self.utility.overwriteSaveAs(strFilePath=strNewsHtmlFilePath, unicodeData=self.driver.page_source)
                #更新news DB 為已抓取 (isGot = 1)
                #self.db.updateNewsStatusIsGot(strNewsUrl=strNewsUrl)
            