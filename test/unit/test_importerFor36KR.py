# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import json
from cameo.importerFor36KR import ImporterFor36KR
"""
測試 將 36kr news.json 資料 import 至 DB
"""
class ImporterFor36KRTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.importer = ImporterFor36KR()
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 import news.json to db
    def test_import(self):
        logging.info("ImporterFor36KRTest.test_import")
        self.importer.importNewsJsonToDb()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


