# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import datetime
import re
import json
import logging
from scrapy import Selector
from cameo.utility import Utility
from cameo.localdb import LocalDbForCRUNCHBASE
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForCRUNCHBASE:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = LocalDbForCRUNCHBASE()
        self.dicSubCommandHandler = {
            "search_funding_rounds":[self.parseSearchFundingRoundsPage],
            "search_investors":[self.parseSearchInvestorsPage],
            "organization":[self.parseOrganizationPage],
        }
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfProject = {} #project.json 資料
        self.dicParsedResultOfUpdate = {} #update.json 資料
        self.dicParsedResultOfComment = {} #comment.json 資料
        self.dicParsedResultOfReward = {} #reward.json 資料
        self.dicParsedResultOfProfile = {} #profile.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return ("- CRUNCHBASE -\n"
                "useage:\n"
                "search_funding_rounds - parse funding_rounds.html then insert organization url to localdb \n"
                "search_investors - parse investors.html then insert organization url to localdb \n"
                "organization - parse organization.html then create .json \n")

    #執行 parser
    def runParser(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)
#funding rounds #####################################################################################
    #解析 funding_rounds.html
    def parseSearchFundingRoundsPage(self, uselessArg1=None):
        strFundingRoundsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        lstStrFundingRoundsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strFundingRoundsHtmlFolderPath, strSuffixes="funding_rounds.html")
        strFundingRoundsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        if not os.path.exists(strFundingRoundsResultFolderPath):
            os.mkdir(strFundingRoundsResultFolderPath) #mkdir parsed_result/CRUNCHBASE/
        for strFundingRoundsHtmlFilePath in lstStrFundingRoundsHtmlFilePath:
            with open(strFundingRoundsHtmlFilePath, "r") as fundingRoundsHtmlFile:
                strPageSource = fundingRoundsHtmlFile.read()
            root = Selector(text=strPageSource)
            lstStrOrganizationUrl = root.css("div.cbRow div.cbCell:nth-of-type(3) span.identifier a.cb-link::attr(href)").extract()
            for strOrganizationUrl in lstStrOrganizationUrl:
                self.db.insertOrganizationUrlIfNotExists(strOrganizationUrl=strOrganizationUrl)
#investors #####################################################################################
    #解析 investors.html
    def parseSearchInvestorsPage(self, uselessArg1=None):
        strInvestorsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        lstStrInvestorsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strInvestorsHtmlFolderPath, strSuffixes="investors.html")
        strInvestorsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\CRUNCHBASE"
        if not os.path.exists(strInvestorsResultFolderPath):
            os.mkdir(strInvestorsResultFolderPath) #mkdir parsed_result/CRUNCHBASE/
        for strInvestorsHtmlFilePath in lstStrInvestorsHtmlFilePath:
            with open(strInvestorsHtmlFilePath, "r") as investorsHtmlFile:
                strPageSource = investorsHtmlFile.read()
            root = Selector(text=strPageSource)
            lstStrOrganizationUrl = root.css("TODO").extract()
            for strOrganizationUrl in lstStrOrganizationUrl:
                self.db.insertOrganizationUrlIfNotExists(strOrganizationUrl=strOrganizationUrl)
#organization #####################################################################################
    #解析 organization page 進入點
    def parseOrganizationPage(self, uselessArg1=None):
        lstFuncOfParseOrganization = [
            self.beforeParseOrganizationPage,
            self.parseOrganizationHtmlPage,
            self.afterParseOrganizationPage
        ]
        for funcOfParseOrganization in lstFuncOfParseOrganization:
            funcOfParseOrganization()
    #解析 organization page 之前
    def beforeParseOrganizationPage(self):
        self.dicParsedResultOfProject = {} #project.json 資料
        self.dicParsedResultOfUpdate = {} #update.json 資料
        self.dicParsedResultOfComment = {} #comment.json 資料
        self.dicParsedResultOfReward = {} #reward.json 資料
        strProjectsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\INDIEGOGO\\%s\\projects"%strCategoryName)
        if not os.path.exists(strProjectsResultFolderPath):
            #mkdir parsed_result/INDIEGOGO/category/projects/
            os.mkdir(strProjectsResultFolderPath)
            
    #解析 organization page 之後
    def afterParseOrganizationPage(self):
        strProjectsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\INDIEGOGO\\%s\\projects"%strCategoryName)
        #將 parse 結果寫入 json 檔案
        self.utility.writeObjectToJsonFile(self.dicParsedResultOfProject, strProjectsResultFolderPath + u"\\project.json")
        self.utility.writeObjectToJsonFile(self.dicParsedResultOfUpdate, strProjectsResultFolderPath + u"\\update.json")
        self.utility.writeObjectToJsonFile(self.dicParsedResultOfComment, strProjectsResultFolderPath + u"\\comment.json")
        self.utility.writeObjectToJsonFile(self.dicParsedResultOfReward, strProjectsResultFolderPath + u"\\reward.json")
        
    #解析 organization.html
    def parseOrganizationHtmlPage(self):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"\\INDIEGOGO\\%s\\projects"%strCategoryName)
        lstStrDetailsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_details.html")
        for strProjectDetailsHtmlPath in lstStrDetailsHtmlFilePath:
            logging.info("parsing %s"%strProjectDetailsHtmlPath)
            with open(strProjectDetailsHtmlPath, "r") as projDetailsHtmlFile: #open *_details.html
                strProjHtmlFileName = os.path.basename(projDetailsHtmlFile.name)
                strProjUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_details.html$", strProjHtmlFileName).group(1)
                if not self.checkIsProjUrlInProjUrlListFile(strCategoryName=strCategoryName, strProjUrl=strProjUrl):
                    logging.warning("%s not in project_url_list.txt, skip parse it"%strProjUrl)
                    continue #skip
                if strProjUrl not in self.dicParsedResultOfProject:
                    self.dicParsedResultOfProject[strProjUrl] = {}
                strPageSource = projDetailsHtmlFile.read()
                root = Selector(text=strPageSource)
                #parse *_details.html
                #strCreatorUrl
                strIndividualsUrl = root.css("div.campaignTrustPassportDesktop-ownerInfo a.ng-binding[href*='individuals']::attr(href)").extract_first() #parse individuals url
                self.dicParsedResultOfProject[strProjUrl]["strCreatorUrl"] = strIndividualsUrl
                # append url to parsed_result/*/category/individuals_url_list.txt
                strIndividualsUrlListFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\INDIEGOGO\\%s\\individuals_url_list.txt"%(strCategoryName))
                lstStrExistsIndividualsUrl = []
                if os.path.exists(strIndividualsUrlListFilePath):
                    with open(strIndividualsUrlListFilePath, "r") as individualsUrlListFile:
                        lstStrExistsIndividualsUrl = individualsUrlListFile.readlines()
                if strIndividualsUrl+u"\n" not in lstStrExistsIndividualsUrl:#檢查有無重覆的 individuals url
                    with open(strIndividualsUrlListFilePath, "a") as individualsUrlListFile:
                        individualsUrlListFile.write(strIndividualsUrl + u"\n") #append url to individuals_url_list.txt
