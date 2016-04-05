# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.spiderForTECHORANGE import SpiderForTECHORANGE
"""
測試 抓取 TECHORANGE
"""

class SpiderForTECHORANGETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForTECHORANGE()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()
    
    #測試抓取 Browse page
    def test_downloadIndexPage(self):
        logging.info("SpiderForTECHORANGETest.test_downloadIndexPage")
        self.spider.downloadIndexPage()

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


