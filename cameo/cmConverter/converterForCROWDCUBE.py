# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import re
import os
import dateparser
from cameo.utility import Utility as CameoUtility
from crawlermaster.utility import Utility as CmUtility

class ConverterForCROWDCUBE:
    
    #建構子
    def __init__(self):
        self.cmUtility = CmUtility()
        self.cameoUtility = CameoUtility()
        self.dicParsedResultOfStartup = {} #startup.json 資料
        
    #轉換 startup 資訊
    def convertStartup(self, lstLstDicRawData=[]):
        #_company.html raw data
        lstDicCompanyPageRawData = lstLstDicRawData[0]
        for dicCompanyPageRawData in lstDicCompanyPageRawData[0:]:
            strCompanyFilePath = dicCompanyPageRawData.get("meta-data-html-filepath", None)
            logging.info("convert: %s"%strCompanyFilePath)
            strCompanyId = re.search("^.*\\\\(.*)_company.html$", strCompanyFilePath).group(1)
            strCompanyUrl = u"https://www.crowdcube.com/companies/" + strCompanyId
            #檢查 資料是否有誤
            lstCompanyData = dicCompanyPageRawData.get("cc-company", [])
            lstLocationData = dicCompanyPageRawData.get("cc-Location", [])
            if lstCompanyData == [] or lstLocationData == []:
                #錯誤資料 跳過
                #os.remove(strOrganizationHtmlFilePath)
                continue
            #建立 dict
            if strCompanyUrl not in self.dicParsedResultOfStartup:
                self.dicParsedResultOfStartup[strCompanyUrl] = {}
            #strCompany
            strCompany = self.cmUtility.extractFirstInList(lstSource=dicCompanyPageRawData.get("cc-company", []))
            self.dicParsedResultOfStartup[strCompanyUrl]["strCompany"] = strCompany
            #strUrl
            self.dicParsedResultOfStartup[strCompanyUrl]["strUrl"] = strCompanyUrl
            #strCrawlTime
            strCrawlTime = self.cmUtility.getCtimeOfFile(strFilePath=strCompanyFilePath)
            self.dicParsedResultOfStartup[strCompanyUrl]["strCrawlTime"] = strCrawlTime
            #lstStrFounders
            lstStrFounders = dicCompanyPageRawData.get("cc-company-founders", [])
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrFounders"] = lstStrFounders
            #strIntro
            lstStrIntro = dicCompanyPageRawData.get("cc-company-intro", [])
            self.dicParsedResultOfStartup[strCompanyUrl]["strIntro"] = u" ".join(lstStrIntro)
            """
            #lstStrProduct
            lstStrProduct = dicCompanyPageRawData.get("cb-lstStrProduct", [])
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrProduct"] = lstStrProduct
            """
            #lstIndustry
            lstIndustry = dicCompanyPageRawData.get("cc-Industry", [])
            self.dicParsedResultOfStartup[strCompanyUrl]["lstIndustry"] = lstIndustry
            #strLocation
            lstStrLocation = dicCompanyPageRawData.get("cc-Location", [])
            strLocation = u" ".join(lstStrLocation[0:-1])
            strLocation = re.sub("[\s]+", " ", strLocation).strip()
            self.dicParsedResultOfStartup[strCompanyUrl]["strLocation"] = strLocation
            #strCity
            strAddress = None
            if strLocation and strLocation != u"":
                (strAddress, fLatitude, fLongitude) = self.cameoUtility.geopyGeocode(strOriginLocation=strLocation)
            else:
                pass
            self.dicParsedResultOfStartup[strCompanyUrl]["strCity"] = strAddress
            #strCountry
            strOriginCountry = None
            if strAddress:
                strOriginCountry = strAddress.split(u",")[-1].strip()
            self.dicParsedResultOfStartup[strCompanyUrl]["strCountry"] = self.cameoUtility.getCountryCode(strCountryName=strOriginCountry)
            #strContinent
            self.dicParsedResultOfStartup[strCompanyUrl]["strContinent"] = self.cameoUtility.getContinentByCountryNameWikiVersion(strCountryName=strOriginCountry)
            #lstDicSeries
            lstDicSeries = []
            lstStrSeriesDate = dicCompanyPageRawData.get("cc-SeriesDate", [])
            for intSeriesIndex in range(len(lstStrSeriesDate)):
                dicSeries = {}
                #intSeriesValuation
                dicSeries.setdefault("intSeriesValuation", 0)
                #intSeriesMoney
                lstStrSeriesMoney = dicCompanyPageRawData.get("cc-SeriesMoney", [])
                if len(lstStrSeriesMoney) >= intSeriesIndex:
                    dicSeries.setdefault("intSeriesMoney", self.parseCrowdcubeMoney(strOriginMoney=lstStrSeriesMoney[intSeriesIndex]))
                else:
                    dicSeries.setdefault("intSeriesMoney", 0)
                #lstStrInvestorUrl
                dicSeries.setdefault("lstStrInvestorUrl", [])
                #strDate
                lstStrSeriesDate = dicCompanyPageRawData.get("cc-SeriesDate", [])
                if len(lstStrSeriesDate) >= intSeriesIndex:
                    dicSeries.setdefault("strDate", self.cameoUtility.parseStrDateByDateparser(strOriginDate=lstStrSeriesDate[intSeriesIndex]))
                else:
                    dicSeries.setdefault("strDate", "")
                #strSeriesType
                dicSeries.setdefault("strSeriesType", "")
                #lstStrInvestor
                dicSeries.setdefault("lstStrInvestor", [])
                #strCurrency
                dicSeries.setdefault("strCurrency", "GBP")
                #strCrawlTime
                dicSeries.setdefault("strCrawlTime", strCrawlTime)
                lstDicSeries.append(dicSeries)
            self.dicParsedResultOfStartup[strCompanyUrl]["lstDicSeries"] = lstDicSeries
            #lstStrFollowers (無此資料)
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrFollowers"] = []
            #isFundraising (需定義問題)
            self.dicParsedResultOfStartup[strCompanyUrl]["isFundraising"] = True
            #lstStrFoundersDesc (無此資料)
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrFoundersDesc"] = []
            #intRaisedMoney
            self.dicParsedResultOfStartup[strCompanyUrl]["intRaisedMoney"] = 0
            #intRaisedMoneyInTWD
            self.dicParsedResultOfStartup[strCompanyUrl]["intRaisedMoneyInTWD"] = 0
            #lstStrTierTagId
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrTierTagId"] = []
            #lstStrNewSubCategoryId
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrNewSubCategoryId"] = []
            #lstStrNewCategoryId
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrNewCategoryId"] = []
            #lstStrTopic (無此資料)
            #intFollower (無此資料)
            #lstStrTeam
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrTeam"] = []
            #lstStrTeamDesc
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrTeamDesc"] = []
            #lstStrInvestor
            self.dicParsedResultOfStartup[strCompanyUrl]["lstStrInvestor"] = []
            
    #解析 crowdcube 金額的數字
    def parseCrowdcubeMoney(self, strOriginMoney=None):
        intDefaultMoney = 0
        if not strOriginMoney or not re.search("[\d\.]+", strOriginMoney):
            return intDefaultMoney
        else:
            intParsedMoney = 0
            mMoneyWithK = re.search("([\d\.]+)k", strOriginMoney)
            mMoneyWithM = re.search("([\d\.]+)M", strOriginMoney)
            mMoneyWithB = re.search("([\d\.]+)B", strOriginMoney)
            if mMoneyWithK:
                intParsedMoney = int(float(mMoneyWithK.group(1)) * 1000)
            if mMoneyWithM:
                intParsedMoney = int(float(mMoneyWithM.group(1)) * 1000000)
            if mMoneyWithB:
                intParsedMoney = int(float(mMoneyWithB.group(1)) * 1000000000)
            return intParsedMoney
        
    #將 startup convert 結果寫入 startup.json
    def flushConvertedStartupDataToJsonFile(self, strJsonFilePath=None):
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfStartup, strJsonFilePath=strJsonFilePath)
        self.dicParsedResultOfStartup = {}