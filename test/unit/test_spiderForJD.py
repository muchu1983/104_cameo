# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.spiderForJD import SpiderForJD
"""
測試 抓取 京東眾籌
"""

class SpiderForJDTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForJD()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()
    """
    #測試抓取 index page
    def test_downloadIndexPage(self):
        logging.info("SpiderForJDTest.test_downloadIndexPage")
        self.spider.downloadIndexPage()
    
    #測試抓取 category page
    def test_downloadCategoryPage(self):
        logging.info("SpiderForJDTest.test_downloadCategoryPage")
        self.spider.downloadCategoryPage(strCategoryPage1Url=None)
    """
    #測試抓取 project page
    def test_downloadProjectPage(self):
        logging.info("SpiderForJDTest.test_downloadProjectPage")
        self.spider.downloadProjectPage(strCategoryPage1Url=None)
    """
    #測試抓取 funder page
    def test_downloadFunderPage(self):
        logging.info("SpiderForJDTest.test_downloadFunderPage")
        self.spider.downloadFunderPage(strCategoryPage1Url=None)
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


