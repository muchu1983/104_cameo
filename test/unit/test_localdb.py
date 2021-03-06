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
from cameo.localdb import LocalDbForINSIDE
from cameo.localdb import LocalDbForTECHCRUNCH
from cameo.localdb import LocalDbForJD
from cameo.localdb import LocalDbForCROWDCUBE
from cameo.localdb import LocalDbForCRUNCHBASE
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
    """
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
        db.updateNewsStatusIsNotGot(strNewsUrlPart="/for/unit")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
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
    
    #測試 inside 本地端資料庫存取
    def test_localdb_for_inside(self):
        logging.info("LocalDbTest.test_localdb_for_inside")
        db = LocalDbForINSIDE()
        db.clearTestData() #清除前次測試資料
        db.insertTagIfNotExists(strTagPage1Url="http://tag_for_unit_test/p1")
        self.assertEquals(db.fetchallNotObtainedTagPage1Url()[0], "http://tag_for_unit_test/p1")
        db.updateTagStatusIsGot(strTagPage1Url="http://tag_for_unit_test/p1")
        self.assertEquals(db.fetchallCompletedObtainedTagPage1Url()[0], "http://tag_for_unit_test/p1")
        db.insertNewsUrlAndNewsTagMappingIfNotExists(strNewsUrl="http://news/for/unit/test", strTagPage1Url="http://tag_for_unit_test/p1")
        self.assertEquals(db.fetchallNewsUrlByTagPage1Url(strTagPage1Url="http://tag_for_unit_test/p1")[0], "http://news/for/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.updateNewsStatusIsGot(strNewsUrl="http://news/for/unit/test")
        self.assertTrue(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.updateNewsStatusIsNotGot(strNewsUrlPart="/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.clearTestData() #清除本次測試資料
    
    #測試 techcrunch 本地端資料庫存取
    def test_localdb_for_techcrunch(self):
        logging.info("LocalDbTest.test_localdb_for_techcrunch")
        db = LocalDbForTECHCRUNCH()
        db.clearTestData() #清除前次測試資料
        db.insertTopicIfNotExists(strTopicPage1Url="http://topic_for_unit_test")
        self.assertEquals(db.fetchallNotObtainedTopicUrl()[0], "http://topic_for_unit_test")
        db.updateTopicStatusIsGot(strTopicPage1Url="http://topic_for_unit_test")
        self.assertEquals(db.fetchallCompletedObtainedTopicUrl()[0], "http://topic_for_unit_test")
        db.insertNewsUrlIfNotExists(strNewsUrl="http://news/for/unit/test", strTopicPage1Url="http://topic_for_unit_test")
        self.assertEquals(db.fetchallNewsUrlByTopicUrl(strTopicPage1Url="http://topic_for_unit_test")[0], "http://news/for/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.updateNewsStatusIsGot(strNewsUrl="http://news/for/unit/test")
        self.assertTrue(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        self.assertEquals(db.fetchallCompletedObtainedNewsUrl(), ["http://news/for/unit/test"])
        db.updateNewsStatusIsNotGot(strNewsUrl="http://news/for/unit/test")
        self.assertFalse(db.checkNewsIsGot(strNewsUrl="http://news/for/unit/test"))
        db.clearTestData() #清除本次測試資料
    
    #測試 京東眾籌 本地端資料庫存取
    def test_localdb_for_jd(self):
        logging.info("LocalDbTest.test_localdb_for_jd")
        db = LocalDbForJD()
        db.clearTestData() #清除前次測試資料
        db.insertCategoryIfNotExists(strCategoryPage1Url="http://category_for_unit_test", strCategoryName="category_for_unit_test")
        self.assertEquals(db.fetchCategoryNameByUrl(strCategoryPage1Url="http://category_for_unit_test"), "category_for_unit_test")
        self.assertEquals(db.fetchallNotObtainedCategoryUrl()[0], "http://category_for_unit_test")
        db.updateCategoryStatusIsGot(strCategoryPage1Url="http://category_for_unit_test")
        self.assertEquals(db.fetchallCompletedObtainedCategoryUrl()[0], "http://category_for_unit_test")
        db.insertProjectUrlIfNotExists(strProjectUrl="http://project/for/unit/test", strCategoryPage1Url="http://category_for_unit_test")
        db.insertFunderUrlIfNotExists(strFunderUrl="http://funder/for/unit/test", strCategoryPage1Url="http://category_for_unit_test")
        self.assertEquals(db.fetchallProjectUrlByCategoryUrl(strCategoryPage1Url="http://category_for_unit_test")[0], "http://project/for/unit/test")
        self.assertEquals(db.fetchallFunderUrlByCategoryUrl(strCategoryPage1Url="http://category_for_unit_test")[0], "http://funder/for/unit/test")
        self.assertFalse(db.checkProjectIsGot(strProjectUrl="http://project/for/unit/test"))
        self.assertFalse(db.checkFunderIsGot(strFunderUrl="http://funder/for/unit/test"))
        db.updateProjectStatusIsGot(strProjectUrl="http://project/for/unit/test")
        db.updateFunderStatusIsGot(strFunderUrl="http://funder/for/unit/test")
        self.assertTrue(db.checkProjectIsGot(strProjectUrl="http://project/for/unit/test"))
        self.assertTrue(db.checkFunderIsGot(strFunderUrl="http://funder/for/unit/test"))
        self.assertEquals(db.fetchallCompletedObtainedProjectUrl(), ["http://project/for/unit/test"])
        self.assertEquals(db.fetchallCompletedObtainedFunderUrl(), ["http://funder/for/unit/test"])
        db.updateProjectStatusIsNotGot(strProjectUrl="http://project/for/unit/test")
        db.updateFunderStatusIsNotGot(strFunderUrl="http://funder/for/unit/test")
        self.assertFalse(db.checkProjectIsGot(strProjectUrl="http://project/for/unit/test"))
        self.assertFalse(db.checkFunderIsGot(strFunderUrl="http://funder/for/unit/test"))
        db.clearTestData() #清除本次測試資料
    
    #測試 crowdcube 本地端資料庫存取
    def test_localdb_for_crowdcube(self):
        logging.info("LocalDbTest.test_localdb_for_crowdcube")
        db = LocalDbForCROWDCUBE()
        db.clearTestData() #清除前次測試資料
        db.insertAccountIfNotExists(strEmail="ebucdworc+0100@gmail.com", strPassword="bee520")
        db.insertAccountIfNotExists(strEmail="ebucdworc+0101@gmail.com", strPassword="bee520")
        (strAccountEmail, strAccountPassword) = db.fetchRandomReadyAccount()
        self.assertTrue(strAccountEmail.startswith("ebucdworc"))
        db.insertCompanyUrlIfNotExists(strCompanyUrl="http://company/for/unit/test")
        self.assertEquals(db.fetchallNotObtainedCompanyUrl(), ["http://company/for/unit/test"])
        self.assertFalse(db.checkCompanyIsGot(strCompanyUrl="http://company/for/unit/test"))
        db.updateCompanyStatusIsGot(strCompanyUrl="http://company/for/unit/test")
        self.assertTrue(db.checkCompanyIsGot(strCompanyUrl="http://company/for/unit/test"))
        self.assertEquals(db.fetchallCompletedObtainedCompanyUrl(), ["http://company/for/unit/test"])
        db.updateCompanyStatusIsNotGot(strCompanyUrl="http://company/for/unit/test")
        self.assertFalse(db.checkCompanyIsGot(strCompanyUrl="http://company/for/unit/test"))
        db.clearTestData() #清除本次測試資料
    """
    #測試 crunchbase 本地端資料庫存取
    def test_localdb_for_crunchbase(self):
        logging.info("LocalDbTest.test_localdb_for_crunchbase")
        db = LocalDbForCRUNCHBASE()
        db.clearTestData() #清除前次測試資料
        db.insertAccountIfNotExists(strEmail="esabhcnurc+0100@gmail.com", strPassword="bee520")
        db.insertAccountIfNotExists(strEmail="esabhcnurc+0101@gmail.com", strPassword="bee520")
        (strAccountEmail, strAccountPassword) = db.fetchRandomReadyAccount()
        self.assertTrue(strAccountEmail.startswith("esabhcnurc"))
        db.insertOrganizationUrlIfNotExists(strOrganizationUrl="http://organization/for/unit/test")
        self.assertEquals(db.fetchallNotObtainedOrganizationUrl(), ["http://organization/for/unit/test"])
        self.assertFalse(db.checkOrganizationIsGot(strOrganizationUrl="http://organization/for/unit/test"))
        db.updateOrganizationStatusIsGot(strOrganizationUrl="http://organization/for/unit/test")
        self.assertTrue(db.checkOrganizationIsGot(strOrganizationUrl="http://organization/for/unit/test"))
        self.assertEquals(db.fetchallCompletedObtainedOrganizationUrl(), ["http://organization/for/unit/test"])
        db.updateOrganizationStatusIsNotGot(strOrganizationUrl="http://organization/for/unit/test")
        self.assertFalse(db.checkOrganizationIsGot(strOrganizationUrl="http://organization/for/unit/test"))
        db.clearTestData() #清除本次測試資料
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


