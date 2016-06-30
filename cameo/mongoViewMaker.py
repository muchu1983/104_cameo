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
建立 mongoDB 的 View 資料表
"""
class MongoViewMaker:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = ExternalDbOfCameo().mongodb
        #self.db = LocalDbForJsonImporter().mongodb #測試用本地端 db
        
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

