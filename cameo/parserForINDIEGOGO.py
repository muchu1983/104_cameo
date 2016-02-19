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
從 local HTML 檔案解析資料
"""
class ParserForINDIEGOGO:
    
    def __init__(self):
        self.LOCAL_HTML_CATEGORY_PAGE_PATH = "./cameo_res/INDIEGOGO/"
        self.LOCAL_HTML_EXT = ".html"
    
    def parseCategoryPage(self):
        for i in range(24):
            strCategoryPageFilePath = self.LOCAL_HTML_CATEGORY_PAGE_PATH + str(i) + self.LOCAL_HTML_EXT
            with open(strCategoryPageFilePath, "r") as file:
                strPageSource = file.read()
            root = Selector(text=strPageSource)
            strCategoryName = root.css("explore-breadcrumbs span div div.exploreBreadcrumbs-breadcrumb-label.exploreBreadcrumbs-breadcrumb-category.ng-binding::text").extract_first().strip().replace("/", "")
            strCategoryFolderPath = self.LOCAL_HTML_CATEGORY_PAGE_PATH + strCategoryName
            if not os.path.exists(strCategoryFolderPath):
                os.mkdir(strCategoryFolderPath)
