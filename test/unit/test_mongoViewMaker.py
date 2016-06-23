# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.mongoViewMaker import MongoViewMaker

"""
測試 建立 mongo db 的 view 表格
"""

class MongoViewMakerTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.viewMaker = MongoViewMaker()
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 建立 ViewSyndicateAndStartup
    def test_makeViewSyndicateAndStartup(self):
        logging.info("MongoViewMakerTest.test_makeViewSyndicateAndStartup")
        self.viewMaker.makeViewSyndicateAndStartup()


#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


