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
import urllib
from scrapy import Selector
from cameo.utility import Utility
from cameo.localdb import LocalDbForJD
from crawlermaster.cmparser import CmParser
from cameo.cmConverter.converterForJD import ConverterForJD
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForJD:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = LocalDbForJD()
        self.dicSubCommandHandler = {
            "index":[self.parseIndexPage],
            "category":[self.parseCategoryPage],
            "project":[self.parseProjectPage],
            "funder":[self.parseFunderPage]
        }
        self.strWebsiteDomain = u"http://z.jd.com"
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfCategory = {} #category.json 資料
        self.dicParsedResultOfProject = {} #project.json 資料
        self.dicParsedResultOfUpdate = {} #update.json 資料
        self.dicParsedResultOfQanda = {} #qanda.json 資料
        self.dicParsedResultOfReward = {} #reward.json 資料
        self.dicParsedResultOfProfile = {} #profile.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return (
            "- JD -\n"
            "useage:\n"
            "index - parse index.html then insert category into DB \n"
            "category - parse category.html then insert project into DB \n"
            "project - parse projects/*.html then create json and insert funder into DB \n"
            "funder - parse profiles/*.html then create json \n"
        )
                
    #執行 parser
    def runParser(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)
    
    #解析 index.html
    def parseIndexPage(self, uselessArg1=None):
        strIndexResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\JD"
        if not os.path.exists(strIndexResultFolderPath):
            os.mkdir(strIndexResultFolderPath) #mkdir parsed_result/JD/
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD"
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        with open(strIndexHtmlFilePath, "r") as indexHtmlFile:
            strPageSource = indexHtmlFile.read()
            root = Selector(text=strPageSource)
        lstStrCategoryPage1Url = root.css("div.browse ul#categorylist li a::attr(href)").extract()
        lstStrCategoryName = root.css("div.browse ul#categorylist li a::text").extract()
        for (indexOFCategory, strCategoryPage1Url) in enumerate(lstStrCategoryPage1Url):
            if strCategoryPage1Url.startswith("/bigger/search.html?categoryId="):
                strCategoryPage1Url = self.strWebsiteDomain + strCategoryPage1Url
                #URL encode 分類名稱
                strCategoryName = lstStrCategoryName[indexOFCategory]
                logging.info("insert category %s:%s"%(strCategoryName, strCategoryPage1Url))
                self.db.insertCategoryIfNotExists(strCategoryPage1Url=strCategoryPage1Url, strCategoryName=strCategoryName)
                
    #解析 category.html (strCategoryPage1Url == None 會自動找尋已完成下載之 category)
    def parseCategoryPage(self, strCategoryPage1Url=None):
        if strCategoryPage1Url is None:
            #未指定 category url
            #取得已下載完成的 strCategoryUrl list
            lstStrObtainedCategoryUrl = self.db.fetchallCompletedObtainedCategoryUrl()
            for strObtainedCategoryUrl in lstStrObtainedCategoryUrl: #category loop
                self.parseCategoryPageWithGivenCategoryUrl(strCategoryPage1Url=strObtainedCategoryUrl)
        else:
            #有指定 category url
            self.parseCategoryPageWithGivenCategoryUrl(strCategoryPage1Url=strCategoryPage1Url)
                
    #解析 category.html
    def parseCategoryPageWithGivenCategoryUrl(self, strCategoryPage1Url=None):
        #取出 category 名稱
        strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strCategoryPage1Url)
        strCategoryResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\JD\\%s"%strCategoryName
        if not os.path.exists(strCategoryResultFolderPath):
            os.mkdir(strCategoryResultFolderPath) #mkdir parsed_result/JD/category/
        strCategoryHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD\\%s"%strCategoryName
        self.dicParsedResultOfCategory = {} #清空 dicParsedResultOfCategory 資料 (暫無用處)
        strCategorySuffixes = u"_%s_category.html"%strCategoryName
        lstStrCategoryHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strCategoryHtmlFolderPath, strSuffixes=strCategorySuffixes)
        for strCategoryHtmlFilePath in lstStrCategoryHtmlFilePath: #category page loop
            logging.info("parse %s"%strCategoryHtmlFilePath)
            with open(strCategoryHtmlFilePath, "r") as categoryHtmlFile:
                strPageSource = categoryHtmlFile.read()
                root = Selector(text=strPageSource)
            #解析 project URL
            lstStrProjectUrl = root.css("li.info a::attr(href)").extract()
            for strProjectUrl in lstStrProjectUrl: #project loop
                #儲存 project url 及 news category id 至 DB
                if re.match("^/project/details/[\d]+.html$", strProjectUrl): #filter remove AD and other url
                    strProjectUrl = self.strWebsiteDomain + strProjectUrl
                    logging.info("insert project url: %s"%strProjectUrl)
                    self.db.insertProjectUrlIfNotExists(strProjectUrl=strProjectUrl, strCategoryPage1Url=strCategoryPage1Url)
    
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
        """
        strCssJsonFilePath = "cameo_res\\selector_rule\\jd_backer_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicSponsorPageRawData = cmParser.localHtmlFileParse(strBasedir=strProjectHtmlFolderPath, strSuffixes="_sponsor.html")
        """
        lstDicSponsorPageRawData = []
        #converter
        rawDataConverter = ConverterForJD()
        rawDataConverter.convertProject(lstLstDicRawData=[lstDicIntroPageRawData, lstDicProgressPageRawData, lstDicQandaPageRawData, lstDicSponsorPageRawData])
        rawDataConverter.flushConvertedProjectDataToJsonFile(strJsonFolderPath=strProjectResultFolderPath)
        
    #解析 profiles/*.html 產生 json 並 取得 (strCategoryPage1Url == None 會自動找尋已完成下載之 category)
    def parseFunderPage(self, strCategoryPage1Url=None):
        if strCategoryPage1Url is None:
            #未指定 category url
            #取得已下載完成的 strCategoryUrl list
            lstStrObtainedCategoryUrl = self.db.fetchallCompletedObtainedCategoryUrl()
            for strObtainedCategoryUrl in lstStrObtainedCategoryUrl: #category loop
                strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strObtainedCategoryUrl)
                self.parseFunderPageWithGivenCategory(strCategoryPage1Url=strObtainedCategoryUrl, strCategoryName=strCategoryName)
        else:
            #有指定 category url
            strCategoryName = self.db.fetchCategoryNameByUrl(strCategoryPage1Url=strCategoryPage1Url)
            self.parseFunderPageWithGivenCategory(strCategoryPage1Url=strCategoryPage1Url, strCategoryName=strCategoryName)
        
    #解析 profiles/*.html 產生 json 
    def parseFunderPageWithGivenCategory(self, strCategoryPage1Url=None, strCategoryName=None):
        strProfileResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\JD\\%s\\profiles"%strCategoryName
        if not os.path.exists(strProfileResultFolderPath):
            os.mkdir(strProfileResultFolderPath) #mkdir parsed_result/JD/category/profiles
        strProfileHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\JD\\%s\\profiles"%strCategoryName
        #_proj.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\jd_creator_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicProjPageRawData = cmParser.localHtmlFileParse(strBasedir=strProfileHtmlFolderPath, strSuffixes="_proj.html")
        #_order.html
        strCssJsonFilePath = "cameo_res\\selector_rule\\jd_creator_back_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        lstDicOrderPageRawData = cmParser.localHtmlFileParse(strBasedir=strProfileHtmlFolderPath, strSuffixes="_order.html")
        #converter
        rawDataConverter = ConverterForJD()
        rawDataConverter.convertProfile(lstLstDicRawData=[lstDicProjPageRawData, lstDicOrderPageRawData])
        strProfileJsonFilePath = strProfileResultFolderPath + u"\\profile.json"
        rawDataConverter.flushConvertedProfileDataToJsonFile(strJsonFilePath=strProfileJsonFilePath)