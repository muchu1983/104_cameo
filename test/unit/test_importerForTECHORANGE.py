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
from cameo.importerForTECHORANGE import ImporterForTECHORANGE
"""
測試 將科技報橘 news.json 資料 import 至 DB
"""
class ImporterForTECHORANGETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.importer = ImporterForTECHORANGE()
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 import news.json to db
    def test_import(self):
        self.importer.importNewsJsonToDb()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


