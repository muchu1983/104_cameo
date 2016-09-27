# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from subprocess import call
"""
以 shell script 執行 sikuli
透過 sikuli 將 HTML 抓取到 source_html 下
"""
class SpiderForCRUNCHBASE:
    
    #建構子
    def __init__(self):
        self.dicSubCommandHandler = {
            "search_funding_rounds":self.handleSearchFundingRoundsPage,
            "search_investors":self.handleSearchInvestorsPage,
            "organization":self.handleOrganizationPage,
        }
        self.strSikuliFolderPath = r"cameo_sikuli\spiderForCRUNCHBASE_chrome.sikuli"
    
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
        call(
            [
                r"cameo_sikuli\runsikulix.cmd", "-c",
                r"-r", self.strSikuliFolderPath,
                r"--args", r"project", arg1
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