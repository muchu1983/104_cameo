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
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForWEBACKERS:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.dicSubCommandHandler = {"category":[self.parseCategoryPage],
                                     "project":[self.beforeParseProjectPage,
                                                self.parseIntroPage,
                                                self.afterParseProjectPage],
                                     "profile":[]}
        self.strWebsiteDomain = u"https://www.webackers.com"
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"cameo_res\\source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"cameo_res\\parsed_result"
        self.dicParsedResultOfCategory = {} #category.json 資料
        self.dicParsedResultOfProject = {} #project.json 資料
        self.dicParsedResultOfUpdate = {} #update.json 資料
        self.dicParsedResultOfComment = {} #comment.json 資料
        self.dicParsedResultOfReward = {} #reward.json 資料
        self.dicParsedResultOfProfile = {} #profile.json 資料
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return ("- WEBACKERS -\n"
                "useage:\n"
                "category - parse #_category.html then create project_url_list.txt\n"
                "project category - parse project's html of given category then create .json\n"
                "profile category - parse profile's html of given category then create .json\n")

    #執行 parser
    def runParser(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)

#category #####################################################################################
    #解析 category.html
    def parseCategoryPage(self, uselessArg1=None):
        strBrowseResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"\\WEBACKERS"
        strBrowseHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"\\WEBACKERS"
        lstStrCategoryHtmlFolderPath = self.utility.getSubFolderPathList(strBasedir=strBrowseHtmlFolderPath)
        for strCategoryHtmlFolderPath in lstStrCategoryHtmlFolderPath: #各分類子資料夾
            strCategoryResultFolderPath = strBrowseResultFolderPath + u"\\%s"%re.match("^.*WEBACKERS\\\\([a-z]*)$", strCategoryHtmlFolderPath).group(1)
            if not os.path.exists(strCategoryResultFolderPath):
                os.mkdir(strCategoryResultFolderPath) #mkdir parsed_result/WEBACKERS/category/
            strCategoryJsonFilePath = strCategoryResultFolderPath + u"\\category.json"
            #清空 dicParsedResultOfCategory 資料
            self.dicParsedResultOfCategory = {}
            self.dicParsedResultOfCategory["project_url_list"] = []
            self.dicParsedResultOfCategory["profile_url_list"] = []
            #解析各頁的 category.html 並將 url 集合於 json 檔案裡
            lstStrCategoryHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strCategoryHtmlFolderPath, strSuffixes=u"category.html")
            for strCategoryHtmlFilePath in lstStrCategoryHtmlFilePath: #category.html 各分頁
                with open(strCategoryHtmlFilePath, "r") as categoryHtmlFile:
                    strPageSource = categoryHtmlFile.read()
                    root = Selector(text=strPageSource)
                    #開始解析
                    lstStrProjectUrl = root.css("li.cbp-item div.thumbnail > a:first-of-type::attr(href)").extract()
                    lstStrProfileUrl = root.css("li.cbp-item div.thumbnail a.pull-left::attr(href)").extract()
                    #寫入 url
                    for strProjectUrl in lstStrProjectUrl:
                        #儲存在 category.html 下的 project 資料
                        dicProjectData = {}
                        #strUrl
                        strFullProjectUrl = self.strWebsiteDomain + strProjectUrl
                        dicProjectData["strUrl"] = strFullProjectUrl
                        #strDescription
                        strDescription = None
                        elesDivThumbnail = root.css("div.thumbnail")
                        for eleDivThumbnail in elesDivThumbnail:
                            if len(eleDivThumbnail.css("a[href='%s']"%strProjectUrl)) != 0:
                                strDescription = eleDivThumbnail.css("div.caption_view p::text").extract_first()
                        dicProjectData["strDescription"] = strDescription
                        self.dicParsedResultOfCategory["project_url_list"].append(dicProjectData)
                    for strProfileUrl in lstStrProfileUrl:
                        strFullProfileUrl = self.strWebsiteDomain + strProfileUrl
                        self.dicParsedResultOfCategory["profile_url_list"].append(strFullProfileUrl)
            self.utility.writeObjectToJsonFile(self.dicParsedResultOfCategory, strCategoryJsonFilePath)
