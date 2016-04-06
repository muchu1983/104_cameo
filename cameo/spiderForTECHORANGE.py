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
        self.dicSubCommandHandler = {"index":self.downloadIndexPage,
                                     "tag":None,
                                     "news":None}
        self.utility = Utility()
        self.db = LocalDbForTECHORANGE()
        self.driver = None
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return ("- TECHORANGE -\n"
                "useage:\n"
                "index - \n"
                "tag - \n"
                "news tag - \n")
    
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
        self.driver.get("http://buzzorange.com/techorange/")
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
            strTagUrl = strTagWebsiteDomain + u"/" + strNotObtainedTagName
            #tag 第0頁
            intPageNum = 0
            time.sleep(random.randint(2,5)) #sleep random time
            self.driver.get(strTagUrl)
            #儲存 html
            strTagHtmlFilePath = strTagHtmlFolderPath + u"\\%d_%s_tag.html"%(intPageNum, strNotObtainedTagName)
            self.utility.overwriteSaveAs(strFilePath=strTagHtmlFilePath, unicodeData=self.driver.page_source)
            #tag 下一頁
            elesNextPageA = self.driver.find_elements_by_css_selector("ul.page-numbers li a.next.page-numbers")
            while len(elesNextPageA) != 0:
                time.sleep(random.randint(2,5)) #sleep random time
                intPageNum = intPageNum+1
                strTagUrl = elesNextPageA[0].get_attribute("href")
                self.driver.get(strTagUrl)
                #儲存 html
                strTagHtmlFilePath = strTagHtmlFolderPath + u"\\%d_%s_tag.html"%(intPageNum, strNotObtainedTagName)
                self.utility.overwriteSaveAs(strFilePath=strTagHtmlFilePath, unicodeData=self.driver.page_source)
                #tag 再下一頁
                elesNextPageA = self.driver.find_elements_by_css_selector("ul.page-numbers li a.next.page-numbers")
            #更新tag DB 為已抓取 (isGot = 1)
            self.db.updateTagStatusIsGot(strTagName=strNotObtainedTagName)
            
    #下載 news 頁面 (指定 tag 名稱)
    def downloadNewsPage(self, strTagName=None):
        logging.info("download news page")
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE\\news"
        if not os.path.exists(strNewsHtmlFolderPath):
            os.mkdir(strNewsHtmlFolderPath) #mkdir source_html/TECHORANGE/news/
        #取得 DB 紀錄中，指定 strTagName tag 的 news url
        lstStrNewsUrl = self.db.fetchallNewsUrlByTagName(strTagName=strTagName)
        for strNewsUrl in lstStrNewsUrl:
            time.sleep(random.randint(2,5)) #sleep random time
            self.driver.get(strNewsUrl)
            #儲存 html
            strNewsName = re.match("http://buzzorange.com/techorange/[0-9]*/[0-9]*/[0-9]*/(.*)/", strNewsUrl).group(1)
            strNewsHtmlFilePath = strNewsHtmlFolderPath + u"\\%s_news.html"%strNewsName
            self.utility.overwriteSaveAs(strFilePath=strNewsHtmlFilePath, unicodeData=self.driver.page_source)
            #更新news DB 為已抓取 (isGot = 1)
            