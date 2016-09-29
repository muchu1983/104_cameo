# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
from subprocess import call
from cameo.localdb import LocalDbForCRUNCHBASE
from cameo.utility import Utility
"""
以 shell script 執行 sikuli
透過 sikuli 將 HTML 抓取到 source_html 下
"""
class SpiderForCRUNCHBASE:
    
    #建構子
    def __init__(self):
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicSubCommandHandler = {
            "search_funding_rounds":self.handleSearchFundingRoundsPage,
            "search_investors":self.handleSearchInvestorsPage,
            "organization":self.handleOrganizationPage,
        }
        self.strSikuliFolderPath = r"cameo_sikuli\spiderForCRUNCHBASE_chrome.sikuli"
        self.db = LocalDbForCRUNCHBASE()
        self.utility = Utility()
    
    #下載 funding rounds 頁面
    def handleSearchFundingRoundsPage(self, arg1=None):
        if arg1:
            call(
                [
                    r"cameo_sikuli\runsikulix.cmd", "-c",
                    r"-r", self.strSikuliFolderPath,
                    r"--args", r"search_funding_rounds", arg1
                ]
            )
        else:
            call(
                [
                    r"cameo_sikuli\runsikulix.cmd", "-c",
                    r"-r", self.strSikuliFolderPath,
                    r"--args", r"search_funding_rounds"
                ]
            )
    
    #下載 investors 頁面
    def handleSearchInvestorsPage(self, arg1=None):
        if arg1:
            call(
                [
                    r"cameo_sikuli\runsikulix.cmd", "-c",
                    r"-r", self.strSikuliFolderPath,
                    r"--args", r"search_investors", arg1
                ]
            )
        else:
            call(
                [
                    r"cameo_sikuli\runsikulix.cmd", "-c",
                    r"-r", self.strSikuliFolderPath,
                    r"--args", r"search_investors"
                ]
            )

    #下載 organization 頁面
    def handleOrganizationPage(self, arg1=None):
        strOrganizationFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\CRUNCHBASE\\organization")
        if not os.path.exists(strOrganizationFolderPath):
            #mkdir parsed_result/CRUNCHBASE/organization/
            os.mkdir(strOrganizationFolderPath)
        lstStrOrganizationUrl = self.db.fetchallNotObtainedOrganizationUrl()
        strOrganizationUrlListFilePath = strOrganizationFolderPath + u"\\organization_url_list.txt"
        #刪除原本的 organization_url_list.txt
        if os.path.exists(strOrganizationUrlListFilePath):
            os.remove(strOrganizationUrlListFilePath)
        #建立新的 organization_url_list.txt
        for strOrganizationUrl in lstStrOrganizationUrl:
            self.utility.appendLineToTxtIfNotExists(strTxtFilePath=strOrganizationUrlListFilePath, strLine=strOrganizationUrl)
        call(
            [
                r"cameo_sikuli\runsikulix.cmd", "-c",
                r"-r", self.strSikuliFolderPath,
                r"--args", r"organization"
            ]
        )
        
    #取得 spider 使用資訊
    def getUseageMessage(self):
        return (
            "- CRUNCHBASE -\n"
            "useage:\n"
            "search_funding_rounds [category]- download category_funding_rounds.html \n"
            "search_investors [category]- download category_investors.html \n"
            "organization - download organization.html \n"
        )
        
    #執行 spider
    def runSpider(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        self.dicSubCommandHandler[strSubcommand](strArg1)