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
        self.dicSubCommandHandler = {"index":[],
                                     "tag":[],
                                     "news":[]}
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfTag = {} #tag.json 資料
        self.dicParsedResultOfNews = {} #news.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return ("- TECHORANGE -\n"
                "useage:\n"
                "index - \n"
                "tag - "
                "news - ")
                
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
                self.db.insertTagIFNotExists(strTagName=strHotTagName)
            