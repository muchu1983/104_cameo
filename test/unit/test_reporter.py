# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.reporter import ReporterForINDIEGOGO
from cameo.reporter import ReporterForWEBACKERS
"""
測試 建立報告
"""
class ReporterTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.rINDIEGOGO = ReporterForINDIEGOGO()
        self.rWEBACKERS = ReporterForWEBACKERS()
        
    #收尾
    def tearDown(self):
        pass

    #測試 建立 indiegogo 報告
    def test_reportIndiegogo(self):
        logging.info("ReporterTest.test_reportIndiegogo")
        self.rINDIEGOGO.CountDownloadedProject()
        self.rINDIEGOGO.CountParsedProject()
        
    #測試 建立 webackers 報告
    def test_reportWebackers(self):
        logging.info("ReporterTest.test_reportWebackers")

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


