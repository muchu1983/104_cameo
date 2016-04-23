# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.spiderForBNEXT import SpiderForBNEXT
"""
測試 抓取 BNEXT
"""

class SpiderForBNEXTTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForBNEXT()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()
    
    #測試抓取 index page
    def test_downloadIndexPage(self):
        logging.info("SpiderForBNEXTTest.test_downloadIndexPage")
        self.spider.downloadIndexPage()
    """
    #測試抓取 tag page
    def test_downloadTagPage(self):
        logging.info("SpiderForBNEXTTest.test_downloadTagPage")
        self.spider.downloadTagPag()
    
    #測試抓取 news page
    def test_downloadNewsPage(self):
        logging.info("SpiderForBNEXTTest.test_downloadNewsPage")
        self.spider.downloadNewsPage(strTagName="software_digimarketing")
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


