# -*- coding: utf-8 -*-
"""
Copyright (C) 2016, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.spiderForCRUNCHBASE import SpiderForCRUNCHBASE
"""
測試 抓取 CRUNCHBASE
"""

class SpiderForCRUNCHBASETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForCRUNCHBASE()
        
    #收尾
    def tearDown(self):
        pass
    """
    #測試註冊帳號
    def test_registerAccount(self):
        logging.info("SpiderForCRUNCHBASETest.test_registerAccount")
        self.spider.registerAccount()
    
    #測試登入帳號
    def test_loginAccount(self):
        logging.info("SpiderForCRUNCHBASETest.test_loginAccount")
        self.spider.loginAccount()
    
    #測試抓取 companies page
    def test_downloadCompaniesPage(self):
        logging.info("SpiderForCRUNCHBASETest.test_downloadCompaniesPage")
        self.spider.downloadCompaniesPage()
    """
    
    #測試抓取 funding rounds page
    def test_handleSearchFundingRoundsPage(self):
        logging.info("SpiderForCRUNCHBASETest.test_handleSearchFundingRoundsPage")
        self.spider.handleSearchFundingRoundsPage(arg1=None)
    """
    #測試抓取 organization page
    def test_handleOrganizationPage(self):
        logging.info("SpiderForCRUNCHBASETest.test_handleOrganizationPage")
        self.spider.handleOrganizationPage(arg1=None)
    
    #測試建立 category 清單
    def test_createCategoryListJsonFile(self):
        logging.info("SpiderForCRUNCHBASETest.test_createCategoryListJsonFile")
        self.spider.createCategoryListJsonFile()
    """
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


