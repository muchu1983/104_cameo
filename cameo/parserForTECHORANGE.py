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
from cameo.localdb import LocalDbForTECHORANGE
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForTECHORANGE:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = LocalDbForTECHORANGE()
        self.dicSubCommandHandler = {
            "index":[self.parseIndexPage],
            "tag":[self.parseTagPage],
            "news":[self.findMoreTagByParseNewsPage],
            "json":[self.parseNewsPageThenCreateNewsJson]
        }
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.intNewsJsonNum = 0 #news.json 檔案編號
        self.intMaxNewsPerNewsJsonFile = 1000 #每個 news.json 儲存的 news 之最大數量
        self.dicParsedResultOfTag = {} #tag.json 資料
        self.dicParsedResultOfNews = [] #news.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return ("- TECHORANGE -\n"
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
        strIndexResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\TECHORANGE"
        if not os.path.exists(strIndexResultFolderPath):
            os.mkdir(strIndexResultFolderPath) #mkdir parsed_result/TECHORANGE/
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE"
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        with open(strIndexHtmlFilePath, "r") as indexHtmlFile:
            strPageSource = indexHtmlFile.read()
            root = Selector(text=strPageSource)
            lstStrHotTagUrl = root.css("ul#menu-tag-bar li.menu-item-object-post_tag a::attr(href)").extract()
            for strHotTagUrl in lstStrHotTagUrl:
                if strHotTagUrl.startswith("https://buzzorange.com/techorange/tag/"):
                    strHotTagName = re.match("^https://buzzorange\.com/techorange/tag/(.*)/$", strHotTagUrl).group(1)
                    logging.info("find tag: %s"%strHotTagName)
                    self.db.insertTagIfNotExists(strTagName=strHotTagName)
                
    #解析 tag.html
    def parseTagPage(self, uselessArg1=None):
        strTagResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\TECHORANGE\\tag"
        if not os.path.exists(strTagResultFolderPath):
            os.mkdir(strTagResultFolderPath) #mkdir parsed_result/TECHORANGE/tag/
        strTagHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE\\tag"
        self.dicParsedResultOfTag = {} #清空 dicParsedResultOfTag 資料 (暫無用處)
        #取得已下載完成的 strTagName list
        lstStrObtainedTagName = self.db.fetchallCompletedObtainedTagName()
        for strObtainedTagName in lstStrObtainedTagName: #tag loop
            strTagSuffixes = u"_%s_tag.html"%strObtainedTagName
            lstStrTagHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strTagHtmlFolderPath, strSuffixes=strTagSuffixes)
            for strTagHtmlFilePath in lstStrTagHtmlFilePath: #tag page loop
                logging.info("parse %s"%strTagHtmlFilePath)
                with open(strTagHtmlFilePath, "r") as tagHtmlFile:
                    strPageSource = tagHtmlFile.read()
                    root = Selector(text=strPageSource)
                    #解析 news URL
                    lstStrNewsUrl = root.css("#main article.post header.entry-header h4.entry-title a::attr(href)").extract()
                    for strNewsUrl in lstStrNewsUrl: #news loop
                        #儲存 news url 及 news tag mapping 至 DB
                        logging.info("find news: %s"%strNewsUrl)
                        self.db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl=strNewsUrl, strTagName=strObtainedTagName)
                    
    #解析 news.html 之一 (取得更多 tag)
    def findMoreTagByParseNewsPage(self, uselessArg1=None):
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE\\news"
        #讀取 news.html
        lstStrNewsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strNewsHtmlFolderPath, strSuffixes=u"_news.html")
        for strNewsHtmlFilePath in lstStrNewsHtmlFilePath:
            logging.info("parse %s"%strNewsHtmlFilePath)
            with open(strNewsHtmlFilePath, "r") as newsHtmlFile:
                strPageSource = newsHtmlFile.read()
                root = Selector(text=strPageSource)
                #解析 news.html
                lstStrTagUrl = root.css("ul.post-tags li a[rel=tag]::attr(href)").extract()
                for strTagUrl in lstStrTagUrl:
                    if strTagUrl.startswith("https://buzzorange.com/techorange/tag/"):
                        strTagName = re.match("https://buzzorange\.com/techorange/tag/(.*)/", strTagUrl).group(1)
                        logging.info("find tag: %s"%strTagName)
                        self.db.insertTagIfNotExists(strTagName=strTagName)
        
    #解析 news.html 之二 (產生 news.json )
    def parseNewsPageThenCreateNewsJson(self, uselessArg1=None):
        strNewsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\TECHORANGE\\news"
        if not os.path.exists(strNewsResultFolderPath):
            os.mkdir(strNewsResultFolderPath) #mkdir parsed_result/TECHORANGE/news/
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\TECHORANGE\\news"
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
                dicNewsData["strSiteName"] = u"TECHORANGE"
                #strUrl
                strShareNewsUrlHref = root.css("#share_group_btns div.share_facebook a::attr(href)").extract_first().strip()
                strNewsUrl = re.match("^.*(https://buzzorange.com/techorange/[\d]{4}/[\d]{2}/[\d]{2}/.*/)$", strShareNewsUrlHref).group(1).strip()
                dicNewsData["strUrl"] = strNewsUrl
                #strTitle
                dicNewsData["strTitle"] = root.css("header.entry-header h1.entry-title::text").extract_first().strip()
                #strContent
                # filter 項目：'by'作者、日期、tag、分享計數、分享總數、標題、上一頁、下一頁、java script、廣告…
                strCssNotFilter = ":not(a[rel=tag]):not(script)"
                lstStrContent = root.css("#main div.entry-content *%s::text"%strCssNotFilter).extract()
                strContent = re.sub("\s", "", u"".join(lstStrContent)) #接合 新聞內容 並去除空白字元
                dicNewsData["strContent"] = strContent.strip().strip(u"、")
                #lstStrKeyword
                dicNewsData["lstStrKeyword"] = root.css("ul.post-tags li a[rel=tag]::text").extract()
                #strPublishDate
                strPublishDateText = root.css("#main article.post header.entry-header span time.entry-date::text").extract_first().strip()
                dicNewsData["strPublishDate"] = re.sub("/", "-", strPublishDateText)
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