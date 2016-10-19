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
from cameo.spiderForTECHORANGE import SpiderForTECHORANGE
from cameo.parserForTECHORANGE import ParserForTECHORANGE
from cameo.importerForTECHORANGE import ImporterForTECHORANGE
from cameo.spiderForBNEXT import SpiderForBNEXT
from cameo.parserForBNEXT import ParserForBNEXT
from cameo.importerForBNEXT import ImporterForBNEXT
from cameo.spiderForPEDAILY import SpiderForPEDAILY
from cameo.parserForPEDAILY import ParserForPEDAILY
from cameo.importerForPEDAILY import ImporterForPEDAILY
from cameo.spiderForINSIDE import SpiderForINSIDE
from cameo.parserForINSIDE import ParserForINSIDE
from cameo.importerForINSIDE import ImporterForINSIDE
from cameo.spiderForTECHCRUNCH import SpiderForTECHCRUNCH
from cameo.parserForTECHCRUNCH import ParserForTECHCRUNCH
from cameo.importerForTECHCRUNCH import ImporterForTECHCRUNCH
"""
新聞平台 自動化 抓取 解析 匯入
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    cameoUtility = Utility()
    filesysUtility = FileSystemUtility()
    strSettingsJsonFilePath = filesysUtility.getPackageResourcePath(strPackageName="cameo.automation", strResourceName="automationForALLNEWS_settings.json")
    dicSettings = cameoUtility.readObjectFromJsonFile(strJsonFilePath=strSettingsJsonFilePath)
    #TECHCRUNCH
    try:
        spider = SpiderForTECHCRUNCH()
        parser = ParserForTECHCRUNCH()
        importer = ImporterForTECHCRUNCH()
        spider.runSpider(["index"])
        parser.runParser(["index"])
        spider.runSpider(["topic"])
        parser.runParser(["topic"])
        spider.runSpider(["news"])
        parser.runParser(["json"])
        importer.runImporter(["import"])
        cameoUtility.sendEmail(
            strSubject="SUCCESS!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg="",
            lstStrTarget=dicSettings["lstStrMail"]
        )
    except Exception as e:
        logging.warning("automation for ALLNEWS fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
    #TECHORANGE
    try:
        spider = SpiderForTECHORANGE()
        parser = ParserForTECHORANGE()
        importer = ImporterForTECHORANGE()
        spider.runSpider(["index"])
        parser.runParser(["index"])
        spider.runSpider(["tag"])
        parser.runParser(["tag"])
        spider.runSpider(["news"])
        parser.runParser(["news"])
        spider.runSpider(["tag"])
        parser.runParser(["tag"])
        spider.runSpider(["news"])
        parser.runParser(["json"])
        importer.runImporter(["import"])
    except Exception as e:
        logging.warning("automation for ALLNEWS fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
    #BNEXT
    try:
        spider = SpiderForBNEXT()
        parser = ParserForBNEXT()
        importer = ImporterForBNEXT()
        spider.runSpider(["index"])
        parser.runParser(["index"])
        spider.runSpider(["tag"])
        parser.runParser(["tag"])
        spider.runSpider(["news"])
        parser.runParser(["news"])
        spider.runSpider(["tag"])
        parser.runParser(["tag"])
        spider.runSpider(["news"])
        parser.runParser(["json"])
        importer.runImporter(["import"])
    except Exception as e:
        logging.warning("automation for ALLNEWS fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
    #PEDAILY
    try:
        spider = SpiderForPEDAILY()
        parser = ParserForPEDAILY()
        importer = ImporterForPEDAILY()
        spider.runSpider(["index"])
        parser.runParser(["index"])
        spider.runSpider(["category"])
        parser.runParser(["category"])
        spider.runSpider(["news"])
        parser.runParser(["json"])
        importer.runImporter(["import"])
    except Exception as e:
        logging.warning("automation for ALLNEWS fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
    #INSIDE
    try:
        spider = SpiderForINSIDE()
        parser = ParserForINSIDE()
        importer = ImporterForINSIDE()
        spider.runSpider(["index"])
        parser.runParser(["index"])
        spider.runSpider(["tag"])
        parser.runParser(["tag"])
        spider.runSpider(["news"])
        parser.runParser(["news"])
        spider.runSpider(["tag"])
        parser.runParser(["tag"])
        spider.runSpider(["news"])
        parser.runParser(["json"])
        importer.runImporter(["import"])
    except Exception as e:
        logging.warning("automation for ALLNEWS fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
        
if __name__ == "__main__":
    entry_point()