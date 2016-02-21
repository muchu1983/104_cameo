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
從 source HTML 檔案解析資料
"""
class ParserForINDIEGOGO:
    
    def __init__(self):
        self.SOURCE_HTML_CATEGORY_PAGE_PATH = u"./cameo_res/source_html/INDIEGOGO/"
        self.PARSED_RESULT_PATH = u"./cameo_res/parsed_result/INDIEGOGO/"
        self.SOURCE_HTML_EXT = u".html"
        self.PROJ_URL_LIST_FILENAME = u"_proj_url_list.txt"
    
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
                
