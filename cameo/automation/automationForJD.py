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
from cameo.spiderForJD import SpiderForJD
from cameo.parserForJD import ParserForJD
from cameo.importerForJD import ImporterForJD
"""
JD 自動化 抓取 解析 匯入
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    cameoUtility = Utility()
    filesysUtility = FileSystemUtility()
    spider = SpiderForJD()
    parser = ParserForJD()
    importer = ImporterForJD()
    strSettingsJsonFilePath = filesysUtility.getPackageResourcePath(strPackageName="cameo.automation", strResourceName="automationForJD_settings.json")
    dicSettings = cameoUtility.readObjectFromJsonFile(strJsonFilePath=strSettingsJsonFilePath)
    try:
        spider.runSpider(["index"])
        parser.runParser(["index"])
        spider.runSpider(["category"])
        parser.runParser(["category"])
        spider.runSpider(["project"])
        parser.runParser(["project"])
        spider.runSpider(["funder"])
        parser.runParser(["funder"])
        importer.importJsonData()
        cameoUtility.sendEmail(
            strSubject="SUCCESS!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg="",
            lstStrTarget=dicSettings["lstStrMail"]
        )
    except Exception as e:
        logging.warning("automation for JD fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
        
if __name__ == "__main__":
    entry_point()