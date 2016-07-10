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
                
    #解析 category.html
    def parseCategoryPage(self, uselessArg1=None):
        strTopicResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\topic"
        if not os.path.exists(strTopicResultFolderPath):
            os.mkdir(strTopicResultFolderPath) #mkdir parsed_result/TECHCRUNCH/topic/
        strTopicHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\topic"
        self.dicParsedResultOfTopic = {} #清空 dicParsedResultOfTopic 資料 (暫無用處)
        #取得已下載完成的 strTopicUrl list
        lstStrObtainedTopicUrl = self.db.fetchallCompletedObtainedTopicUrl()
        for strObtainedTopicUrl in lstStrObtainedTopicUrl: #topic loop
            #re 找出 topic 名稱
            strTopicNamePartInUrl = re.match("^https://techcrunch.com/topic/(.*)/$", strObtainedTopicUrl).group(1)
            strTopicName = re.sub(u"/", u"__", strTopicNamePartInUrl)
            strTopicSuffixes = u"_%s_topic.html"%strTopicName
            lstStrTopicHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strTopicHtmlFolderPath, strSuffixes=strTopicSuffixes)
            for strTopicHtmlFilePath in lstStrTopicHtmlFilePath: #topic page loop
                logging.info("parse %s"%strTopicHtmlFilePath)
                with open(strTopicHtmlFilePath, "r") as topicHtmlFile:
                    strPageSource = topicHtmlFile.read()
                    root = Selector(text=strPageSource)
                #解析 news URL
                lstStrNewsUrl = root.css("ul.river li.topic-river-block div.block-content-topic h3 a::attr(href)").extract()
                for strNewsUrl in lstStrNewsUrl: #news loop
                    #儲存 news url 及 news topic id 至 DB
                    if re.match("^https://techcrunch.com/[\d]{4}/[\d]{2}/[\d]{2}/.*$", strNewsUrl): #filter remove AD and other url
                        self.db.insertNewsUrlIfNotExists(strNewsUrl=strNewsUrl, strTopicPage1Url=strObtainedTopicUrl)
    
    #解析 projects/*.html 產生 json 並 取得 funder url
    def parseProjectPage(self, uselessArg1=None):
        strNewsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\news"
        if not os.path.exists(strNewsResultFolderPath):
            os.mkdir(strNewsResultFolderPath) #mkdir parsed_result/TECHCRUNCH/news/
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\news"
        strCssJsonFilePath = "cameo_res\\selector_rule\\techcrunch_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        cmParser.localHtmlFileParse()
        strNewsJsonFilePath = strNewsResultFolderPath + u"\\news.json"
        cmParser.flushConvertedDataToJsonFile(strJsonFilePath=strNewsJsonFilePath)
        
    #解析 profile/*.html 產生 json 
    def parseFunderPage(self, uselessArg1=None):
        strNewsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\news"
        if not os.path.exists(strNewsResultFolderPath):
            os.mkdir(strNewsResultFolderPath) #mkdir parsed_result/TECHCRUNCH/news/
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHCRUNCH\\news"
        strCssJsonFilePath = "cameo_res\\selector_rule\\techcrunch_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        cmParser.localHtmlFileParse()
        strNewsJsonFilePath = strNewsResultFolderPath + u"\\news.json"
        cmParser.flushConvertedDataToJsonFile(strJsonFilePath=strNewsJsonFilePath)