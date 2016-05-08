# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo_api.spiderForYahooCurrency import SpiderForYahooCurrency
"""
測試抓取 https://tw.money.yahoo.com/currency 即時匯率
"""
class SpiderForYahooCurrencyTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForYahooCurrency()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()

    #測試 取得 匯率 json
    def test_updateCurrencyHtml(self):
        logging.info("SpiderForYahooCurrencyTest.test_updateCurrencyHtml")
        self.spider.updateCurrencyData()
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


