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
        self.dicSubCommandHandler = {"index":[self.parseIndexPage],
                                     "tag":[self.parseTagPage],
                                     "news":[self.findMoreTagByParseNewsPage],
                                     "json":[self.parseNewsPageThenCreateNewsJson]}
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfTag = {} #tag.json 資料
        self.dicParsedResultOfNews = {} #news.json 資料
        
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
            lstStrHotTagUrl = root.css("ul#tag-bar li.menu-item-object-post_tag a::attr(href)").extract()
            for strHotTagUrl in lstStrHotTagUrl:
                strHotTagName = re.match("^http://buzzorange.com/techorange/tag/(.*)/$", strHotTagUrl).group(1)
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
                with open(strTagHtmlFilePath, "r") as tagHtmlFile:
                    strPageSource = tagHtmlFile.read()
                    root = Selector(text=strPageSource)
                    #解析 news URL
                    lstStrNewsUrl = root.css("ul.article-list li article header.entry-header h2.entry-title a::attr(href)").extract()
                    for strNewsUrl in lstStrNewsUrl: #news loop
                        #儲存 news url 及 news tag mapping 至 DB
                        self.db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl=strNewsUrl, strTagName=strObtainedTagName)
                        
    #解析 news.html 之一 (取得更多 tag)
    def findMoreTagByParseNewsPage(self, uselessArg1=None):
        pass
        
    #解析 news.html 之二 (產生 news.json )
    def parseNewsPageThenCreateNewsJson(self, uselessArg1=None):
        pass