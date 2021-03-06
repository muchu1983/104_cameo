# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from selenium import webdriver
import os
import logging
import time
import datetime
import re
import random
import pkg_resources
from cameo.externaldb import ExternalDbForCurrencyApi
#from cameo.localdb import LocalDbForCurrencyApi #測試用本地端 db

"""
抓取 https://tw.money.yahoo.com/currency 即時匯率
"""
class SpiderForYahooCurrency:
    
    #建構子
    def __init__(self):
        self.driver = None
        self.db = ExternalDbForCurrencyApi().mongodb
        #self.db = LocalDbForCurrencyApi().mongodb #測試用本地端 db
        
    #取得 selenium driver 物件
    def getDriver(self):
        #chromeDriverExeFilePath = pkg_resources.resource_filename("cameo_res", "chromedriver.exe")
        #driver = webdriver.Chrome(chromeDriverExeFilePath)
        phantomjsDriverExeFilePath = pkg_resources.resource_filename("cameo_res", "phantomjs.exe")
        driver = webdriver.PhantomJS(phantomjsDriverExeFilePath)
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
    def runSpider(self):
        self.initDriver() #init selenium driver
        self.updateExRateData()
        self.quitDriver() #quit selenium driver
        
    #更新 匯率 資料
    def updateExRateData(self):
        self.driver.get("https://tw.money.yahoo.com/currency")
        #亞洲、美洲、歐非
        elesAreaTabLi = self.driver.find_elements_by_css_selector("ul.sub-tabs.D-ib li")
        intCurrentAreaTab = 0
        while len(elesAreaTabLi) == 3:
            time.sleep(random.randint(20,30))
            elesAreaTabLi[intCurrentAreaTab].click()
            time.sleep(random.randint(20,30))
            #解析 匯率資料
            elesExRateTr = self.driver.find_elements_by_css_selector("tbody tr.Bd-b")
            for eleExRateTr in elesExRateTr:
                strExRateHref = eleExRateTr.find_element_by_css_selector("td.Ta-start a").get_attribute("href")
                strCurrencyName = re.match("https://tw.money.yahoo.com/currency/(USD...)=X", strExRateHref).group(1)
                strUSDollar = eleExRateTr.find_element_by_css_selector("td.Ta-end:nth-of-type(3)").text
                # update DB
                logging.info("start update ex-rate data...")
                strTimeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db.ModelExRate.update_one({"strCurrencyName":strCurrencyName},
                                   {"$set": {"strDate":strTimeNow,
                                          "strCurrencyName":strCurrencyName,
                                          "fUSDollar":float(strUSDollar)
                                          }
                                   }, 
                                   upsert=True) #upsert = update or insert if data not exists (有則更新，無則新增)
                logging.info("ex-rate data updated. [%s]"%strTimeNow)
            #準備切換至下一個 area tab
            elesAreaTabLi = self.driver.find_elements_by_css_selector("ul.sub-tabs.D-ib li")
            intCurrentAreaTab = (intCurrentAreaTab+1)%3