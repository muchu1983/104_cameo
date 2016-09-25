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
            "companies":self.downloadCompaniesPage,
            "company":self.downloadCompanyPage
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
            "companies - download companies page \n"
            "company - download company page \n"
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
            #登入帳號
            self.loginAccount()
        
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
    
    #下載 companies 頁面 
    def downloadCompaniesPage(self, uselessArg1=None):
        logging.info("download companies page")
        strCompaniesHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CROWDCUBE"
        if not os.path.exists(strCompaniesHtmlFolderPath):
            os.mkdir(strCompaniesHtmlFolderPath) #mkdir source_html/CROWDCUBE/
        #CROWDCUBE Funded companies 頁面
        self.driver.get("https://www.crowdcube.com/companies")
        #展開 Load more
        isLoadMoreBtnHide = False
        while not isLoadMoreBtnHide:
            eleLoadMoreBtn = self.driver.find_element_by_css_selector("#loadMoreCompanies")
            strLoadMoreBtnClass = eleLoadMoreBtn.get_attribute("class")
            if "is-hidden" in strLoadMoreBtnClass:
                isLoadMoreBtnHide = True
            else:
                eleLoadMoreBtn.click()
                time.sleep(10)
        #儲存 html
        strCompaniesHtmlFilePath = strCompaniesHtmlFolderPath + u"\\companies.html"
        self.utility.overwriteSaveAs(strFilePath=strCompaniesHtmlFilePath, unicodeData=self.driver.page_source)
    
    #下載 company 頁面
    def downloadCompanyPage(self, uselessArg1=None):
        logging.info("download company page")
        #建立 companies 資料夾
        strCompaniesHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CROWDCUBE\\companies"
        if not os.path.exists(strCompaniesHtmlFolderPath):
            os.mkdir(strCompaniesHtmlFolderPath) #mkdir source_html/CROWDCUBE/companies
        #取得 DB 紀錄中，未完成下載的 company url
        lstStrCompanyUrl = self.db.fetchallNotObtainedCompanyUrl()
        for strCompanyUrl in lstStrCompanyUrl:
            #檢查是否已下載
            if not self.db.checkCompanyIsGot(strCompanyUrl=strCompanyUrl):
                time.sleep(random.randint(5,9)) #sleep random time
                try:
                    self.driver.get(strCompanyUrl)
                    #儲存 html
                    strCompanyName = re.match("^https://www.crowdcube.com/companies/(.*)$", strCompanyUrl).group(1)
                    strCompanyHtmlFilePath = strCompaniesHtmlFolderPath + u"\\%s_company.html"%strCompanyName
                    self.utility.overwriteSaveAs(strFilePath=strCompanyHtmlFilePath, unicodeData=self.driver.page_source)
                    #更新 company DB 為已抓取 (isGot = 1)
                    self.db.updateCompanyStatusIsGot(strCompanyUrl=strCompanyUrl)
                    logging.info("got company page: %s"%strCompanyUrl)
                except Exception as e:
                    logging.warning(str(e))
                    logging.warning("selenium driver crashed. skip get company: %s"%strCompanyUrl)
                    self.restartDriver() #重啟 