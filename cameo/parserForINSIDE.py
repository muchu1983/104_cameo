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
import dateparser
from scrapy import Selector
from cameo.utility import Utility
from cameo.localdb import LocalDbForINSIDE
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForINSIDE:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = LocalDbForINSIDE()
        self.dicSubCommandHandler = {"index":[self.parseIndexPage],
                             "tag":[self.parseTagPage],
                             "news":[self.findMoreTagByParseNewsPage],
                             "json":[self.parseNewsPageThenCreateNewsJson]}
        self.strWebsiteDomain = u"http://www.inside.com.tw"
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.intNewsJsonNum = 0 #news.json 檔案編號
        self.intMaxNewsPerNewsJsonFile = 1000 #每個 news.json 儲存的 news 之最大數量
        self.dicParsedResultOfTag = {} #tag.json 資料
        self.dicParsedResultOfNews = [] #news.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return ("- INSIDE -\n"
                "useage:\n"
                "index - parse index.html then insert tag into DB \n"
                "tag - parse tag.html then insert news and newstag into DB \n"
                "news - parse news.html then insert tag into DB \n"
                "json - parse news.html then create json \n")
                
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
        strIndexResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\INSIDE"
        if not os.path.exists(strIndexResultFolderPath):
            os.mkdir(strIndexResultFolderPath) #mkdir parsed_result/INSIDE/
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\INSIDE"
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        with open(strIndexHtmlFilePath, "r") as indexHtmlFile:
            strPageSource = indexHtmlFile.read()
            root = Selector(text=strPageSource)
            lstStrUrlInIndexPage = root.css("a::attr(href)").extract()
            for strUrlInIndexPage in lstStrUrlInIndexPage:
                if strUrlInIndexPage.startswith("http://www.inside.com.tw/category/"):
                    self.db.insertTagIfNotExists(strTagPage1Url=strUrlInIndexPage)
                
    #解析 tag.html
    def parseTagPage(self, uselessArg1=None):
        strTagResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\INSIDE\\tag"
        if not os.path.exists(strTagResultFolderPath):
            os.mkdir(strTagResultFolderPath) #mkdir parsed_result/INSIDE/tag/
        strTagHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\INSIDE\\tag"
        self.dicParsedResultOfTag = {} #清空 dicParsedResultOfTag 資料 (暫無用處)
        #取得已下載完成的 strTagPage1Url list
        lstStrObtainedTagPage1Url = self.db.fetchallCompletedObtainedTagPage1Url()
        for strObtainedTagPage1Url in lstStrObtainedTagPage1Url: #tag loop
            #re 找出 tag 名稱
            strTagNamePartInUrl = re.match("^http://www.inside.com.tw/category/(.*)$", strObtainedTagPage1Url).group(1)
            strTagName = re.sub(u"/", u"__", strTagNamePartInUrl)
            strTagSuffixes = u"_%s_tag.html"%strTagName
            lstStrTagHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strTagHtmlFolderPath, strSuffixes=strTagSuffixes)
            for strTagHtmlFilePath in lstStrTagHtmlFilePath: #tag page loop
                logging.info("parse %s"%strTagHtmlFilePath)
                with open(strTagHtmlFilePath, "r") as tagHtmlFile:
                    strPageSource = tagHtmlFile.read()
                    root = Selector(text=strPageSource)
                    #解析 news URL
                    lstStrNewsUrl = root.css("section#articles article div.post-container h2.entry-title a::attr(href)").extract()
                    for strNewsUrl in lstStrNewsUrl: #news loop
                        #儲存 news url 及 news tag mapping 至 DB
                        if re.match("^http://www.inside.com.tw/[\d]{4}/[\d]{2}/[\d]{2}/.*$", strNewsUrl): #filter remove AD and other url
                            self.db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl=strNewsUrl, strTagPage1Url=strObtainedTagPage1Url)
                    
    #解析 news.html 之一 (取得更多 tag)
    def findMoreTagByParseNewsPage(self, uselessArg1=None):
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\INSIDE\\news"
        #讀取 news.html
        lstStrNewsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strNewsHtmlFolderPath, strSuffixes=u"_news.html")
        for strNewsHtmlFilePath in lstStrNewsHtmlFilePath:
            logging.info("parse %s"%strNewsHtmlFilePath)
            with open(strNewsHtmlFilePath, "r") as newsHtmlFile:
                strPageSource = newsHtmlFile.read()
                root = Selector(text=strPageSource)
                #解析 news.html
                lstStrUrlInNewsPage = root.css("a::attr(href)").extract()
                for strUrlInNewsPage in lstStrUrlInNewsPage:
                    if strUrlInNewsPage.startswith("http://www.inside.com.tw/category/"):
                        self.db.insertTagIfNotExists(strTagPage1Url=strUrlInNewsPage)
        
    #解析 news.html 之二 (產生 news.json )
    def parseNewsPageThenCreateNewsJson(self, uselessArg1=None):
        strNewsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\INSIDE\\news"
        if not os.path.exists(strNewsResultFolderPath):
            os.mkdir(strNewsResultFolderPath) #mkdir parsed_result/INSIDE/news/
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\INSIDE\\news"
        self.dicParsedResultOfNews = [] #清空 news.json 資料
        self.intNewsJsonNum = 0 #計數器歸零
        #讀取 news.html
        lstStrNewsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strNewsHtmlFolderPath, strSuffixes=u"_news.html")
        for strNewsHtmlFilePath in lstStrNewsHtmlFilePath:
            logging.info("parse %s"%strNewsHtmlFilePath)
            try:
                dicNewsData = {} #新聞資料物件
                with open(strNewsHtmlFilePath, "r") as newsHtmlFile:
                    strPageSource = newsHtmlFile.read()
                    root = Selector(text=strPageSource)
                #解析 news.html
                #strSiteName
                dicNewsData["strSiteName"] = u"INSIDE"
                #strUrl
                strUrl = root.css("div.thumb-container a::attr(href)").extract_first()
                dicNewsData["strUrl"] = strUrl
                #strTitle
                strTitle = root.css("div.post-container h2.entry-title::text").extract_first()
                dicNewsData["strTitle"] = strTitle
                #strContent
                lstStrContent = root.css("div.post-container div.content *:not(script)::text").extract()
                strContent = re.sub("\s", "", u"".join(lstStrContent)) #接合 新聞內容 並去除空白字元
                dicNewsData["strContent"] = strContent.strip()
                #lstStrKeyword
                lstStrKeyword = root.css("div.cat-list a::text").extract()
                dicNewsData["lstStrKeyword"] = lstStrKeyword
                #strPublishDate
                strPublishDate = root.css("div.post-container a.published-time::text").extract_first().strip()
                strPublishDate = self.utility.parseStrDateByDateparser(strOriginDate=strPublishDate)
                dicNewsData["strPublishDate"] = strPublishDate
                #strCrawlDate
                dicNewsData["strCrawlDate"] = self.utility.getCtimeOfFile(strFilePath=strNewsHtmlFilePath)
                #將 新聞資料物件 加入 json
                self.dicParsedResultOfNews.append(dicNewsData)
            except:
                logging.error("parse %s fail skip it"%strNewsHtmlFilePath)
                # set isGot = 0
                strNewsHtmlFileName = strNewsHtmlFilePath.split(os.sep)[-1]
                strNewsName = re.match(u"^(?P<newsName>.*)_news.html$", strNewsHtmlFileName).group("newsName")
                self.db.updateNewsStatusIsNotGot(strNewsUrlPart=strNewsName)
                continue #skip it
            #每一千筆資料另存一個 json
            if len(self.dicParsedResultOfNews) == self.intMaxNewsPerNewsJsonFile:
                self.intNewsJsonNum = self.intNewsJsonNum + self.intMaxNewsPerNewsJsonFile
                #儲存 json
                strNewsJsonFilePath = strNewsResultFolderPath + u"\\%d_news.json"%self.intNewsJsonNum
                self.utility.writeObjectToJsonFile(dicData=self.dicParsedResultOfNews, strJsonFilePath=strNewsJsonFilePath)
                logging.info("%d news saved on %s"%(self.intMaxNewsPerNewsJsonFile, strNewsJsonFilePath))
                self.dicParsedResultOfNews = [] #清空 news.json 資料
        else:#news loop 順利結束，儲存剩餘的 news 至 json
            self.intNewsJsonNum = self.intNewsJsonNum + self.intMaxNewsPerNewsJsonFile
            #儲存 json
            strNewsJsonFilePath = strNewsResultFolderPath + u"\\%d_news.json"%self.intNewsJsonNum
            self.utility.writeObjectToJsonFile(dicData=self.dicParsedResultOfNews, strJsonFilePath=strNewsJsonFilePath)
            logging.info("%d news saved on %s"%(len(self.dicParsedResultOfNews), strNewsJsonFilePath))
            self.dicParsedResultOfNews = [] #清空 news.json 資料