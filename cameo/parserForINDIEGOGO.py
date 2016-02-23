# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
from scrapy import Selector
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForINDIEGOGO:
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"./cameo_res/source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"./cameo_res/parsed_result"
        self.CATEGORY_URL_LIST_FILENAME = u"category_url_list.txt"
        self.PROJ_URL_LIST_FILENAME = u"_proj_url_list.txt"
        
    #解析 explore.html
    def parseExplorePage(self):
        strExploreHtmlPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"/INDIEGOGO/explore.html"
        strExploreResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"/INDIEGOGO"
        if not os.path.exists(strExploreResultFolderPath):
            os.mkdir(strExploreResultFolderPath) #mkdir parsed_result/INDIEGOGO/
        with open(strExploreHtmlPath, "r") as expHtmlFile:
            strPageSource = expHtmlFile.read()
        root = Selector(text=strPageSource)
        lstStrCategoryUrls = root.css("explore-category-link-www a.i-uncolored-link::attr(href)").extract()
        strCategoryUrlListFilePath = strExploreResultFolderPath + u"/" + self.CATEGORY_URL_LIST_FILENAME
        with open(strCategoryUrlListFilePath, "w+") as catUrlListFile:
            for strCategoryUrl in lstStrCategoryUrls:
                catUrlListFile.write(strCategoryUrl + u"\n")
        
"""
    #解析 category_*.html
    def parseCategoryPage(self):
        for i in range(24):
            strCategoryPageFilePath = self.SOURCE_HTML_CATEGORY_PAGE_PATH + str(i) + self.SOURCE_HTML_EXT
            with open(strCategoryPageFilePath, "r") as catFile:
                strPageSource = catFile.read()
            root = Selector(text=strPageSource)
            strCategoryName = root.css("explore-breadcrumbs span div div.exploreBreadcrumbs-breadcrumb-label.exploreBreadcrumbs-breadcrumb-category.ng-binding::text").extract_first().strip().replace("/", "")
            print(i, strCategoryName)
            strParsedCategoryFolderPath = self.PARSED_RESULT_PATH + strCategoryName + u"/"
            if not os.path.exists(strParsedCategoryFolderPath):
                os.mkdir(strParsedCategoryFolderPath)
            with open(strParsedCategoryFolderPath + strCategoryName + self.PROJ_URL_LIST_FILENAME, "w+") as urlFile:
                lstStrUrls = root.css("a.discoveryCard::attr(href)").extract()
                for strUrl in lstStrUrls:
                    urlFile.write(strUrl + u"\n")
"""