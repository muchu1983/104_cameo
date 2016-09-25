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
            "company":[self.parseProjectPage]
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
                
    #解析 projects/*.html 產生 json (strCategoryPage1Url == None 會自動找尋已完成下載之 category)
    def parseProjectPage(self, strCategoryPage1Url=None):
        if strCategoryPage1Url is None:
            #未指定 category url
            #取得已下載完成的 strCategoryUrl list
            lstStrObtainedCategoryUrl = self.db.fetchallCompletedObtainedCategoryUrl()
            for strObtainedCategoryUrl in lstStrObtainedCategoryUrl: #category loop
                strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strObtainedCategoryUrl)
                self.parseProjectPageWithGivenCategory(strCategoryPage1Url=strObtainedCategoryUrl, strCategoryName=strCategoryName)
        else:
            #有指定 category url
            strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strCategoryPage1Url)
            self.parseProjectPageWithGivenCategory(strCategoryPage1Url=strCategoryPage1Url, strCategoryName=strCategoryName)
    
    #解析 指定 category 的 projects/*.html 產生 json 並 取得 funder url
    def parseProjectPageWithGivenCategory(self, strCategoryPage1Url=None, strCategoryName=None):
        strProjectResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\JD\\%s\\projects"%strCategoryName
        if not os.path.exists(strProjectResultFolderPath):
            os.mkdir(strProjectResultFolderPath) #mkdir parsed_result/JD/category/projects
        strProjectHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD\\%s\\projects"%strCategoryName
        #_intro.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\jd_main_page_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicIntroPageRawData = cmParser.localHtmlFileParse(strBasedir=strProjectHtmlFolderPath, strSuffixes="_intro.html")
        #_progress.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\jd_qa_update_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicProgressPageRawData = cmParser.localHtmlFileParse(strBasedir=strProjectHtmlFolderPath, strSuffixes="_progress.html")
        #_qanda.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\jd_comment_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicQandaPageRawData = cmParser.localHtmlFileParse(strBasedir=strProjectHtmlFolderPath, strSuffixes="_qanda.html")
        #_sponsor.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\jd_backer_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicSponsorPageRawData = cmParser.localHtmlFileParse(strBasedir=strProjectHtmlFolderPath, strSuffixes="_sponsor.html")
        #converter
        rawDataConverter = ConverterForJD()
        rawDataConverter.convertProject(lstLstDicRawData=[lstDicIntroPageRawData, lstDicProgressPageRawData, lstDicQandaPageRawData, lstDicSponsorPageRawData])
        rawDataConverter.flushConvertedProjectDataToJsonFile(strJsonFolderPath=strProjectResultFolderPath)
        