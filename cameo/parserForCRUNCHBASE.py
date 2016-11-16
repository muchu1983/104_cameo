# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import datetime
import re
import json
import logging
from scrapy import Selector
from cameo.utility import Utility
from cameo.localdb import LocalDbForCRUNCHBASE
from crawlermaster.cmparser import CmParser
from cameo.cmConverter.converterForCRUNCHBASE import ConverterForCRUNCHBASE
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForCRUNCHBASE:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = LocalDbForCRUNCHBASE()
        self.dicSubCommandHandler = {
            "search_funding_rounds":[self.parseSearchFundingRoundsPage],
            "search_investors":[self.parseSearchInvestorsPage],
            "organization":[self.parseOrganizationPage],
            "cb_companies.csv":[self.parseCompaniesCsv]
        }
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfStartup = {} #startup.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return ("- CRUNCHBASE -\n"
                "useage:\n"
                "search_funding_rounds - parse funding_rounds.html then insert organization url to localdb \n"
                "search_investors - parse investors.html then insert organization url to localdb \n"
                "organization - parse organization.html then create .json \n"
                "cb_companies.csv - parse cb_companies.csv then insert organization url to localdb \n"
                )

    #執行 parser
    def runParser(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)
#funding rounds #####################################################################################
    #解析 funding_rounds.html
    def parseSearchFundingRoundsPage(self, uselessArg1=None):
        strFundingRoundsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        lstStrFundingRoundsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strFundingRoundsHtmlFolderPath, strSuffixes="funding_rounds.html")
        strFundingRoundsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        if not os.path.exists(strFundingRoundsResultFolderPath):
            os.mkdir(strFundingRoundsResultFolderPath) #mkdir parsed_result/CRUNCHBASE/
        for strFundingRoundsHtmlFilePath in lstStrFundingRoundsHtmlFilePath:
            with open(strFundingRoundsHtmlFilePath, "r") as fundingRoundsHtmlFile:
                strPageSource = fundingRoundsHtmlFile.read()
            root = Selector(text=strPageSource)
            lstStrOrganizationUrl = root.css("div.cbRow div.cbCell:nth-of-type(3) span.identifier a.cb-link::attr(href)").extract()
            for strOrganizationUrl in lstStrOrganizationUrl:
                self.db.insertOrganizationUrlIfNotExists(strOrganizationUrl=strOrganizationUrl)
#investors #####################################################################################
    #解析 investors.html
    def parseSearchInvestorsPage(self, uselessArg1=None):
        strInvestorsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        lstStrInvestorsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strInvestorsHtmlFolderPath, strSuffixes="investors.html")
        strInvestorsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        if not os.path.exists(strInvestorsResultFolderPath):
            os.mkdir(strInvestorsResultFolderPath) #mkdir parsed_result/CRUNCHBASE/
        for strInvestorsHtmlFilePath in lstStrInvestorsHtmlFilePath:
            with open(strInvestorsHtmlFilePath, "r") as investorsHtmlFile:
                strPageSource = investorsHtmlFile.read()
            root = Selector(text=strPageSource)
            lstStrOrganizationUrl = root.css("TODO").extract()
            for strOrganizationUrl in lstStrOrganizationUrl:
                self.db.insertOrganizationUrlIfNotExists(strOrganizationUrl=strOrganizationUrl)
#organization #####################################################################################
    #解析 organization.html
    def parseOrganizationPage(self, uselessArg1=None):
        strOrganizationResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\CRUNCHBASE\\organization"
        strOrganizationHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CRUNCHBASE\\organization"
        if not os.path.exists(strOrganizationResultFolderPath):
            os.mkdir(strOrganizationResultFolderPath) #mkdir parsed_result/CRUNCHBASE/organization/
        #organization.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\crunchbase_organization.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        rawDataConverter = ConverterForCRUNCHBASE()
        lstDicOrganizationPageRawData = cmParser.localHtmlFileParse(
            strBasedir=strOrganizationHtmlFolderPath,
            strSuffixes="_organization.html",
            isIterable=True,
            isResetIteration=True
        )
        #convert
        intStartupJsonIndex = 1
        while len(lstDicOrganizationPageRawData)>0:
            strStartupJsonFilePath = strOrganizationResultFolderPath + u"\\%d_startup.json"%(intStartupJsonIndex*1000)
            rawDataConverter.convertStartup(lstLstDicRawData=[lstDicOrganizationPageRawData])
            rawDataConverter.flushConvertedStartupDataToJsonFile(strJsonFilePath=strStartupJsonFilePath)
            intStartupJsonIndex = intStartupJsonIndex+1
            lstDicOrganizationPageRawData = cmParser.localHtmlFileParse(
                strBasedir=strOrganizationHtmlFolderPath,
                strSuffixes="_organization.html",
                isIterable=True
            )
        
#CB_companies.csv ##################################################################################
    #解析 CB_companies.csv
    def parseCompaniesCsv(self, uselessArg1=None):
        strCompaniesCsvFilePath = u"cameo_res\\CB_companies.csv"
        with open(strCompaniesCsvFilePath, "r") as companiesCsvFile:
            for strCompanyUrlLine in companiesCsvFile:
                lstStrCompanyUrlLine = strCompanyUrlLine.split(",")
                if lstStrCompanyUrlLine[0] == "Mark":
                    strOrganizationUrl = lstStrCompanyUrlLine[1]
                    self.db.insertOrganizationUrlIfNotExists(strOrganizationUrl=strOrganizationUrl)