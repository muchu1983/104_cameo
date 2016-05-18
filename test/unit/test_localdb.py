# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.localdb import LocalDbForCurrencyApi
from cameo.localdb import LocalDbForTECHORANGE
from cameo.localdb import LocalDbForBNEXT
from cameo.localdb import LocalDbForPEDAILY
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
        
    #測試 幣別轉換API 本地端資料庫存取
    def test_localdb_for_currency_api(self):
        self.db = LocalDbForCurrencyApi()
        logging.info("LocalDbTest.test_getMongoDbClient")
        self.assertIsNotNone(self.db.mongodb)

    #測試 techorange 本地端資料庫存取
    def test_localdb_for_techorange(self):
        logging.info("LocalDbTest.test_localdb_for_techorange")
        db = LocalDbForTECHORANGE()
        db.clearTestData() #清除前次測試資料
        db.insertTagIfNotExists(strTagName="tag_for_unit_test")
        self.assertEquals(db.fetchallNotObtainedTagName()[0], "tag_for_unit_test")
        db.updateTagStatusIsGot(strTagName="tag_for_unit_test")
        self.assertEquals(db.fetchallCompletedObtainedTagName()[0], "tag_for_unit_test")
        db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl="http://news/for/unit/test", strTagName="tag_for_unit_test")
        self.assertEquals(db.fetchallNewsUrlByTagName(strTagName="tag_for_unit_test")[0], "http://news/for/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.updateNewsStatusIsGot(strNewsUrl="http://news/for/unit/test")
        self.assertTrue(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.clearTestData() #清除本次測試資料
        
    #測試 bnext 本地端資料庫存取
    def test_localdb_for_bnext(self):
        logging.info("LocalDbTest.test_localdb_for_bnext")
        db = LocalDbForBNEXT()
        db.clearTestData() #清除前次測試資料
        db.insertTagIfNotExists(strTagName="tag_for_unit_test")
        self.assertEquals(db.fetchallNotObtainedTagName()[0], "tag_for_unit_test")
        db.updateTagStatusIsGot(strTagName="tag_for_unit_test")
        self.assertEquals(db.fetchallCompletedObtainedTagName()[0], "tag_for_unit_test")
        db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl="http://news/for/unit/test", strTagName="tag_for_unit_test")
        self.assertEquals(db.fetchallNewsUrlByTagName(strTagName="tag_for_unit_test")[0], "http://news/for/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.updateNewsStatusIsGot(strNewsUrl="http://news/for/unit/test")
        self.assertTrue(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.clearTestData() #清除本次測試資料
        
    #測試 pedaily 本地端資料庫存取
    def test_localdb_for_pedaily(self):
        logging.info("LocalDbTest.test_localdb_for_pedaily")
        db = LocalDbForPEDAILY()
        db.clearTestData() #清除前次測試資料
        db.insertCategoryIfNotExists(strCategoryName="category_for_unit_test")
        self.assertEquals(db.fetchallNotObtainedCategoryName()[0], "category_for_unit_test")
        db.updateCategoryStatusIsGot(strCategoryName="category_for_unit_test")
        self.assertEquals(db.fetchallCompletedObtainedCategoryName()[0], "category_for_unit_test")
        db.insertNewsUrlIfNotExists(strNewsUrl="http://news/for/unit/test", strCategoryName="category_for_unit_test")
        self.assertEquals(db.fetchallNewsUrlByCategoryName(strCategoryName="category_for_unit_test")[0], "http://news/for/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.updateNewsStatusIsGot(strNewsUrl="http://news/for/unit/test")
        self.assertTrue(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        self.assertEquals(db.fetchallCompletedObtainedNewsUrl(), ["http://news/for/unit/test"])
        db.updateNewsStatusIsNotGot(strNewsUrl="http://news/for/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.clearTestData() #清除本次測試資料

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


