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
from subprocess import call
"""
測試 操作 scrapy
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
    def test_call_scrapy(self):
        logging.info("ScrapyTest.test_call_scrapy")
        call(["scrapy", "crawl", "yahoo"], cwd=".")

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


