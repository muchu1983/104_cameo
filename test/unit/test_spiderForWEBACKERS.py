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
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試抓取 Browse page
    def test_downloadBrowsePageAndParseBrowsePage(self):
        logging.info("SpiderForWEBACKERSTest.test_downloadBrowsePageAndParseBrowsePage")
        spider = SpiderForWEBACKERS()
        spider.downloadBrowsePageAndParseBrowsePage()

    #測試抓取 Category page
    def test_downloadCategoryPage(self):
        logging.info("SpiderForWEBACKERSTest.test_downloadCategoryPage")
        spider = SpiderForWEBACKERS()
        spider.downloadCategoryPage()

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


