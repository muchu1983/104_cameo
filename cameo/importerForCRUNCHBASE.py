#coding: utf-8
import os
import sys
import time
import datetime
import dateparser
import math
import re
import logging
from cameo.utility import Utility
from cameo.externaldb import ExternalDbForJsonImporter
#from cameo.localdb import LocalDbForJsonImporter #測試用本地端 db

class ImporterForCRUNCHBASE:
    
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = ExternalDbForJsonImporter().mongodb
        #self.db = LocalDbForJsonImporter().mongodb #測試用本地端 db
        self.dicSubCommandHandler = {"import":[self.importJsonData]}
        
    #取得 importer 使用資訊
    def getUseageMessage(self):
        return (
            "- CRUNCHBASE -\n"
            "useage:\n"
            "import - import json to database \n"
        )
        
    #執行 importer
    def runImporter(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)
            
    #匯入所有 json 進入點
    def importJsonData(self, uselessArg1=None):
        self.importStartupJson()
    
    #匯入 startup.json
    def importStartupJson(self):
        for strStartupJsonFilePath in self.getParsedStartupFilePath():
            logging.info("import: %s"%strStartupJsonFilePath)
            dicTotalStartup = self.utility.readObjectFromJsonFile(strJsonFilePath=strStartupJsonFilePath)
            collectionStartup = self.db.ModelStartup
            for strUrl, dicStartup in dicTotalStartup.items():
                #strSource
                dicStartup.setdefault("strSource", "CRUNCHBASE")
                #strCrawlTime
                dicStartup["strCrawlTime"] = self.getCorrectFormatDateTime(dicStartup.get("strCrawlTime"))
                #lstIntCategoryId
                dicStartup.setdefault("lstIntCategoryId", [])
                #lstStrCategory
                dicStartup.setdefault("lstStrCategory", [])
                #lstIntSubCategoryId
                dicStartup.setdefault("lstIntSubCategoryId", [])
                #lstStrSubCategory
                dicStartup.setdefault("lstStrSubCategory", [])
                #lstDicPress
                dicStartup.setdefault("lstDicPress", [])
                #lstDicSeries
                lstDicSeries = []
                for dicSeries in dicStartup.get("lstDicSeries", []):
                    dicSeries["strCrawlTime"] = self.getCorrectFormatDateTime(dicSeries.get("strCrawlTime"))
                    dicSeries["strDate"] = self.getCorrectFormatDateTime(dicSeries.get("strDate"))
                    lstDicSeries.append(dicSeries)
                dicStartup["lstDicSeries"] = lstDicSeries
                #upsert startup
                collectionStartup.update_one(
                    {"strUrl": strUrl},
                    {
                        "$set":dicStartup
                    },
                    upsert=True
                )
                #lstStrTag
                lstStrTag = self.makeTagFieldOnModelStartup(
                    dicStartup.get("lstIndustry", []),
                    dicStartup.get("lstStrCategory", []),
                    dicStartup.get("lstStrSubCategory", [])
                )
                collectionStartup.update_one(
                    {"strUrl": strUrl},
                    {
                        "$set":{
                            "lstStrTag":lstStrTag
                        }
                    },
                    upsert=True
                )
                #領投人資料表 ModelSyndicateCrunchbase
                collectionSyndicateCrunchbase = self.db.ModelSyndicateCrunchbase
                for dicSeries in dicStartup.get("lstDicSeries", []):
                    lstStrInvestorUrl = dicSeries.get("lstStrInvestorUrl", [])
                    lstStrInvestor = dicSeries.get("lstStrInvestor", [])
                    lstStrLeadInvestor = dicSeries.get("lstStrLeadInvestor", [])
                    strCrawlTime = dicSeries.get("strCrawlTime", "")
                    if len(lstStrInvestorUrl) == len(lstStrInvestor): #檢查 investor 列表與 investor url 列表是否一致
                        for intIndexOfLstStrInvestorUrl in range(len(lstStrInvestorUrl)):
                            strInvestor = lstStrInvestor[intIndexOfLstStrInvestorUrl]
                            #檢查是否為領投人之一
                            if strInvestor in lstStrLeadInvestor:
                                strLeadInvestorUrl = lstStrInvestorUrl[intIndexOfLstStrInvestorUrl]
                                #投資資訊
                                dicInvestment = {
                                    "campanyName":dicStartup.get("strCompany", None),
                                    "series":dicSeries.get("strSeriesType", None),
                                    "lstStrBackers":lstStrInvestor
                                }
                                collectionSyndicateCrunchbase.update_one(
                                    {"strUrl": strLeadInvestorUrl},
                                    {
                                        "$set":{
                                            "strName":strInvestor,
                                            "strCrawTime":dicSeries.get("strCrawlTime", None),
                                            "dicInvestment":dicInvestment
                                        }
                                    },
                                    upsert=True
                                )
                                """
                strUrl:領投人的網址
                strName:名稱
                strCrawTime:抓取時間
                lstStrBackers:{
                    campanyName:"Airbnb"
                    series:"a輪"
                    lstStrBackers: {
                        backerA
                        backerB
                        ...
                    }  
                }
                            """
                            
    #建立 lstStrTag 欄位內容
    def makeTagFieldOnModelStartup(self, lstIndustry, lstStrCategory, lstStrSubCategory):
        lstStrTag = []
        lstStrTag = lstStrTag + lstIndustry
        lstStrTag = lstStrTag + lstStrCategory
        lstStrTag = lstStrTag + lstStrSubCategory
        lstStrTag = list(set(lstStrTag))
        return lstStrTag
    
    #取得 json 檔案根目錄
    def strParsedResultPath(self):
        return u"cameo_res/parsed_result/CRUNCHBASE"
    
    #取得 startup.json 檔案位置
    def getParsedStartupFilePath(self):
        return self.utility.getFilePathListWithSuffixes(strBasedir=self.strParsedResultPath() + "\\organization", strSuffixes="startup.json")
    
    #修改日期格式
    def getCorrectFormatDateTime(self, strDate):
        return datetime.datetime.strptime(strDate, "%Y-%m-%d").strftime("%Y/%m/%d")
    
