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
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForWEBACKERS:
    #建構子
    def __init__(self):
        logging.basicConfig(level=logging.WARNING)
        self.utility = Utility()
        self.dicSubCommandHandler = {}
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfProject = {} #project.json 資料
        self.dicParsedResultOfUpdate = {} #update.json 資料
        self.dicParsedResultOfComment = {} #comment.json 資料
        self.dicParsedResultOfReward = {} #reward.json 資料
        self.dicParsedResultOfProfile = {} #profile.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return """- WEBACKERS -
useage:
"""

    #執行 parser
    def runParser(self, lstSubcommand=[]):
        pass

#category #####################################################################################
    #解析 category.html
    def parseCategoryPage(self, uselessArg1=None):
        strBrowseHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\WEBACKERS"
        lstStrCategoryFolderPath = self.utility.getSubFolderPathList(strBasedir=strBrowseHtmlFolderPath)
        for strCategoryFolderPath in lstStrCategoryFolderPath:
            lstStrCategoryHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strCategoryFolderPath, strSuffixes=u"category.html")
            for strCategoryHtmlFilePath in lstStrCategoryHtmlFilePath:
                print(strCategoryHtmlFilePath)