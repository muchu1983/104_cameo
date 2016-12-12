# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import re
import dateparser
from crawlermaster.utility import Utility
"""
[
    {
        "lstStrKeyword": "cm:techcrunch-news-tags", 
        "strContent": "cm:techcrunch-news-content", 
        "strCrawlDate": "", 
        "strPublishDate": "cm:techcrunch-news-time", 
        "strSiteName": "TECHCRUNCH", 
        "strTitle": "cm:techcrunch-news-title", 
        "strUrl": "cm:techcrunch-news-url"
    }
]
"""
class ConverterFor36KR:
    
    #建構子
    def __init__(self):
        self.cmUtility = Utility()
        self.lstDicNewsData = []
        
    def convert(self, lstDicNewsRawData=[], strNewsJsonFilePath=None):
        for dicRawData in lstDicNewsRawData:
            strHtmlFilePath = dicRawData.get("meta-data-html-filepath", None)
            logging.info("convert %s"%strHtmlFilePath)
            try:
                dicNews = {}
                #strTitle
                dicNews["strTitle"] = dicRawData.get("36kr-news-title", [""])[0].strip().strip(u"_36氪").strip()
                #lstStrKeyword
                dicNews["lstStrKeyword"] = dicRawData.get("36kr-news-tags", [""])[0].split(",")
                #strContent
                dicNews["strContent"] = dicRawData.get("36kr-news-content", [""])[0].strip()
                #strCrawlDate
                dicNews["strCrawlDate"] = self.cmUtility.getCtimeOfFile(strFilePath=strHtmlFilePath)
                #strSiteName
                dicNews["strSiteName"] = u"36KR"
                #strUrl
                strUrl = u""
                lstStrMetaContent = dicRawData.get("36kr-news-url", [""])
                for strMetaContent in lstStrMetaContent:
                    if strMetaContent.startswith("http://36kr.com/p/") and strMetaContent.endswith("html"):
                        strUrl = strMetaContent.strip()
                        break
                dicNews["strUrl"] = strUrl
                #strPublishDate (找不到 暫以 strCrawlDate 取代)
                dicNews["strPublishDate"] = dicNews["strCrawlDate"]
                self.lstDicNewsData.append(dicNews)
            except Exception as e:
                logging.warning(str(e))
                logging.warning("convert failed skip: %s"%strHtmlFilePath)
        self.flushConvertedDataToJsonFile(strJsonFilePath=strNewsJsonFilePath)
        logging.info("save %s"%strNewsJsonFilePath)
        
    def flushConvertedDataToJsonFile(self, strJsonFilePath=None):
        self.cmUtility.writeObjectToJsonFile(dicData=self.lstDicNewsData, strJsonFilePath=strJsonFilePath)
        self.lstDicNewsData = []