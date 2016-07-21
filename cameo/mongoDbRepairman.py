# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import datetime
import json
import logging
import re
from cameo.utility import Utility
from cameo.externaldb import ExternalDbOfCameo
#from cameo.localdb import LocalDbForJsonImporter #測試用本地端 db
"""
mongoDB 維護工作
"""
class MongoDbRepairman:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = ExternalDbOfCameo().mongodb
        #self.db = LocalDbForJsonImporter().mongodb #測試用本地端 db
        
    def makeTagFieldOnModelFundProject(self):
        for docFundProject in self.db.ModelFundProject.find({}):
            lstStrTag = []
            strCategory = docFundProject["strCategory"]
            strSubCategory = docFundProject["strSubCategory"]
            lstStrCategory = docFundProject["lstStrCategory"]
            lstStrSubCategory = docFundProject["lstStrSubCategory"]
            lstStrTag.append(strCategory)
            lstStrTag.append(strSubCategory)
            lstStrTag = lstStrTag + lstStrCategory
            lstStrTag = lstStrTag + lstStrSubCategory
            lstStrTag = list(set(lstStrTag))
            self.db.ModelFundProject.update_one(
                {
                    "_id":docFundProject["_id"]
                },
                {
                    "$set":{
                        "lstStrTag":lstStrTag
                    }
                },
                upsert=True
            )
        
    def makeTagFieldOnModelStartup(self):
        for docStartup in self.db.ModelStartup.find({}):
            lstStrTag = []
            lstIndustry = docStartup["lstIndustry"]
            lstStrCategory = docStartup["lstStrCategory"]
            lstStrSubCategory = docStartup["lstStrSubCategory"]
            lstStrTag = lstStrTag + lstIndustry
            lstStrTag = lstStrTag + lstStrCategory
            lstStrTag = lstStrTag + lstStrSubCategory
            lstStrTag = list(set(lstStrTag))
            self.db.ModelStartup.update_one(
                {
                    "_id":docStartup["_id"]
                },
                {
                    "$set":{
                        "lstStrTag":lstStrTag
                    }
                },
                upsert=True
            )
        
    def removeModelStartupInvestorAndModelRewardPersonUnnecessaryData(self):
        #投資型
        for docStartupInvestor in self.db.ModelStartupInvestor.find({}):
            strUrl = docStartupInvestor["strUrl"]
            if strUrl:
                if strUrl.startswith("https://angel.co/"):
                    continue
                else:
                    self.db.ModelStartupInvestor.delete_one({"strUrl":strUrl})
                    logging.info("delete: %s"%strUrl)
        #回饋型
        for docRewardPerson in self.db.ModelRewardPerson.find({}):
            strUrl = docRewardPerson["strUrl"]
            if strUrl:
                if strUrl.startswith("https://angel.co/"):
                    self.db.ModelRewardPerson.delete_one({"strUrl":strUrl})
                    logging.info("delete: %s"%strUrl)
                else:
                    continue
                    
    #find null strCurrency and replace it with ""
    def replaceNullStrCurrencyToEmptyString(self):
        for docFundProject in self.db.ModelFundProject.find({"strSource":"INDIEGOGO"}): #所有專案 INDIEGOGO loop
            if not docFundProject["strCurrency"]: #strCurrency 為 null
                docFundProject["strCurrency"] = ""
                logging.info("replace strCurrency null by empty string: [_id:%s]"%docFundProject["_id"])
                self.db.ModelFundProject.update_one(
                    {
                        "_id":docFundProject["_id"]
                    },
                    {
                        "$set":docFundProject,
                    },
                    upsert=True
                )
        
    #make view ViewStartupAndInvestment
    def makeViewStartupAndInvestment(self):
        self.db.ViewStartupAndInvestment.remove({})
        for docSyndicate in self.db.ModelSyndicate.find({}): #所有投資人 loop
            lstDicInvestment = docSyndicate.get("lstDicInvestment", None)
            if lstDicInvestment: #投資項目資料
                for dicInvestment in lstDicInvestment:
                    strCompanyName = dicInvestment.get("strCompanyName", None)
                    strName = dicInvestment.get("strName", None)
                    intYear = dicInvestment.get("intYear", None)
                    #新創團隊資料
                    docInvestmentStartup = self.db.ModelStartup.find_one({"strCompany":strCompanyName}) #欄位名稱是 strCompany 而不是 strCompanyName
                    if docInvestmentStartup: #檢查新創團隊資料
                        #upsert 所有資料
                        logging.info("upsert ViewStartupAndInvestment")
                        self.db.ViewStartupAndInvestment.update_one(
                            {
                                "strName":strName,
                                "strCompanyName":strCompanyName,
                                "intYear":intYear
                            },
                            {
                                "$set":{
                                    #投資項目資料
                                    "strName":strName,
                                    "strCompanyName":strCompanyName,
                                    "intYear":intYear,
                                    #新創團隊資料 (without strCompanyName)
                                    "lstDicSeries":docInvestmentStartup.get("lstDicSeries", None),
                                    "lstIndustry":docInvestmentStartup.get("lstIndustry", None),
                                    "lstIntCategoryId":docInvestmentStartup.get("lstIntCategoryId", None),
                                    "lstStrProduct":docInvestmentStartup.get("lstStrProduct", None),
                                    "lstIntSubCategoryId":docInvestmentStartup.get("lstIntSubCategoryId", None),
                                    "lstStrFollowers":docInvestmentStartup.get("lstStrFollowers", None),
                                    "lstStrSubCategory":docInvestmentStartup.get("lstStrSubCategory", None),
                                    "strStartupSource":docInvestmentStartup.get("strSource", None),#與syndicate重覆，加入 Startup 辨別
                                    "strStartupCrawlTime":docInvestmentStartup.get("strCrawlTime", None),#與syndicate重覆，加入 Startup 辨別
                                    "strCountry":docInvestmentStartup.get("strCountry", None),
                                    "strIntro":docInvestmentStartup.get("strIntro", None),
                                    "strContinent":docInvestmentStartup.get("strContinent", None),
                                    "lstStrInvestor":docInvestmentStartup.get("lstStrInvestor", None),
                                    "lstDicPress":docInvestmentStartup.get("lstDicPress", None),
                                    "lstStrFounders":docInvestmentStartup.get("lstStrFounders", None),
                                    "lstStrFoundersUrl":docInvestmentStartup.get("lstStrFoundersUrl", None),
                                    "lstStrFoundersDesc":docInvestmentStartup.get("lstStrFoundersDesc", None),
                                    "lstStrTeam":docInvestmentStartup.get("lstStrTeam", None),
                                    "isFundraising":docInvestmentStartup.get("isFundraising", None),
                                    "lstStrTeamDesc":docInvestmentStartup.get("lstStrTeamDesc", None),
                                    "strStartupUrl":docInvestmentStartup.get("strUrl", None),#與syndicate重覆，加入 Startup 辨別
                                    "strLocation":docInvestmentStartup.get("strLocation", None),
                                    "strCity":docInvestmentStartup.get("strCity", None),
                                    "strProduct":docInvestmentStartup.get("strProduct", None),
                                    "lstStrCategory":docInvestmentStartup.get("lstStrCategory", None),
                                }
                            },
                            upsert=True
                        )
                else:
                    logging.warning("docInvestmentStartup is None")
        else:
            logging.warning("lstDicInvestment is None")
            
    #make view ViewStartupAndSeries
    def makeViewStartupAndSeries(self):
        self.db.ViewStartupAndSeries.remove({})
        for docStartup in self.db.ModelStartup.find({}): #所有新創團隊 loop
            strCompanyName = docStartup.get("strCompany", None)
            lstDicSeries = docStartup.get("lstDicSeries", []) 
            if lstDicSeries: #投資階段資料
                for dicSeries in lstDicSeries:
                    intSeriesValuation = dicSeries.get("intSeriesValuation", None)
                    intSeriesMoney = dicSeries.get("intSeriesMoney", None)
                    lstStrSeriesInvestor = dicSeries.get("lstStrInvestor", [])
                    strSeriesDate = dicSeries.get("strDate", None)
                    strSeriesType = dicSeries.get("strSeriesType", None)
                    lstStrSeriesInvestorUrl = dicSeries.get("lstStrInvestorUrl", [])
                    strSeriesCurrency = dicSeries.get("strCurrency", None)
                    strSeriesCrawlTime = dicSeries.get("strCrawlTime", None)
                    #upsert 所有資料
                    logging.info("upsert ViewStartupAndSeries")
                    self.db.ViewStartupAndSeries.update_one(
                        {
                            "strCompanyName":strCompanyName,
                            "intSeriesValuation":intSeriesValuation,
                            "intSeriesMoney":intSeriesMoney,
                            "lstStrSeriesInvestor":lstStrSeriesInvestor,
                            "strSeriesDate":strSeriesDate,
                            "strSeriesType":strSeriesType,
                            "lstStrSeriesInvestorUrl":lstStrSeriesInvestorUrl,
                            "strSeriesCurrency":strSeriesCurrency,
                            "strSeriesCrawlTime":strSeriesCrawlTime
                        },
                        {
                            "$set":{
                                #投資階段資料
                                "intSeriesValuation":intSeriesValuation,
                                "intSeriesMoney":intSeriesMoney,
                                "lstStrSeriesInvestor":lstStrSeriesInvestor,
                                "strSeriesDate":strSeriesDate,
                                "strSeriesType":strSeriesType,
                                "lstStrSeriesInvestorUrl":lstStrSeriesInvestorUrl,
                                "strSeriesCurrency":strSeriesCurrency,
                                "strSeriesCrawlTime":strSeriesCrawlTime,
                                #新創團隊資料
                                "strCompanyName":docStartup.get("strCompany", None),
                                "lstDicSeries":docStartup.get("lstDicSeries", None),
                                "lstIndustry":docStartup.get("lstIndustry", None),
                                "lstIntCategoryId":docStartup.get("lstIntCategoryId", None),
                                "lstStrProduct":docStartup.get("lstStrProduct", None),
                                "lstIntSubCategoryId":docStartup.get("lstIntSubCategoryId", None),
                                "lstStrFollowers":docStartup.get("lstStrFollowers", None),
                                "lstStrSubCategory":docStartup.get("lstStrSubCategory", None),
                                "strStartupSource":docStartup.get("strSource", None),#與syndicate重覆，加入 Startup 辨別
                                "strStartupCrawlTime":docStartup.get("strCrawlTime", None),#與syndicate重覆，加入 Startup 辨別
                                "strCountry":docStartup.get("strCountry", None),
                                "strIntro":docStartup.get("strIntro", None),
                                "strContinent":docStartup.get("strContinent", None),
                                "lstStrInvestor":docStartup.get("lstStrInvestor", None),
                                "lstDicPress":docStartup.get("lstDicPress", None),
                                "lstStrFounders":docStartup.get("lstStrFounders", None),
                                "lstStrFoundersUrl":docStartup.get("lstStrFoundersUrl", None),
                                "lstStrFoundersDesc":docStartup.get("lstStrFoundersDesc", None),
                                "lstStrTeam":docStartup.get("lstStrTeam", None),
                                "isFundraising":docStartup.get("isFundraising", None),
                                "lstStrTeamDesc":docStartup.get("lstStrTeamDesc", None),
                                "strStartupUrl":docStartup.get("strUrl", None),#與syndicate重覆，加入 Startup 辨別
                                "strLocation":docStartup.get("strLocation", None),
                                "strCity":docStartup.get("strCity", None),
                                "strProduct":docStartup.get("strProduct", None),
                                "lstStrCategory":docStartup.get("lstStrCategory", None),
                            }
                        },
                        upsert=True
                    )
            else:
                logging.warning("lstDicSeries is None")

    #make view ViewSyndicateAndStartup
    def makeViewSyndicateAndStartup(self):
        self.db.ViewSyndicateAndStartup.remove({})
        for docSyndicate in self.db.ModelSyndicate.find({}): #所有投資人 loop
            lstDicInvestment = docSyndicate.get("lstDicInvestment", None)
            if lstDicInvestment: #投資項目資料
                for dicInvestment in lstDicInvestment:
                    strCompanyName = dicInvestment.get("strCompanyName", None)
                    strName = dicInvestment.get("strName", None)
                    intYear = dicInvestment.get("intYear", None)
                    #投資人資料
                    logging.info("find syndicate with strName:%s"%strName)
                    docInvestmentSyndicate = self.db.ModelSyndicate.find_one({"strName":strName})
                    #新創團隊資料
                    logging.info("find startup with strCompanyName:%s"%strCompanyName)
                    docInvestmentStartup = self.db.ModelStartup.find_one({"strCompany":strCompanyName}) #欄位名稱是 strCompany 而不是 strCompanyName
                    if docInvestmentSyndicate and docInvestmentStartup: #檢查投資人與新創團隊資料
                        #投資階段資料
                        lstDicSeries = docInvestmentStartup.get("lstDicSeries", []) 
                        for dicSeries in lstDicSeries:
                            intSeriesValuation = dicSeries.get("intSeriesValuation", None)
                            intSeriesMoney = dicSeries.get("intSeriesMoney", None)
                            lstStrSeriesInvestor = dicSeries.get("lstStrInvestor", [])
                            strSeriesDate = dicSeries.get("strDate", None)
                            strSeriesType = dicSeries.get("strSeriesType", None)
                            lstStrSeriesInvestorUrl = dicSeries.get("lstStrInvestorUrl", [])
                            strSeriesCurrency = dicSeries.get("strCurrency", None)
                            strSeriesCrawlTime = dicSeries.get("strCrawlTime", None)
                            #upsert 所有資料
                            logging.info("upsert ViewSyndicateAndStartup with key (strName,strCompanyName):(%s,%s)"%(strName,strCompanyName))
                            self.db.ViewSyndicateAndStartup.update_one(
                                {
                                    "strName":strName,
                                    "strCompanyName":strCompanyName
                                },
                                {
                                    "$set":{
                                        #投資項目資料
                                        "strName":strName,
                                        "strCompanyName":strCompanyName,
                                        "intYear":intYear,
                                        #投資階段資料
                                        "intSeriesValuation":intSeriesValuation,
                                        "intSeriesMoney":intSeriesMoney,
                                        "lstStrSeriesInvestor":lstStrSeriesInvestor,
                                        "strSeriesDate":strSeriesDate,
                                        "strSeriesType":strSeriesType,
                                        "lstStrSeriesInvestorUrl":lstStrSeriesInvestorUrl,
                                        "strSeriesCurrency":strSeriesCurrency,
                                        "strSeriesCrawlTime":strSeriesCrawlTime,
                                        #投資人資料 (without strName)
                                        "lstDicInvestment":docSyndicate.get("lstDicInvestment", None),
                                        "lstStrManagerUrl":docInvestmentSyndicate.get("lstStrManagerUrl", None),
                                        "intTypicalInvestment":docInvestmentSyndicate.get("intTypicalInvestment", None),
                                        "fCarryPerDeal":docInvestmentSyndicate.get("fCarryPerDeal", None),
                                        "intDealsPerYear":docInvestmentSyndicate.get("intDealsPerYear", None),
                                        "strSource":docInvestmentSyndicate.get("strSource", None),
                                        "lstStrBackers":docInvestmentSyndicate.get("lstStrBackers", None),
                                        "strUrl":docInvestmentSyndicate.get("strUrl", None),
                                        "intBackedBy":docInvestmentSyndicate.get("intBackedBy", None),
                                        "strCurrency":docInvestmentSyndicate.get("strCurrency", None),
                                        "strCrawlTime":docInvestmentSyndicate.get("strCrawlTime", None),
                                        "intBackerCount":docInvestmentSyndicate.get("intBackerCount", None),
                                        "strManager":docInvestmentSyndicate.get("strManager", None),
                                        "strTypicalInvestment":docInvestmentSyndicate.get("strTypicalInvestment", None),
                                        #新創團隊資料 (without strCompanyName)
                                        "lstDicSeries":docInvestmentStartup.get("lstDicSeries", None),
                                        "lstIndustry":docInvestmentStartup.get("lstIndustry", None),
                                        "lstIntCategoryId":docInvestmentStartup.get("lstIntCategoryId", None),
                                        "lstStrProduct":docInvestmentStartup.get("lstStrProduct", None),
                                        "lstIntSubCategoryId":docInvestmentStartup.get("lstIntSubCategoryId", None),
                                        "lstStrFollowers":docInvestmentStartup.get("lstStrFollowers", None),
                                        "lstStrSubCategory":docInvestmentStartup.get("lstStrSubCategory", None),
                                        "strStartupSource":docInvestmentStartup.get("strSource", None),#與syndicate重覆，加入 Startup 辨別
                                        "strStartupCrawlTime":docInvestmentStartup.get("strCrawlTime", None),#與syndicate重覆，加入 Startup 辨別
                                        "strCountry":docInvestmentStartup.get("strCountry", None),
                                        "strIntro":docInvestmentStartup.get("strIntro", None),
                                        "strContinent":docInvestmentStartup.get("strContinent", None),
                                        "lstStrInvestor":docInvestmentStartup.get("lstStrInvestor", None),
                                        "lstDicPress":docInvestmentStartup.get("lstDicPress", None),
                                        "lstStrFounders":docInvestmentStartup.get("lstStrFounders", None),
                                        "lstStrFoundersUrl":docInvestmentStartup.get("lstStrFoundersUrl", None),
                                        "lstStrFoundersDesc":docInvestmentStartup.get("lstStrFoundersDesc", None),
                                        "lstStrTeam":docInvestmentStartup.get("lstStrTeam", None),
                                        "isFundraising":docInvestmentStartup.get("isFundraising", None),
                                        "lstStrTeamDesc":docInvestmentStartup.get("lstStrTeamDesc", None),
                                        "strStartupUrl":docInvestmentStartup.get("strUrl", None),#與syndicate重覆，加入 Startup 辨別
                                        "strLocation":docInvestmentStartup.get("strLocation", None),
                                        "strCity":docInvestmentStartup.get("strCity", None),
                                        "strProduct":docInvestmentStartup.get("strProduct", None),
                                        "lstStrCategory":docInvestmentStartup.get("lstStrCategory", None),
                                    }
                                },
                                upsert=True
                            )
                    else:
                        if not docInvestmentSyndicate:
                            logging.warning("docInvestmentSyndicate is None")
                        if not docInvestmentStartup:
                            logging.warning("docInvestmentStartup is None")
            else:
                logging.warning("lstDicInvestment is None")