#project #####################################################################################
    #解析 project page(s) 之前
    def beforeParseProjectPage(self, strCategoryName=None):
        strProjectsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\WEBACKERS\\%s\\projects"%strCategoryName)
        if not os.path.exists(strProjectsResultFolderPath):
            #mkdir parsed_result/WEBACKERS/category/projects/
            os.mkdir(strProjectsResultFolderPath)
            
    #解析 project page(s) 之後
    def afterParseProjectPage(self, strCategoryName=None):
        strProjectsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\WEBACKERS\\%s\\projects"%strCategoryName)
        #將 parse 結果寫入 json 檔案
        self.utility.writeObjectToJsonFile(self.dicParsedResultOfProject, strProjectsResultFolderPath + u"\\project.json")
        
    #解析 intro.html
    def parseIntroPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"\\WEBACKERS\\%s\\projects"%strCategoryName)
        lstStrIntroHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_intro.html")
        for strProjectIntroHtmlFilePath in lstStrIntroHtmlFilePath:
            logging.info("parsing %s"%strProjectIntroHtmlFilePath)
            with open(strProjectIntroHtmlFilePath, "r") as projectIntroHtmlFile:
                strProjHtmlFileName = os.path.basename(projectIntroHtmlFile.name)
                #取得 url
                strProjId = re.search("^(.*)_intro.html$", strProjHtmlFileName).group(1)
                strProjUrl = u"https://www.webackers.com/Proposal/Display/" + strProjId
                if strProjUrl not in self.dicParsedResultOfProject:
                    self.dicParsedResultOfProject[strProjUrl] = {}
                #取得 category 頁面的 project 資料
                strCategoryJsonFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\WEBACKERS\\%s\\category.json"%strCategoryName)
                dicCategoryData = self.utility.readObjectFromJsonFile(strJsonFilePath=strCategoryJsonFilePath)
                #開始解析
                strPageSource = projectIntroHtmlFile.read()
                root = Selector(text=strPageSource)
                #strSource
                self.dicParsedResultOfProject[strProjUrl]["strSource"] = \
                    u"WEBACKERS"
                #strUrl
                self.dicParsedResultOfProject[strProjUrl]["strUrl"] = \
                    strProjUrl
                #strProjectName
                self.dicParsedResultOfProject[strProjUrl]["strProjectName"] = \
                    root.css("a[href*='%s'] span.case_title::text"%strProjId).extract_first().strip()
                #strLocation
                self.dicParsedResultOfProject[strProjUrl]["strLocation"] = u"Taiwan"
                #strCountry
                self.dicParsedResultOfProject[strProjUrl]["strCountry"] = u"ROC"
                #strContinent
                self.dicParsedResultOfProject[strProjUrl]["strContinent"] = u"Asia"
                #strDescription
                strDescription = None
                for dicProjectData in dicCategoryData["project_url_list"]:
                    if dicProjectData["strUrl"] == strProjUrl:
                        strDescription = dicProjectData["strDescription"]
                self.dicParsedResultOfProject[strProjUrl]["strDescription"] = strDescription
                #strIntroduction
        
##project.json
#intStatus
#strCreator
#strCreatorUrl
#intVideoCount
#intImageCount
#isPMSelect
#strCategory
#strSubCategory
#fFundProgress
#intFundTarget
#intRaisedMoney
#strCurrency
#intBacker
#intRemainDays
#strEndDate
#strStartDate
#intComment
#intUpdate
#lstStrBacker
#intFbLike
##reward.json
#strUrl
#strRewardContent
#intRewardMoney
#intRewardBacker
#intRewardLimit
#strRewardDeliveryDate
#strRewardShipTo
#intRewardRetailPrice
##update.json
#strUrl
#strUpdateTitle
#strUpdateContent
#strUpdateDate
##comment.json
#strUrl
#strQnaQuestion
#strQnaAnswer
#strQnaDate

#profile #####################################################################################
##profile.json
#strName
#strDescription
#strLocation
#strCountry
#strContinent
#lstStrSocialNetwork
#lstStrCreatedProject
#lstStrCreatedProjectUrl
#lstStrBackedProject
#lstStrBackedProjectUrl
#intBackedCount
#intCreatedCount
#isCreator
#isBacker
#intLiveProject
#intSuccessProject
#intFailedProject
#strIdentityName
#strLastLoginDate
#intFbFriends