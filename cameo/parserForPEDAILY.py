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
from cameo.localdb import LocalDbForPEDAILY
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForPEDAILY:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = LocalDbForPEDAILY()
        self.dicSubCommandHandler = {"index":[self.parseIndexPage],
                                     "category":[self.parseCategoryPage],
                                     "json":[self.parseNewsPageThenCreateNewsJson]}
        self.strWebsiteDomain = u"http://www.pedaily.cn"
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.intNewsJsonNum = 0 #news.json 檔案編號
        self.intMaxNewsPerNewsJsonFile = 1000 #每個 news.json 儲存的 news 之最大數量
        self.dicParsedResultOfCategory = {} #category.json 資料
        self.dicParsedResultOfNews = [] #news.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return ("- PEDAILY -\n"
                "useage:\n"
                "index - parse index.html then insert tag into DB \n"
                "category - parse category.html then insert news into DB \n"
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
        strIndexResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\PEDAILY"
        if not os.path.exists(strIndexResultFolderPath):
            os.mkdir(strIndexResultFolderPath) #mkdir parsed_result/PEDAILY/
        strIndexHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\PEDAILY"
        strIndexHtmlFilePath = strIndexHtmlFolderPath + u"\\index.html"
        with open(strIndexHtmlFilePath, "r") as indexHtmlFile:
            strPageSource = indexHtmlFile.read()
            root = Selector(text=strPageSource)
            lstStrCategoryUrl = root.css("div.footer ul.main li.box-fix-d dl dt:nth-of-type(3) ul li a::attr(href)").extract()
            for strCategoryUrl in lstStrCategoryUrl:
                strCategoryName = re.match("^http://www.pedaily.cn/(.*)/$", strCategoryUrl).group(1)
                strCategoryName = urllib.quote(strCategoryName.encode("utf-8")) #url encode
                self.db.insertCategoryIfNotExists(strCategoryName=strCategoryName)
                
    #解析 category.html
    def parseCategoryPage(self, uselessArg1=None):
        strTagResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\BNEXT\\tag"
        if not os.path.exists(strTagResultFolderPath):
            os.mkdir(strTagResultFolderPath) #mkdir parsed_result/BNEXT/tag/
        strTagHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\BNEXT\\tag"
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
                    lstStrNewsUrl = root.css("div#search_list div.item_box div.div_tr div.item_text a.item_title::attr(href)").extract()
                    for strNewsUrl in lstStrNewsUrl: #news loop
                        #儲存 news url 及 news tag mapping 至 DB
                        if strNewsUrl.startswith("/article/view/id/"): #filter remove AD and px... url
                            strNewsUrl = self.strWebsiteDomain + strNewsUrl
                            self.db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl=strNewsUrl, strTagName=strObtainedTagName)
    
    #解析 news.html 之二 (產生 news.json )
    def parseNewsPageThenCreateNewsJson(self, uselessArg1=None):
        strNewsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\BNEXT\\news"
        if not os.path.exists(strNewsResultFolderPath):
            os.mkdir(strNewsResultFolderPath) #mkdir parsed_result/BNEXT/news/
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\BNEXT\\news"
        self.dicParsedResultOfNews = [] #清空 news.json 資料
        self.intNewsJsonNum = 0 #計數器歸零
        #讀取 news.html
        lstStrNewsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strNewsHtmlFolderPath, strSuffixes=u"_news.html")
        for strNewsHtmlFilePath in lstStrNewsHtmlFilePath:
            logging.info("parse %s"%strNewsHtmlFilePath)
            dicNewsData = {} #新聞資料物件
            with open(strNewsHtmlFilePath, "r") as newsHtmlFile:
                strPageSource = newsHtmlFile.read()
                root = Selector(text=strPageSource)
            #解析 news.html
            #檢查 news 是否為看板新聞
            eleBoardLabel = root.css("span.board-label").extract_first()
            if eleBoardLabel: # is not None
                # rename news 檔名為 xxx_news.html.error
                os.rename(strNewsHtmlFilePath, strNewsHtmlFilePath + u".error")
                logging.warning("%s is board news,skip parse it."%strNewsHtmlFilePath)
                continue #略過該筆 news
            #strSiteName
            dicNewsData["strSiteName"] = u"BNEXT"
            #strUrl
            strUrl = root.css("div.fb-like::attr(data-href)").extract_first()
            dicNewsData["strUrl"] = strUrl
            #strTitle
            strTitle = root.css("div.main_title::text").extract_first()
            dicNewsData["strTitle"] = strTitle
            #strContent
            lstStrContent = root.css("div.content.htmlview *:not(script)::text").extract()
            strContent = re.sub("\s", "", u"".join(lstStrContent)) #接合 新聞內容 並去除空白字元
            dicNewsData["strContent"] = strContent.strip()
            #lstStrKeyword
            lstStrKeyword = root.css("div.tag_box a.tag_link::text").extract()
            dicNewsData["lstStrKeyword"] = lstStrKeyword
            #strPublishDate
            strPublishDate = root.css("div.info_box span.info:nth-of-type(2)::text").extract_first()
            strPublishDate = re.sub("[^0-9-]", "", re.sub("/", "-", strPublishDate)) #date format 2016-04-24
            dicNewsData["strPublishDate"] = strPublishDate
            #strCrawlDate
            dicNewsData["strCrawlDate"] = self.utility.getCtimeOfFile(strFilePath=strNewsHtmlFilePath)
            #將 新聞資料物件 加入 json
            self.dicParsedResultOfNews.append(dicNewsData)
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