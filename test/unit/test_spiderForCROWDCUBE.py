# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.spiderForCROWDCUBE import SpiderForCROWDCUBE
"""
測試 抓取 CROWDCUBE
"""

class SpiderForCROWDCUBETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForCROWDCUBE()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()
    """
    #測試註冊帳號
    def test_registerAccount(self):
        logging.info("SpiderForCROWDCUBETest.test_registerAccount")
        self.spider.registerAccount()
    
    #測試登入帳號
    def test_loginAccount(self):
        logging.info("SpiderForCROWDCUBETest.test_loginAccount")
        self.spider.loginAccount()
    """
    #測試抓取 companies page
    def test_downloadCompaniesPage(self):
        logging.info("SpiderForCROWDCUBETest.test_downloadCompaniesPage")
        self.spider.downloadCompaniesPage()
    """
    #測試抓取 category page
    def test_downloadCategoryPage(self):
        logging.info("SpiderForCROWDCUBETest.test_downloadCategoryPage")
        self.spider.downloadCategoryPage(strCategoryPage1Url=None)
    
    #測試抓取 project page
    def test_downloadProjectPage(self):
        logging.info("SpiderForCROWDCUBETest.test_downloadProjectPage")
        self.spider.downloadProjectPage(strCategoryPage1Url=None)
    
    #測試抓取 funder page
    def test_downloadFunderPage(self):
        logging.info("SpiderForCROWDCUBETest.test_downloadFunderPage")
        self.spider.downloadFunderPage(strCategoryPage1Url=None)
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


