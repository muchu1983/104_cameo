# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import json
from cameo.parserForWEBACKERS import ParserForWEBACKERS

"""
測試
"""

class ParserForWEBACKERSTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
        
    #測試 解析 category 頁面
    def test_parseCategoryPage(self):
        logging.info("ParserForWEBACKERSTest.test_parseCategoryPage")
        parser = ParserForWEBACKERS()
        parser.parseCategoryPage()
        
    #測試 解析 project 頁面
    def test_parseProjectPage(self):
        logging.info("ParserForWEBACKERSTest.test_parseProjectPage")
        strCategoryName = "charity"
        parser = ParserForWEBACKERS()
        parser.beforeParseProjectPage(strCategoryName)
        parser.parseIntroPage(strCategoryName)
        parser.parseSponsorPage(strCategoryName)
        parser.afterParseProjectPage(strCategoryName)

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


