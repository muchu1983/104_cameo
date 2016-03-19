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
    
    #測試 解析 回饋組合的贊助狀態 字串
    def test_parseStrRewardBacker(self):
        logging.info("ParserForWEBACKERSTest.test_parseStrRewardBacker")
        parser = ParserForWEBACKERS()
        ret = parser.parseStrRewardBacker(strRewardBacker=u"1人待繳5人剩餘94人")
        self.assertEquals((1, 5, 94), ret)
        ret = parser.parseStrRewardBacker(strRewardBacker=u"1人待繳5人")
        self.assertEquals((1, 5, None), ret)
        ret = parser.parseStrRewardBacker(strRewardBacker=u"15人")
        self.assertEquals((15, None, None), ret)
    
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


