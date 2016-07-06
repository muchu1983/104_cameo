# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.mongoDbRepairman import MongoDbRepairman

"""
測試 mongoDB 維護工作
"""

class MongoViewMakerTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.repairman = MongoDbRepairman()
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 建立 ViewSyndicateAndStartup
    def test_repair(self):
        logging.info("MongoViewMakerTest.test_repair")
        #self.viewMaker.makeViewSyndicateAndStartup() #已廢棄
        self.repairman.makeViewStartupAndInvestment()
        self.repairman.makeViewStartupAndSeries()
        #self.repairman.replaceNullStrCurrencyToEmptyString()


#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


