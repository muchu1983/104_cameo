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
import random

"""
抓取 https://tw.money.yahoo.com/currency 即時匯率
"""
class SpiderForYahooCurrency:
    
    #建構子
    def __init__(self):
        self.driver = None
        
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
    def runSpider(self):
        self.initDriver() #init selenium driver
        self.updateCurrencyData()
        self.quitDriver() #quit selenium driver
        
    #更新 滙率 資料
    def updateCurrencyData(self):
        self.driver.get("https://tw.money.yahoo.com/currency")
        #亞洲、美洲、歐非
        elesAreaTabLi = self.driver.find_elements_by_css_selector("ul.sub-tabs.D-ib li")
        intCurrentAreaTab = 0
        while len(elesAreaTabLi) == 3:
            time.sleep(random.randint(2,5))
            elesAreaTabLi[intCurrentAreaTab].click()
            time.sleep(random.randint(2,5))
            elesAreaTabLi = self.driver.find_elements_by_css_selector("ul.sub-tabs.D-ib li")
            intCurrentAreaTab = (intCurrentAreaTab+1)%3