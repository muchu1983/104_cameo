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
    
    #測試抓取 companies page
    def test_downloadCompaniesPage(self):
        logging.info("SpiderForCROWDCUBETest.test_downloadCompaniesPage")
        self.spider.downloadCompaniesPage()
    """
    #測試抓取 company page
    def test_downloadCompanyPage(self):
        logging.info("SpiderForCROWDCUBETest.test_downloadCompanyPage")
        self.spider.downloadCompanyPage()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


