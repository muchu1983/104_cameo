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
from cameo.parserFor36KR import ParserFor36KR
"""
測試 解析 36KR 頁面
"""
class ParserFor36KRTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.parser = ParserFor36KR()
        pass
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 解析 news.html 並建立 news.json
    def test_parseNewsPageThenCreateNewsJson(self):
        logging.info("ParserFor36KRTest.test_parseNewsPageThenCreateNewsJson")
        self.parser.parseNewsPageThenCreateNewsJson()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


