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
from crawlermaster.cmparser import CmParser
from cameo.cmConverter.converterFor36KR import ConverterFor36KR
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserFor36KR:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.dicSubCommandHandler = {
            "json":[self.parseNewsPageThenCreateNewsJson]
        }
        self.strWebsiteDomain = u"http://36kr.com/"
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.intNewsJsonNum = 0 #news.json 檔案編號
        self.intMaxNewsPerNewsJsonFile = 1000 #每個 news.json 儲存的 news 之最大數量
        self.dicParsedResultOfNews = [] #news.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return (
            "- 36KR -\n"
            "useage:\n"
            "json - parse news.html then create json \n"
        )
                
    #執行 parser
    def runParser(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)
    
    #解析 news.html 產生 news.json (TODO 使用 crawlermaster 進行 parse)
    def parseNewsPageThenCreateNewsJson(self, uselessArg1=None):
        strNewsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\36KR\\news"
        if not os.path.exists(strNewsResultFolderPath):
            os.mkdir(strNewsResultFolderPath) #mkdir parsed_result/36KR/news/
        strNewsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\36KR\\news"
        strCssJsonFilePath = "cameo_res\\selector_rule\\36kr_csslist.json"
        cmParser = CmParser(strCssJsonFilePath=strCssJsonFilePath)
        rawDataConverter = ConverterFor36KR()
        intNewsJsonIndex = 1
        lstDicNewsRawData = cmParser.localHtmlFileParse(isIterable=True, isResetIteration=True)
        while len(lstDicNewsRawData)>0:
            strNewsJsonFilePath = strNewsResultFolderPath + u"\\%d_news.json"%(intNewsJsonIndex*1000)
            rawDataConverter.convert(lstDicNewsRawData=lstDicNewsRawData, strNewsJsonFilePath=strNewsJsonFilePath)
            intNewsJsonIndex = intNewsJsonIndex+1
            lstDicNewsRawData = cmParser.localHtmlFileParse(isIterable=True)
        