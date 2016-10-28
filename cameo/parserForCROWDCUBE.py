# -*- coding: utf-8 -*-
"""
Copyright (C) 2016, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import datetime
import re
import json
import logging
import urllib
from scrapy import Selector
from cameo.utility import Utility
from cameo.localdb import LocalDbForCROWDCUBE
from crawlermaster.cmparser import CmParser
from cameo.cmConverter.converterForCROWDCUBE import ConverterForCROWDCUBE
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForCROWDCUBE:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = LocalDbForCROWDCUBE()
        self.dicSubCommandHandler = {
            "companies":[self.parseCompaniesPage],
            "company":[self.parseCompanyPage]
        }
        self.strWebsiteDomain = u"https://www.crowdcube.com"
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfStartup = {} #startup.json 資料
        self.dicParsedResultOfStartupSeries = {} #startup_series.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return (
            "- CROWDCUBE -\n"
            "useage:\n"
            "companies - parse companies.html then insert company url into DB \n"
            "company - parse companies/*.html then create json \n"
        )
    
    #執行 parser
    def runParser(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)
    
    #解析 companies.html
    def parseCompaniesPage(self, uselessArg1=None):
        strCompaniesResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\CROWDCUBE"
        if not os.path.exists(strCompaniesResultFolderPath):
            os.mkdir(strCompaniesResultFolderPath) #mkdir parsed_result/CROWDCUBE/
        strCompaniesHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CROWDCUBE"
        strCompaniesHtmlFilePath = strCompaniesHtmlFolderPath + u"\\companies.html"
        with open(strCompaniesHtmlFilePath, "r") as companiesHtmlFile:
            strPageSource = companiesHtmlFile.read()
            root = Selector(text=strPageSource)
        lstStrCompanyPageUrl = root.css("div.cc-cardGrid__cell section.cc-card a::attr(href)").extract()
        for strCompanyPageUrl in lstStrCompanyPageUrl:
            if strCompanyPageUrl.startswith("/companies/"):
                strCompanyPageUrl = self.strWebsiteDomain + strCompanyPageUrl
                logging.info("insert company: %s"%strCompanyPageUrl)
                self.db.insertCompanyUrlIfNotExists(strCompanyUrl=strCompanyPageUrl)
                
    #解析 companies/*.html 產生 json
    def parseCompanyPage(self, uselessArg1=None):
        strCompanyResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\CROWDCUBE\\companies"
        strCompanyHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CROWDCUBE\\companies"
        if not os.path.exists(strCompanyResultFolderPath):
            os.mkdir(strCompanyResultFolderPath) #mkdir parsed_result/CROWDCUBE/companies/
        #company.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\crowdcube_company.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicCompanyPageRawData = cmParser.localHtmlFileParse(strBasedir=strCompanyHtmlFolderPath, strSuffixes="_company.html")
        #converter
        rawDataConverter = ConverterForCROWDCUBE()
        rawDataConverter.convertStartup(lstLstDicRawData=[lstDicCompanyPageRawData])
        strStartupJsonFilePath = strCompanyResultFolderPath + u"\\startup.json"
        rawDataConverter.flushConvertedStartupDataToJsonFile(strJsonFilePath=strStartupJsonFilePath)
        