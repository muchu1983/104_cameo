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
import re
from cameo.utility import Utility
"""
抓取 貝果 html 存放到 source_html 
"""
class SpiderForWEBACKERS:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.CATEGORY_URL_LIST_FILENAME = u"category_url_list.txt"
        self.PROJ_URL_LIST_FILENAME = u"_proj_url_list.txt"
        self.utility = Utility()
        self.driver = self.getDriver()
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return """- WEBACKERS -
useage:
"""
    
    #取得 selenium driver 物件
    def getDriver(self):
        chromeDriverExeFilePath = ".\cameo_res\chromedriver.exe"
        driver = webdriver.Chrome(chromeDriverExeFilePath)
        return driver
        
    #執行 spider
    def runSpider(self, lstSubcommand=[]):
        pass
        
    #下載 Browse 頁面 並解析
    def downloadBrowsePageAndParseBrowsePage(self):
        strBrowseHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\WEBACKERS"
        if not os.path.exists(strBrowseHtmlFolderPath):
            os.mkdir(strBrowseHtmlFolderPath) #mkdir source_html/WEBACKERS/
        #貝果首頁
        self.driver.get("https://www.webackers.com/")
        #瀏覽提案
        strBrowseUrl = self.driver.find_element_by_css_selector("ul.nav li.font_m1 a[href*='/Proposal/Browse']").get_attribute("href")
        self.driver.get(strBrowseUrl)
        #所有案件
        strAllStatusUrl = self.driver.find_element_by_css_selector("aside.col-md-2 article:nth-of-type(1) a[href*='fundedStatus=ALL']").get_attribute("href")
        self.driver.get(strAllStatusUrl)
        #儲存 browse.html
        strBrowseHtmlFilePath = strBrowseHtmlFolderPath + u"\\browse.html"
        self.utility.overwriteSaveAs(strFilePath=strBrowseHtmlFilePath, unicodeData=self.driver.page_source)
        #解析 category url
        strBrowseResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\WEBACKERS"
        if not os.path.exists(strBrowseResultFolderPath):
            os.mkdir(strBrowseResultFolderPath) #mkdir parsed_result/WEBACKERS/
        strCategoryUrlListFilePath = strBrowseResultFolderPath + u"\\category_url_list.txt"
        elesCategoryUrl = self.driver.find_elements_by_css_selector("aside.col-md-2 article:nth-of-type(2) a")
        with open(strCategoryUrlListFilePath, "w+") as categoryUrlListFile:
            for eleCategoryUrl in elesCategoryUrl:
                categoryUrlListFile.write(eleCategoryUrl.get_attribute("href") + u"\n")
            
    #下載類別頁面
    def downloadCategoryPage(self):
        strCategoryUrlListFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + "\\WEBACKERS\\category_url_list.txt"
        with open(strCategoryUrlListFilePath, "r") as categoryUrlListFile:
            for strCategoryUrl in categoryUrlListFile:
                if "category=ALL" in strCategoryUrl:
                    continue #略過所有類別
                strCategoryName = re.match("^https://www.webackers.com/Proposal/Browse?.*category=([A-Z]*)$", strCategoryUrl).group(1).lower()
                strCategoryHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\WEBACKERS\\%s"%strCategoryName
                if not os.path.exists(strCategoryHtmlFolderPath):
                    os.mkdir(strCategoryHtmlFolderPath) #mkdir source_html/WEBACKERS/category/
                intPageNum = 0
                strCategoryHtmlFilePath = strCategoryHtmlFolderPath + "\\%d_category.html"%intPageNum
                #第0頁
                self.driver.get(strCategoryUrl)
                self.utility.overwriteSaveAs(strFilePath=strCategoryHtmlFilePath, unicodeData=self.driver.page_source)
                #下一頁
                elesNextPageA = self.driver.find_elements_by_css_selector("ul.pagination li:last-of-type a")
                while len(elesNextPageA) != 0:
                    time.sleep(5)
                    intPageNum = intPageNum+1
                    strNextPageUrl = elesNextPageA[0].get_attribute("href")
                    strCategoryHtmlFilePath = strCategoryHtmlFolderPath + "\\%d_category.html"%intPageNum
                    self.driver.get(strNextPageUrl)
                    self.utility.overwriteSaveAs(strFilePath=strCategoryHtmlFilePath, unicodeData=self.driver.page_source)
                    #再下一頁
                    elesNextPageA = self.driver.find_elements_by_css_selector("ul.pagination li:last-of-type a")
                