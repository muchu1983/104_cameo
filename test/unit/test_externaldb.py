# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.externaldb import ExternalDbForCurrencyApi
"""
測試 外部資料庫存取
"""
class ExternalDbTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.cameoDb = ExternalDbForCurrencyApi()
        
    #收尾
    def tearDown(self):
        pass

    #測試 currency api 外部資料庫存取
    def test_externaldb_for_currency_api(self):
        logging.info("ExternalDbTest.test_externaldb_for_currency_api")
        self.assertIsNotNone(self.cameoDb.mongodb)
        self.assertTrue(self.cameoDb.mongodb.ModelExRate.find({}).count() > 0)
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


