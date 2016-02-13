# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import scrapy
"""
測試
"""
class ScrapyTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 scrapy
    def test_scrapy(self):
        logging.info("ScrapyTest.test_scrapy")

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


