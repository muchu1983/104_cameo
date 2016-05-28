# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo_api.spiderForTwExchangeRates import SpiderForTwExchangeRates
"""
測試抓取 http://tw.exchange-rates.org/ 即時匯率
"""
class SpiderForTwExchangeRatesTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.spider = SpiderForTwExchangeRates()
        self.spider.initDriver()
        
    #收尾
    def tearDown(self):
        self.spider.quitDriver()

    #測試 自動更新 匯率資料
    def test_updateExRateData(self):
        logging.info("SpiderForTwExchangeRatesTest.test_updateExRateData")
        self.spider.updateExRateData()
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


