# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.spiderForWEBACKERS import SpiderForWEBACKERS
"""
測試 抓取 WEBACKERS
"""

class SpiderForWEBACKERSTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForWEBACKERS()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()
    """
    #測試抓取 Browse page
    def test_downloadBrowsePageAndParseBrowsePage(self):
        logging.info("SpiderForWEBACKERSTest.test_downloadBrowsePageAndParseBrowsePage")
        self.spider.downloadBrowsePageAndParseBrowsePage()
    
    #測試抓取 Category page
    def test_downloadCategoryPage(self):
        logging.info("SpiderForWEBACKERSTest.test_downloadCategoryPage")
        self.spider.downloadCategoryPage()
    
    #測試抓取 Project page
    def test_downloadProjectPage(self):
        logging.info("SpiderForWEBACKERSTest.test_downloadProjectPage")
        self.spider.downloadProjectPage("sport")
    """
    #測試抓取 profile page
    def test_downloadProfilePage(self):
        logging.info("SpiderForWEBACKERSTest.test_downloadProfilePage")
        self.spider.downloadProfilePage("sport")
    

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


