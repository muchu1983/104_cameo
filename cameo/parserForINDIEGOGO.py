# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import re
import json
from scrapy import Selector
from cameo.utility import Utility
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForINDIEGOGO:
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.dicSubCommandHandler = {"explore":[self.parseExplorePage],
                                     "category":[self.parseCategoryPage],
                                     "project":[self.beforeParseProjectPage,
                                                self.parseProjectDetailsPage,
                                                self.parseProjectStoryPage,
                                                self.parseProjectUpdatesPage,
                                                self.parseProjectCommentsPage,
                                                self.parseProjectBackersPage,
                                                self.parseProjectRewardPage,
                                                self.parseProjectGalleryPage],
                                     "individuals":[self.beforeParseIndividualsPage,
                                                    self.parseIndividualsProfilePage,
                                                    self.parseIndividualsCampaignsPage],}
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"./cameo_res/source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"./cameo_res/parsed_result"
        self.CATEGORY_URL_LIST_FILENAME = u"category_url_list.txt"
        self.PROJ_URL_LIST_FILENAME = u"_proj_url_list.txt"
        self.dicParsedResultOfProject = {}
        self.dicParsedResultOfUpdate = {}
        self.dicParsedResultOfReward = {}
        self.dicParsedResultOfProfile = {}
        
    #取得 parser 使用資訊
    def getUseageMessage(self):
        return """- INDIEGOGO -
useage:
explore - parse explore.html then create category_url_list.txt
category - parse category.html then create xxx_proj_url_list.txt
project category - parse project.html of category then create xxx.json
individuals category - parse individuals.html of category then create xxx.json
"""

    #執行 parser
    def runParser(self, lstSubcommand=[]):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            print("INDIEGOGO parser [%s] starting..."%strSubcommand)
            handler(strArg1)
            print("INDIEGOGO parser [%s] finished."%strSubcommand)
        
    #解析 explore.html
    def parseExplorePage(self, uselessArg1=None):
        strExploreHtmlPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"/INDIEGOGO/explore.html"
        strExploreResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"/INDIEGOGO"
        if not os.path.exists(strExploreResultFolderPath):
            os.mkdir(strExploreResultFolderPath) #mkdir parsed_result/INDIEGOGO/
        with open(strExploreHtmlPath, "r") as expHtmlFile:
            strPageSource = expHtmlFile.read()
        root = Selector(text=strPageSource)
        lstStrCategoryUrls = root.css("explore-category-link-www a.i-uncolored-link::attr(href)").extract()
        if len(lstStrCategoryUrls) == 0:
            lstStrCategoryUrls = root.css("ul.exploreCategories-list li.ng-scope a.ng-binding::attr(href)").extract()
        strCategoryUrlListFilePath = strExploreResultFolderPath + u"/" + self.CATEGORY_URL_LIST_FILENAME
        with open(strCategoryUrlListFilePath, "w+") as catUrlListFile:
            for strCategoryUrl in lstStrCategoryUrls:
                strCategoryUrl = re.sub("#/browse", "", strCategoryUrl)
                strCategoryUrl = re.search("^(https://www.indiegogo.com/explore/[a-z_]*)\??.*$" ,strCategoryUrl).group(1)
                if strCategoryUrl == "https://www.indiegogo.com/explore/all":
                    continue
                else:
                    catUrlListFile.write(strCategoryUrl + u"\n")
        
    #解析 category.html
    def parseCategoryPage(self, uselessArg1=None):
        strCategoryUrlListFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"/INDIEGOGO/category_url_list.txt"
        catUrlListFile = open(strCategoryUrlListFilePath)
        for strCategoryUrl in catUrlListFile:#category loop
            strCategoryName = re.search("^https://www.indiegogo.com/explore/(.*)$" ,strCategoryUrl).group(1)
            strCategoryHtmlPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"/INDIEGOGO/%s/category.html"%(strCategoryName)
            if os.path.exists(strCategoryHtmlPath):#check category.html exists
                strCategoryResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"/INDIEGOGO/" + strCategoryName
                if not os.path.exists(strCategoryResultFolderPath):
                    os.mkdir(strCategoryResultFolderPath) #mkdir parsed_result/INDIEGOGO/category/
                with open(strCategoryHtmlPath, "r") as catHtmlFile: #open category.html
                    strPageSource = catHtmlFile.read()
                    root = Selector(text=strPageSource)
                    lstStrProjUrls = root.css("a.discoveryCard::attr(href)").extract() #parse proj urls
                    strProjectUrlListFilePath = strCategoryResultFolderPath + u"/project_url_list.txt"
                    with open(strProjectUrlListFilePath, "w+") as projUrlListFile: #write to project_url_list.txt
                        for strProjUrl in lstStrProjUrls:
                            projUrlListFile.write(strProjUrl + u"\n")
                            
    #解析 project page(s) 之前
    def beforeParseProjectPage(self, strCategoryName=None):
        strProjectsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        if not os.path.exists(strProjectsResultFolderPath):
            os.mkdir(strProjectsResultFolderPath) #mkdir parsed_result/INDIEGOGO/category/projects/
            
    #解析 _details.html
    def parseProjectDetailsPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        lstStrDetailsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_details.html")
        for strProjectDetailsHtmlPath in lstStrDetailsHtmlFilePath:
            with open(strProjectDetailsHtmlPath, "r") as projDetailsHtmlFile: #open *_details.html
                strProjHtmlFileName = os.path.basename(projDetailsHtmlFile.name)
                strProjUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_details.html$", strProjHtmlFileName).group(1)
                if strProjUrl not in self.dicParsedResultOfProject:
                    self.dicParsedResultOfProject[strProjUrl] = {}
                strPageSource = projDetailsHtmlFile.read()
                root = Selector(text=strPageSource)
                #parse *_details.html
                strIndividualsUrl = root.css("div.campaignTrustPassportDesktop-ownerInfo a.ng-binding[href*='individuals']::attr(href)").extract_first() #parse individuals url
                self.dicParsedResultOfProject[strProjUrl]["strCreatorUrl"] = strIndividualsUrl
                # append url to parsed_result/*/category/individuals_url_list.txt
                strIndividualsUrlListFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/individuals_url_list.txt"%(strCategoryName))
                lstStrExistsIndividualsUrl = []
                if os.path.exists(strIndividualsUrlListFilePath):
                    with open(strIndividualsUrlListFilePath, "r") as individualsUrlListFile:
                        lstStrExistsIndividualsUrl = individualsUrlListFile.readlines()
                if strIndividualsUrl+u"\n" not in lstStrExistsIndividualsUrl:#檢查有無重覆的 individuals url
                    with open(strIndividualsUrlListFilePath, "a") as individualsUrlListFile:
                        individualsUrlListFile.write(strIndividualsUrl + u"\n") #append url to individuals_url_list.txt
                    
    #解析 _story.html
    def parseProjectStoryPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        lstStrStoryHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_story.html")
        for strProjStoryFilePath in lstStrStoryHtmlFilePath:
            with open(strProjStoryFilePath, "r") as projStoryHtmlFile:
                strProjHtmlFileName = os.path.basename(projStoryHtmlFile.name)
                strProjUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_story.html$", strProjHtmlFileName).group(1)
                if strProjUrl not in self.dicParsedResultOfProject:
                    self.dicParsedResultOfProject[strProjUrl] = {}
                strPageSource = projStoryHtmlFile.read()
                root = Selector(text=strPageSource)
                #parse *_story.html then save json to parsed_result/*/projects/
                #strSource
                self.dicParsedResultOfProject[strProjUrl]["strSource"] = \
                    "INDIEGOGO"
                #strUrl
                self.dicParsedResultOfProject[strProjUrl]["strUrl"] = \
                    strProjUrl
                #strProjectName
                self.dicParsedResultOfProject[strProjUrl]["strProjectName"] = \
                    root.css("h1.campaignHeader-title::text").extract_first().strip()
                #strLocation
                self.dicParsedResultOfProject[strProjUrl]["strLocation"] = \
                    root.css("div.campaignHeader-location a.ng-binding::text").extract_first().strip()
                #strCountry
                self.dicParsedResultOfProject[strProjUrl]["strCountry"] = \
                    root.css("div.campaignTrustTeaser-item:nth-of-type(2) div.campaignTrustTeaser-text div.ng-binding:nth-of-type(3)::text").extract_first().strip()
                #strContinent
                self.dicParsedResultOfProject[strProjUrl]["strContinent"] = \
                    root.css("div.campaignTrustTeaser-item:nth-of-type(2) div.campaignTrustTeaser-text div.ng-binding:nth-of-type(2)::text").extract_first().split(",")[1].strip()
                #strDescription = ""
                #strIntroduction = ""
                #strCreator
                self.dicParsedResultOfProject[strProjUrl]["strCreator"] = \
                    root.css("div.campaignTrustTeaser-item:nth-of-type(1) div.campaignTrustTeaser-text div.campaignTrustTeaser-text-title::text").extract_first().strip()
                #strCreatorUrl = "" 由 parseProjectDetailsPage 取得
                #intVideoCount = "" 由 parseProjectGalleryPage 取得
                #intImageCount = "" 由 parseProjectGalleryPage 取得
                #isPMSelect = "" 無法取得
                #intStatus
                isIndemand = False
                if len(root.css("div.indemandSidebar-banner").extract()) > 0:
                    isIndemand = True
                if isIndemand:
                    strIndemandBlurbText = root.css("div.preOrder-fundingBlurb::text").extract_first().strip()
                    intIndemandFundedPersentage = int(re.search("^Original campaign was ([0-9\.]*)% funded on .*$", strIndemandBlurbText).group(1))
                    if intIndemandFundedPersentage >= 100:
                        self.dicParsedResultOfProject[strProjUrl]["intStatus"] = 3
                    else:
                        self.dicParsedResultOfProject[strProjUrl]["intStatus"] = 4
                else:
                    strMetaFundingText = root.css("div.campaignGoal-barMetaFunding em::text").extract_first().strip()
                    intFundingPersentage = int(re.search("([0-9\.]*)%", strMetaFundingText).group(1))
                    if intFundingPersentage >= 100:
                        self.dicParsedResultOfProject[strProjUrl]["intStatus"] = 1
                    else:
                        self.dicParsedResultOfProject[strProjUrl]["intStatus"] = 0
                #strCategory
                self.dicParsedResultOfProject[strProjUrl]["strCategory"] = \
                    root.css("div.campaignTrustTeaser-item:nth-of-type(2) div.campaignTrustTeaser-text-title::text").extract_first().strip()
                #strSubCategory = "" 無法取得
                #intRaisedMoney
                if isIndemand:
                    strFundsAmountText = root.css("div.preOrder-combinedBalance div.ng-binding span.currency span::text").extract_first().strip()
                else:
                    strFundsAmountText = root.css("div.campaignGoal-funds span.campaignGoal-fundsAmount span.currency span::text").extract_first().strip()
                self.dicParsedResultOfProject[strProjUrl]["intRaisedMoney"] = \
                    int(re.sub("[^0-9]", "", strFundsAmountText))
                #intFundTarget = ""
                #fFundProgress = ""
                #strCurrency = ""
                #intBacker = ""
                #intRemainDays = ""
                #intUpdate = ""
                #intComment = ""
                #strEndDate = ""
                #strStartDate = ""
                #intFbLike = ""
                #lstStrBacker = ""
                #isDemand = ""
                #isAON = ""
                            
                            
    #解析 _updates.html
    def parseProjectUpdatesPage(self, strCategoryName=None):
        pass
        
    #解析 _comments.html
    def parseProjectCommentsPage(self, strCategoryName=None):
        pass
        
    #解析 _backers.html
    def parseProjectBackersPage(self, strCategoryName=None):
        pass
        
    #解析 _reward.html (INDIEGOGO 的 reward 資料置於 _story.html)
    def parseProjectRewardPage(self, strCategoryName=None):
        pass
        
    #解析 _gallery.html
    def parseProjectGalleryPage(self, strCategoryName=None):
        pass
        
    #解析 individuals page(s) 之前
    def beforeParseIndividualsPage(self, strCategoryName=None):
        pass
    #解析 _profile.html
    def parseIndividualsProfilePage(self, strCategoryName=None):
        pass
    #解析 _campaigns.html
    def parseIndividualsCampaignsPage(self, strCategoryName=None):
        pass