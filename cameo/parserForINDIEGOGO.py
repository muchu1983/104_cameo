# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import re
from scrapy import Selector
"""
從 source_html 的 HTML 檔案解析資料
結果放置於 parsed_result 下
"""
class ParserForINDIEGOGO:
    #建構子
    def __init__(self):
        self.dicSubCommandHandler = {"explore":[self.parseExplorePage],
                                     "category":[self.parseCategoryPage],
                                     "project":[self.beforeParseProjectPage,
                                                self.parseProjectDetailsPage,
                                                self.parseProjectStoryPage,
                                                self.parseProjectUpdatesPage,
                                                self.parseProjectCommentsPage,
                                                self.parseProjectBackersPage,
                                                self.parseProjectRewardPage],
                                     "individuals":[self.beforeParseIndividualsPage,
                                                    self.parseIndividualsProfilePage,
                                                    self.parseIndividualsCampaignsPage],}
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"./cameo_res/source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"./cameo_res/parsed_result"
        self.CATEGORY_URL_LIST_FILENAME = u"category_url_list.txt"
        self.PROJ_URL_LIST_FILENAME = u"_proj_url_list.txt"
        
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
        strProjectUrlListFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/project_url_list.txt"%(strCategoryName))
        for strProjUrl in open(strProjectUrlListFilePath, "r"):
            strProjectName = re.search("^https://www.indiegogo.com/projects/(.*)/....$" ,strProjUrl).group(1)
            strProjectDetailsHtmlPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects/%s_details.html"%(strCategoryName, strProjectName))
            if os.path.exists(strProjectDetailsHtmlPath):#check *_details.html exists
                with open(strProjectDetailsHtmlPath, "r") as projDetailsHtmlFile: #open *_details.html
                    strPageSource = projDetailsHtmlFile.read()
                    root = Selector(text=strPageSource)
                    #parse *_details.html then append url to parsed_result/*/category/individuals_url_list.txt
                    strIndividualsUrlListFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/individuals_url_list.txt"%(strCategoryName))
                    lstStrExistsIndividualsUrl = []
                    if os.path.exists(strIndividualsUrlListFilePath):
                        with open(strIndividualsUrlListFilePath, "r") as individualsUrlListFile:
                            lstStrExistsIndividualsUrl = individualsUrlListFile.readlines()
                    strIndividualsUrl = root.css("div.campaignTrustPassportDesktop-ownerInfo a.ng-binding[href*='individuals']::attr(href)").extract_first() #parse individuals url
                    if strIndividualsUrl+u"\n" not in lstStrExistsIndividualsUrl:#檢查有無重覆的 individuals url
                        with open(strIndividualsUrlListFilePath, "a") as individualsUrlListFile:
                            individualsUrlListFile.write(strIndividualsUrl + u"\n") #append url to individuals_url_list.txt
                    
    #解析 _story.html
    def parseProjectStoryPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        for base, dirs, files in os.walk(strProjectsHtmlFolderPath): 
            if base == strProjectsHtmlFolderPath:#just check projects dir
                for strProjHtmlFileName in files:
                    if strProjHtmlFileName.endswith("_story.html"):#find _story.html file
                        strProjStoryFilePath = os.path.join(base, strProjHtmlFileName)
                        with open(strProjStoryFilePath, "r") as projStoryHtmlFile:
                            strPageSource = projStoryHtmlFile.read()
                            root = Selector(text=strPageSource)
                            #parse *_story.html then save json to parsed_result/*/projects/
                            strSource = "INDIEGOGO"
                            strUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_story.html$", strProjHtmlFileName).group(1)
                            strProjectName = root.css("h1.campaignHeader-title::text").extract()
                            strLocation = root.css("div.campaignHeader-location a.ng-binding::text").extract_first().strip()
                            strCountry = root.css("div.campaignTrustTeaser-item:nth-of-type(2) div.campaignTrustTeaser-text div.ng-binding:nth-of-type(3)::text").extract_first().strip()
                            strContinent = root.css("div.campaignTrustTeaser-item:nth-of-type(2) div.campaignTrustTeaser-text div.ng-binding:nth-of-type(2)::text").extract_first().split(",")[1].strip()
                            strDescription = ""
                            strIntroduction = ""
                            strCreator = root.css("div.campaignTrustTeaser-item:nth-of-type(1) div.campaignTrustTeaser-text div.campaignTrustTeaser-text-title::text").extract_first().strip()
                            strCreatorUrl = ""
                            intVideoCount = ""
                            intImageCount = ""
                            isPMSelect = ""
                            intStatus = ""
                            strCategory = ""
                            strSubCategory = ""
                            fFundProgress = ""
                            intFundTarget = ""
                            intRaisedMoney = ""
                            strCurrency = ""
                            intBacker = ""
                            intRemainDays = ""
                            intUpdate = ""
                            intComment = ""
                            strEndDate = ""
                            strStartDate = ""
                            intFbLike = ""
                            lstStrBacker = ""
                            isDemand = ""
                            isAON = ""
                            
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
        
    #解析 individuals page(s) 之前
    def beforeParseIndividualsPage(self, strCategoryName=None):
        pass
    #解析 _profile.html
    def parseIndividualsProfilePage(self, strCategoryName=None):
        pass
    #解析 _campaigns.html
    def parseIndividualsCampaignsPage(self, strCategoryName=None):
        pass