# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import datetime
from cameo.monitorUtility import MonitorUtility

"""
測試 monitor utility
"""

class MonitorUtilityTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        pass

    #測試 更新爬蟲 狀態
    def test_updateMonitorStatus(self):
        logging.info("MonitorUtilityTest.test_updateMonitorStatus")
        monitor = MonitorUtility(strIp="210.61.46.64", strCrawlerName="[tier 爬蟲][CrunchBase + Indiegogo]")
        monitor.updateMonitorStatus(
            strIp="210.61.46.64",
            strCrawlerName="[tier 爬蟲][CrunchBase + Indiegogo]",
            strJob="Crawling",
            strCrawlerUrl="https://www.crunchbase.com/organization/groupon",
            dtCrawlerJobTime=datetime.datetime.strptime("2016-11-04 03:59", "%Y-%m-%d %H:%M"),
            dtStratCrawlingTime=datetime.datetime.now(),
            dtParsingTime=datetime.datetime.now(),
            dtImporterTime=datetime.datetime.now(),
            dtUploadingFTPTime=datetime.datetime.now(),
            dtErrorMsgTime=datetime.datetime.now(),
            strErrorMsg=""
        )

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


