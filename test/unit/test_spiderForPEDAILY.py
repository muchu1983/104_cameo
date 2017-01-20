# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.spiderForPEDAILY import SpiderForPEDAILY
"""
測試 抓取 PEDAILY
"""

class SpiderForPEDAILYTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForPEDAILY()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()
    """
    #測試抓取 index page
    def test_downloadIndexPage(self):
        logging.info("SpiderForPEDAILYTest.test_downloadIndexPage")
        self.spider.downloadIndexPage()
    
    #測試抓取 category page
    def test_downloadCategoryPage(self):
        logging.info("SpiderForPEDAILYTest.test_downloadCategoryPage")
        self.spider.downloadCategoryPage()
    """
    #測試抓取 news page
    def test_downloadNewsPage(self):
        logging.info("SpiderForPEDAILYTest.test_downloadNewsPage")
        self.spider.downloadNewsPage(strCategoryName=None)
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


