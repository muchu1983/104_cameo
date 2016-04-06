# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.localdb import LocalDbForTECHORANGE
"""
測試 本地端資料庫存取
"""
class LocalDbTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        pass

    #測試 techorange 本地端資料庫存取
    def test_localdb_for_techorange(self):
        logging.info("LocalDbTest.test_localdb_for_techorange")
        db = LocalDbForTECHORANGE()
        db.insertTagIfNotExists(strTagName="tag_for_unit_test")
        db.fetchallNotObtainedTagName()
        db.updateTagStatusIsGot(strTagName="tag_for_unit_test")
        db.fetchallCompletedObtainedTagName()
        db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl="http://news/for/unit/test", strTagName="tag_for_unit_test")
        db.fetchallNewsUrlByTagName(strTagName="tag_for_unit_test")

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


