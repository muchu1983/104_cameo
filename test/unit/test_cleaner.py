# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.cleaner import CleanerForINDIEGOGO
"""
測試 清理不需要的資料
"""

class CleanerTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.cINDIEGOGO = CleanerForINDIEGOGO()
        
    #收尾
    def tearDown(self):
        pass

    #測試 清理 indiegogo 
    def test_cleanIndiegogo(self):
        logging.info("CleanerTest.test_cleanIndiegogo")
        self.cINDIEGOGO.clean()

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


