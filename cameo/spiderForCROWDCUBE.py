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
import string
import urllib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from cameo.utility import Utility
from cameo.localdb import LocalDbForCROWDCUBE
"""
抓取 CROWDCUBE html 存放到 source_html 
"""
class SpiderForCROWDCUBE:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.strWebsiteDomain = u""
        self.dicSubCommandHandler = {
            "register":self.registerAccount,
            "index":self.downloadIndexPage,
            "category":self.downloadCategoryPage,
            "project":self.downloadProjectPage,
            "funder":self.downloadFunderPage
        }
        self.utility = Utility()
        self.db = LocalDbForCROWDCUBE()
        self.driver = None
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return (
            "- CROWDCUBE -\n"
            "useage:\n"
            "register - register 10 account for use \n"
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
        
    #註冊帳號
    def registerAccount(self, uselessArg1=None):
        logging.info("register account")
        strAccountPassword = u"bee520"
        strAccountEmailTemplate = u"ebucdworc+{0:04d}@gmail.com"
        #+01~+99 實驗用，+100~+999 開發測試用，+1000~+9999 上線用
        for intAccountIndex in range(104, 106):
            #取得 element 準備填入資料
            strAccountEmail = strAccountEmailTemplate.format(intAccountIndex)
            self.driver.get("https://www.crowdcube.com/register#details")
            eleFirstName = self.driver.find_element_by_id("input-first-name")
            eleLastName = self.driver.find_element_by_id("input-last-name")
            eleEmail = self.driver.find_element_by_id("input-email")
            elePassword = self.driver.find_element_by_id("input-password")
            eleNickName = self.driver.find_element_by_id("input-username")
            #send_keys
            strRandomStr = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
            eleFirstName.send_keys(strRandomStr)
            strRandomStr = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
            eleLastName.send_keys(strRandomStr)
            eleEmail.send_keys(strAccountEmail)
            elePassword.send_keys(strAccountPassword)
            strRandomStr = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
            eleNickName.send_keys(strRandomStr)
            time.sleep(10)
            self.driver.find_element_by_css_selector("#register-proceed a").click() #Next
            time.sleep(10)
            self.driver.find_element_by_css_selector("label.cc-investorTypeLabel[for=everyday]").click() #Everyday Investor
            time.sleep(10)
            self.driver.find_element_by_css_selector("div.cc-register__submit button.button").click() #Join
            time.sleep(10)
            #檢查是否成功註冊
            if self.driver.find_element_by_css_selector("div h1.cc-heading").text.startswith("Welcome"):
                #save to localdb
                self.db.insertAccountIfNotExists(strEmail=strAccountEmail, strPassword=strAccountPassword)
                #logout
                self.driver.get("https://www.crowdcube.com/logout")
                time.sleep(10)
    
    #登入帳號
    def loginAccount(self):
        #get ready account
        (strAccountEmail, strAccountPassword) = self.db.fetchRandomReadyAccount()
        #login page
        self.driver.get("https://www.crowdcube.com/login")
        #填入帳密
        eleEmail = self.driver.find_element_by_id("input-email")
        elePassword = self.driver.find_element_by_id("input-password")
        eleEmail.send_keys(strAccountEmail)
        elePassword.send_keys(strAccountPassword)
        time.sleep(10)
        #Login
        self.driver.find_element_by_css_selector("#login-form button.button").click()
        time.sleep(30)
    
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
        
    #下載 category 頁面 (strCategoryPage1Url == None 會自動找尋尚未下載之 category)
    def downloadCategoryPage(self, strCategoryPage1Url=None):
        if strCategoryPage1Url is None:
            #未指定 category url
            #取得 Db 中尚未下載的 category url
            lstStrNotObtainedCategoryPage1Url = self.db.fetchallNotObtainedCategoryUrl()
            for strNotObtainedCategoryPage1Url in lstStrNotObtainedCategoryPage1Url:
                self.downloadCategoryPageWithGivenCategoryUrl(strCategoryPage1Url=strNotObtainedCategoryPage1Url)
        else:
            #有指定 category url
            self.downloadCategoryPageWithGivenCategoryUrl(strCategoryPage1Url=strCategoryPage1Url)
        
    #下載 category 頁面 (指定 category url)
    def downloadCategoryPageWithGivenCategoryUrl(self, strCategoryPage1Url=None):
        logging.info("download category page: %s"%strCategoryPage1Url)
        #取出 category 名稱
        strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strCategoryPage1Url)
        strCategoryHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD\\%s"%strCategoryName
        if not os.path.exists(strCategoryHtmlFolderPath):
            os.mkdir(strCategoryHtmlFolderPath) #mkdir source_html/JD/category/
        #抓取 category 頁面
        try:
            #category 第0頁
            intPageNum = 0
            time.sleep(random.randint(2,5)) #sleep random time
            self.driver.get(strCategoryPage1Url)
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
            self.db.updateCategoryStatusIsGot(strCategoryPage1Url=strCategoryPage1Url)
            logging.info("got category %s"%strCategoryName)
        except Exception as e:
            logging.warning(str(e))
            logging.warning("selenium driver crashed. skip get category: %s"%strCategoryPage1Url)
        finally:
            self.restartDriver() #重啟
            
    #下載 project 頁面 (strCategoryPage1Url == None 會自動找尋已下載完成之 category)
    def downloadProjectPage(self, strCategoryPage1Url=None):
        if strCategoryPage1Url is None:
            #未指定 category url
            lstStrObtainedCategoryUrl = self.db.fetchallCompletedObtainedCategoryUrl()
            for strObtainedCategoryUrl in lstStrObtainedCategoryUrl:
                self.downloadProjectPageWithGivenCategoryUrl(strCategoryPage1Url=strObtainedCategoryUrl)
        else:
            #有指定 category url
            self.downloadProjectPageWithGivenCategoryUrl(strCategoryPage1Url=strCategoryPage1Url)
            
    #下載 project 頁面 (指定 category url)
    def downloadProjectPageWithGivenCategoryUrl(self, strCategoryPage1Url=None):
        logging.info("download project page with category %s"%strCategoryPage1Url)
        #取出 category 名稱
        strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strCategoryPage1Url)
        strProjectHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD\\%s\\projects"%strCategoryName
        if not os.path.exists(strProjectHtmlFolderPath):
            os.mkdir(strProjectHtmlFolderPath) #mkdir source_html/JD/category/projects
        #取得 DB 紀錄中，指定 strCategoryPage1Url category 的 project url
        lstStrProjectUrl = self.db.fetchallProjectUrlByCategoryUrl(strCategoryPage1Url=strCategoryPage1Url)
        intDownloadedProjectCount = 0 #紀錄下載 project 頁面數量
        timeStart = time.time() #計時開始時間點
        timeEnd = None #計時結束時間點
        for strProjectUrl in lstStrProjectUrl:
            #檢查是否已下載
            if not self.db.checkProjectIsGot(strProjectUrl=strProjectUrl):
                if intDownloadedProjectCount%10 == 0: #計算下載10筆 project 所需時間
                    timeEnd = time.time()
                    timeCost = timeEnd - timeStart
                    logging.info("download 10 project cost %f sec"%timeCost)
                    timeStart = timeEnd
                intDownloadedProjectCount = intDownloadedProjectCount+1
                time.sleep(random.randint(5,9)) #sleep random time
                try:
                    self.driver.get(strProjectUrl)
                    #儲存 html
                    strProjectName = re.match("^http://z.jd.com/project/details/([\d]+).html$", strProjectUrl).group(1)
                    #_intro.html
                    strIntroHtmlFilePath = strProjectHtmlFolderPath + u"\\%s_intro.html"%strProjectName
                    self.utility.overwriteSaveAs(strFilePath=strIntroHtmlFilePath, unicodeData=self.driver.page_source)
                    #_progress.html
                    self.driver.find_element_by_css_selector("#qaBtn").click()
                    time.sleep(random.randint(3,7)) #sleep random time
                    strProgressHtmlFilePath = strProjectHtmlFolderPath + u"\\%s_progress.html"%strProjectName
                    self.utility.overwriteSaveAs(strFilePath=strProgressHtmlFilePath, unicodeData=self.driver.page_source)
                    #_qanda.html
                    self.driver.find_element_by_css_selector("#topicBtn").click()
                    time.sleep(random.randint(3,7)) #sleep random time
                    strQandaHtmlFilePath = strProjectHtmlFolderPath + u"\\%s_qanda.html"%strProjectName
                    self.utility.overwriteSaveAs(strFilePath=strQandaHtmlFilePath, unicodeData=self.driver.page_source)
                    #_sponsor.html
                    self.driver.find_element_by_css_selector("#supporterBtn").click()
                    time.sleep(random.randint(3,7)) #sleep random time
                    strSponsorHtmlFilePath = strProjectHtmlFolderPath + u"\\%s_sponsor.html"%strProjectName
                    self.utility.overwriteSaveAs(strFilePath=strSponsorHtmlFilePath, unicodeData=self.driver.page_source)
                    #取得 funder url 並 insert into DB
                    time.sleep(random.randint(3,7)) #sleep random time
                    strFunderUrl = self.driver.find_element_by_css_selector("div.promoters-detail div.promoters-name a").get_attribute("href")
                    self.db.insertFunderUrlIfNotExists(strFunderUrl=strFunderUrl, strCategoryPage1Url=strCategoryPage1Url)
                    #更新 project DB 為已抓取 (isGot = 1)
                    self.db.updateProjectStatusIsGot(strProjectUrl=strProjectUrl)
                except Exception as e:
                    logging.warning(str(e))
                    logging.warning("selenium driver crashed. skip get project: %s"%strProjectUrl)
                finally:
                    self.restartDriver() #重啟 
            
    #下載 funder 頁面 (strCategoryPage1Url == None 會自動找尋已下載完成之 category)
    def downloadFunderPage(self, strCategoryPage1Url=None):
        if strCategoryPage1Url is None:
            #未指定 category url
            lstStrObtainedCategoryUrl = self.db.fetchallCompletedObtainedCategoryUrl()
            for strObtainedCategoryUrl in lstStrObtainedCategoryUrl:
                self.downloadFunderPageWithGivenCategoryUrl(strCategoryPage1Url=strObtainedCategoryUrl)
        else:
            #有指定 category url
            self.downloadFunderPageWithGivenCategoryUrl(strCategoryPage1Url=strCategoryPage1Url)
            
    #下載 funder 頁面 (指定 category url)
    def downloadFunderPageWithGivenCategoryUrl(self, strCategoryPage1Url=None):
        logging.info("download funder page with category %s"%strCategoryPage1Url)
        #取出 category 名稱
        strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strCategoryPage1Url)
        strFunderHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD\\%s\\profiles"%strCategoryName
        if not os.path.exists(strFunderHtmlFolderPath):
            os.mkdir(strFunderHtmlFolderPath) #mkdir source_html/JD/category/profiles
        #取得 DB 紀錄中，指定 strCategoryPage1Url category 的 funder url
        lstStrFunderUrl = self.db.fetchallFunderUrlByCategoryUrl(strCategoryPage1Url=strCategoryPage1Url)
        intDownloadedFunderCount = 0 #紀錄下載 funder 頁面數量
        timeStart = time.time() #計時開始時間點
        timeEnd = None #計時結束時間點
        for strFunderUrl in lstStrFunderUrl:
            #檢查是否已下載
            if not self.db.checkFunderIsGot(strFunderUrl=strFunderUrl):
                if intDownloadedFunderCount%10 == 0: #計算下載10筆 funder 所需時間
                    timeEnd = time.time()
                    timeCost = timeEnd - timeStart
                    logging.info("download 10 funder cost %f sec"%timeCost)
                    timeStart = timeEnd
                intDownloadedFunderCount = intDownloadedFunderCount+1
                time.sleep(random.randint(5,9)) #sleep random time
                try:
                    self.driver.get(strFunderUrl)
                    #儲存 html
                    strFunderName = re.match("^http://z.jd.com/funderCenter.action\?flag=[\d]+&id=([\d]+)$", strFunderUrl).group(1)
                    #_order.html
                    self.driver.find_element_by_css_selector("div.myCentNav a:nth-of-type(1)").click()
                    time.sleep(random.randint(3,7)) #sleep random time
                    strOrderHtmlFilePath = strFunderHtmlFolderPath + u"\\%s_order.html"%strFunderName
                    self.utility.overwriteSaveAs(strFilePath=strOrderHtmlFilePath, unicodeData=self.driver.page_source)
                    #_proj.html
                    self.driver.find_element_by_css_selector("div.myCentNav a:nth-of-type(2)").click()
                    time.sleep(random.randint(3,7)) #sleep random time
                    strProjHtmlFilePath = strFunderHtmlFolderPath + u"\\%s_proj.html"%strFunderName
                    self.utility.overwriteSaveAs(strFilePath=strProjHtmlFilePath, unicodeData=self.driver.page_source)
                    #_sub.html
                    self.driver.find_element_by_css_selector("div.myCentNav a:nth-of-type(3)").click()
                    time.sleep(random.randint(3,7)) #sleep random time
                    strSubHtmlFilePath = strFunderHtmlFolderPath + u"\\%s_sub.html"%strFunderName
                    self.utility.overwriteSaveAs(strFilePath=strSubHtmlFilePath, unicodeData=self.driver.page_source)
                    #更新 funder DB 為已抓取 (isGot = 1)
                    self.db.updateFunderStatusIsGot(strFunderUrl=strFunderUrl)
                except Exception as e:
                    logging.warning(str(e))
                    logging.warning("selenium driver crashed. skip get funder: %s"%strFunderUrl)
                finally:
                    self.restartDriver() #重啟 