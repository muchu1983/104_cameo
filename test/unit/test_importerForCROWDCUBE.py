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
from cameo.importerForCROWDCUBE import ImporterForCROWDCUBE
"""
測試 CROWDCUBE json 資料 import 至 DB
"""
class ImporterForCROWDCUBETest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.importer = ImporterForCROWDCUBE()
        
    #收尾
    def tearDown(self):
        pass
    
    #測試 import json to db
    def test_import(self):
        logging.info("ImporterForCROWDCUBETest.test_import")
        self.importer.importJsonData()
    
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


