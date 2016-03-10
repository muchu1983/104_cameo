# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.utility import Utility
"""
測試 Utility
"""

class UtilityTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.utility = Utility()
        
    #收尾
    def tearDown(self):
        pass

    #測試 轉換數字字串為純數字
    def test_translateNumTextToPureNum(self):
        logging.info("UtilityTest.test_translateNumTextToPureNum")
        self.assertEquals(self.utility.translateNumTextToPureNum("26.3K"), 26300)
        self.assertEquals(self.utility.translateNumTextToPureNum("26.3M"), 26300000)
        self.assertEquals(self.utility.translateNumTextToPureNum("26.3"), 26)
        self.assertEquals(self.utility.translateNumTextToPureNum("0.3k"), 300)
        
    #測試 取得國家所屬的洲名稱
    def test_getContinentByCountryName(self):
        self.assertEquals("Asia", self.utility.getContinentByCountryName("JaPaN"))
        self.assertEquals("North America", self.utility.getContinentByCountryName("United sTaTeS"))
        self.assertEquals("Europe", self.utility.getContinentByCountryName("UnIted Kingdom"))
        self.assertEquals("Europe", self.utility.getContinentByCountryName("Sweden"))
        self.assertEquals("Europe", self.utility.getContinentByCountryName("Slovenia"))
        
    #測試 geopy
    def test_geopy(self):
        self.utility.geopy()

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


