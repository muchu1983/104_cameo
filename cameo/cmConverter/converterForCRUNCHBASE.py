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

class ConverterForCRUNCHBASE:
    
    #建構子
    def __init__(self):
        self.cmUtility = CmUtility()
        self.cameoUtility = CameoUtility()
        self.dicParsedResultOfStartup = {} #startup.json 資料
        
    #轉換 startup 資訊
    def convertStartup(self, lstLstDicRawData=[]):
        #_organization.html raw data
        lstDicOrganizationPageRawData = lstLstDicRawData[0]
        for dicOrganizationPageRawData in lstDicOrganizationPageRawData:
            strOrganizationHtmlFilePath = dicOrganizationPageRawData.get("meta-data-html-filepath", None)
            logging.info("convert: %s"%strOrganizationHtmlFilePath)
            strOrganizationId = re.search("^.*\\\\(.*)_organization.html$", strOrganizationHtmlFilePath).group(1)
            strOrganizationUrl = u"https://www.crunchbase.com/organization/" + strOrganizationId
            #檢查 資料是否有誤
            lstCompanyData = dicOrganizationPageRawData.get("cb-strCompany", [])
            lstLocationData = dicOrganizationPageRawData.get("cb-strLocation", [])
            if lstCompanyData == [] or lstLocationData == []:
                #錯誤資料 刪除 html 檔並跳過
                os.remove(strOrganizationHtmlFilePath)
                continue
            #建立 dict
            if strOrganizationUrl not in self.dicParsedResultOfStartup:
                self.dicParsedResultOfStartup[strOrganizationUrl] = {}
            #strCompany
            strCompany = self.cmUtility.extractFirstInList(lstSource=dicOrganizationPageRawData.get("cb-strCompany", []))
            self.dicParsedResultOfStartup[strOrganizationUrl]["strCompany"] = strCompany
            #strUrl
            self.dicParsedResultOfStartup[strOrganizationUrl]["strUrl"] = strOrganizationUrl
            #strCrawlTime
            strCrawlTime = self.cmUtility.getCtimeOfFile(strFilePath=strOrganizationHtmlFilePath)
            self.dicParsedResultOfStartup[strOrganizationUrl]["strCrawlTime"] = strCrawlTime
            #lstStrFounders
            lstStrFounders = dicOrganizationPageRawData.get("cb-lstStrFounders", [])
            self.dicParsedResultOfStartup[strOrganizationUrl]["lstStrFounders"] = lstStrFounders
            #strIntro
            lstStrIntro = dicOrganizationPageRawData.get("cb-strIntro", [])
            self.dicParsedResultOfStartup[strOrganizationUrl]["strIntro"] = u" ".join(lstStrIntro)
            #lstStrTeam
            lstStrTeam = dicOrganizationPageRawData.get("cb-lstStrTeam", [])
            self.dicParsedResultOfStartup[strOrganizationUrl]["lstStrTeam"] = lstStrTeam
            #lstStrTeamDesc
            lstStrTeamDesc = dicOrganizationPageRawData.get("cb-lstStrTeamDesc", [])
            self.dicParsedResultOfStartup[strOrganizationUrl]["lstStrTeamDesc"] = lstStrTeamDesc
            #lstStrProduct
            lstStrProduct = dicOrganizationPageRawData.get("cb-lstStrProduct", [])
            self.dicParsedResultOfStartup[strOrganizationUrl]["lstStrProduct"] = lstStrProduct
            #lstIndustry
            lstIndustry = dicOrganizationPageRawData.get("cb-lstIndustry", [])
            self.dicParsedResultOfStartup[strOrganizationUrl]["lstIndustry"] = lstIndustry
            #strLocation
            lstStrLocation = dicOrganizationPageRawData.get("cb-strLocation", [])
            strLocation = u" ".join(lstStrLocation)
            self.dicParsedResultOfStartup[strOrganizationUrl]["strLocation"] = strLocation
            #strCity
            (strAddress, fLatitude, fLongitude) = self.cameoUtility.geopyGeocode(strOriginLocation=lstStrLocation[-1])
            self.dicParsedResultOfStartup[strOrganizationUrl]["strCity"] = strAddress
            #strCountry
            strOriginCountry = None
            if strAddress:
                strOriginCountry = strAddress.split(u",")[-1].strip()
            self.dicParsedResultOfStartup[strOrganizationUrl]["strCountry"] = self.cameoUtility.getCountryCode(strCountryName=strOriginCountry)
            #strContinent
            self.dicParsedResultOfStartup[strOrganizationUrl]["strContinent"] = self.cameoUtility.getContinentByCountryNameWikiVersion(strCountryName=strOriginCountry)
            #lstStrInvestor
            lstStrInvestor = dicOrganizationPageRawData.get("cb-lstStrInvestor", [])
            self.dicParsedResultOfStartup[strOrganizationUrl]["lstStrInvestor"] = lstStrInvestor
            #isFundraising (需定義問題)
            #lstStrTopic (無此資料)
            #lstStrFoundersDesc (無此資料)
            #lstStrFollowers (無此資料)
            #intFollower (無此資料)
            #lstDicSeries
            lstDicSeries = []
            lstStrSeriesDate = dicOrganizationPageRawData.get("cb-strSeriesDate", [])
            for intSeriesIndex in range(len(lstStrSeriesDate)):
                dicSeries = {}
                #intSeriesValuation
                lstStrSeriesValuation = dicOrganizationPageRawData.get("cb-intSeriesValuation", [])
                if len(lstStrSeriesValuation) >= intSeriesIndex:
                    dicSeries.setdefault("intSeriesValuation", self.parseCrunchbaseMoney(strOriginMoney=lstStrSeriesValuation[intSeriesIndex]))
                else:
                    dicSeries.setdefault("intSeriesValuation", 0)
                #intSeriesMoney
                lstStrSeriesMoney = dicOrganizationPageRawData.get("cb-intSeriesMoney", [])
                if len(lstStrSeriesMoney) >= intSeriesIndex:
                    dicSeries.setdefault("intSeriesMoney", self.parseCrunchbaseMoney(strOriginMoney=lstStrSeriesMoney[intSeriesIndex]))
                else:
                    dicSeries.setdefault("intSeriesMoney", 0)
                #lstStrInvestorUrl
                dicSeries.setdefault("lstStrInvestorUrl", dicOrganizationPageRawData.get("cb-lstStrInvestorUrl", []))
                #strDate
                lstStrSeriesDate = dicOrganizationPageRawData.get("cb-strSeriesDate", [])
                if len(lstStrSeriesDate) >= intSeriesIndex:
                    dicSeries.setdefault("strDate", self.cameoUtility.parseStrDateByDateparser(strOriginDate=lstStrSeriesDate[intSeriesIndex]))
                else:
                    dicSeries.setdefault("strDate", "")
                dicSeries.setdefault("strDate", )
                #strSeriesType
                lstStrSeriesType = dicOrganizationPageRawData.get("cb-strSeriesType", [])
                if len(lstStrSeriesType) >= intSeriesIndex:
                    dicSeries.setdefault("strSeriesType", lstStrSeriesType[intSeriesIndex])
                else:
                    dicSeries.setdefault("strSeriesType", "")
                #lstStrInvestor
                dicSeries.setdefault("lstStrInvestor", dicOrganizationPageRawData.get("cb-lstStrInvestor", []))
                #strCurrency
                dicSeries.setdefault("strCurrency", "USD")
                #strCrawlTime
                dicSeries.setdefault("strCrawlTime", strCrawlTime)
                lstDicSeries.append(dicSeries)
            self.dicParsedResultOfStartup[strOrganizationUrl]["lstDicSeries"] = lstDicSeries
            
    #解析 crunchbase 金額的數字
    def parseCrunchbaseMoney(self, strOriginMoney=None):
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