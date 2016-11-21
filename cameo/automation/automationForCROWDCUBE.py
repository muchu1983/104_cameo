# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from cameo.utility import Utility
from bennu.filesystemutility import FileSystemUtility
from cameo.spiderForCROWDCUBE import SpiderForCROWDCUBE
from cameo.parserForCROWDCUBE import ParserForCROWDCUBE
from cameo.importerForCROWDCUBE import ImporterForCROWDCUBE
"""
CROWDCUBE 自動化 抓取 解析 匯入
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    cameoUtility = Utility()
    filesysUtility = FileSystemUtility()
    spider = SpiderForCROWDCUBE()
    parser = ParserForCROWDCUBE()
    importer = ImporterForCROWDCUBE()
    strSettingsJsonFilePath = filesysUtility.getPackageResourcePath(strPackageName="cameo.automation", strResourceName="automationForCROWDCUBE_settings.json")
    dicSettings = cameoUtility.readObjectFromJsonFile(strJsonFilePath=strSettingsJsonFilePath)
    try:
        spider.runSpider(["companies"])
        parser.runParser(["companies"])
        spider.runSpider(["company"])
        parser.runParser(["company"])
        importer.importJsonData()
        cameoUtility.sendEmail(
            strSubject="SUCCESS!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg="",
            lstStrTarget=dicSettings["lstStrMail"]
        )
    except Exception as e:
        logging.warning("automation for CROWDCUBE fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
        
if __name__ == "__main__":
    entry_point()