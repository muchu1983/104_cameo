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
from cameo.parserForTECHORANGE import ParserForTECHORANGE
"""
測試 解析 科技報橘 頁面
"""
class ParserForTECHORANGETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 解析 index.html
    def test_parseIndexPage(self):
        logging.info("ParserForTECHORANGETest.test_parseIndexPage")
        parser = ParserForTECHORANGE()
        parser.parseIndexPage()
        
    #測試 解析 tag.html
    def test_parseTagPage(self):
        logging.info("ParserForTECHORANGETest.test_parseTagPage")
        parser = ParserForTECHORANGE()
        parser.parseTagPage()
  
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


