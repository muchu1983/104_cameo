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
                                                self.parseProjectGalleryPage,
                                                self.afterParseProjectPage],
                                     "individuals":[self.beforeParseIndividualsPage,
                                                    self.parseIndividualsProfilePage,
                                                    self.parseIndividualsCampaignsPage],}
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"./cameo_res/source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"./cameo_res/parsed_result"
        self.CATEGORY_URL_LIST_FILENAME = u"category_url_list.txt"
        self.PROJ_URL_LIST_FILENAME = u"_proj_url_list.txt"
        self.dicParsedResultOfProject = {}
        self.dicParsedResultOfUpdate = {}
        self.dicParsedResultOfComment = {}
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
            
    #解析 project page(s) 之後
    def afterParseProjectPage(self, strCategoryName=None):
        pass #TODO write dict to json file
            
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
                #strCreatorUrl
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
                #parse *_story.html
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
                strTrustTeaserText = root.css("div.campaignTrustTeaser-item:nth-of-type(2) div.campaignTrustTeaser-text div.ng-binding:nth-of-type(2)::text").extract_first()
                strContinent = None
                if "," in strTrustTeaserText:
                    strContinent = strTrustTeaserText.split(",")[1].strip()
                self.dicParsedResultOfProject[strProjUrl]["strContinent"] = strContinent
                #strDescription = "" TODO
                #strIntroduction
                self.dicParsedResultOfProject[strProjUrl]["strIntroduction"] = \
                    root.css("div.i-musty-background div:nth-of-type(1)::text").extract_first().strip()
                #strCreator
                self.dicParsedResultOfProject[strProjUrl]["strCreator"] = \
                    root.css("div.campaignTrustTeaser-item:nth-of-type(1) div.campaignTrustTeaser-text div.campaignTrustTeaser-text-title::text").extract_first().strip()
                #strCreatorUrl = "" 已由 parseProjectDetailsPage 取得
                #intVideoCount = "" 由 parseProjectGalleryPage 取得??
                #intImageCount
                strGalleryCountText = root.css("span.i-tab:nth-of-type(5) span span::text").extract_first()
                intImageCount = 0
                if strGalleryCountText != None:
                    intImageCount = int(strGalleryCountText.strip())
                self.dicParsedResultOfProject[strProjUrl]["intImageCount"] = intImageCount
                #isPMSelect = "" 無法取得
                #intStatus
                isIndemand = False
                if len(root.css("div.indemandSidebar-banner").extract()) > 0:
                    isIndemand = True
                intIndemandFundedPersentage = 0
                intFundingPersentage = 0
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
                strCategory = root.css("div.campaignTrustTeaser-item:nth-of-type(2) div.campaignTrustTeaser-text-title::text").extract_first().strip()
                self.dicParsedResultOfProject[strProjUrl]["strCategory"] = \
                    strCategory
                #strSubCategory 與 strCategory 相同
                self.dicParsedResultOfProject[strProjUrl]["strSubCategory"] = \
                    strCategory
                #intRaisedMoney
                intRaisedMoney = 0
                if isIndemand:
                    strFundsAmountText = root.css("div.preOrder-combinedBalance div.ng-binding span.currency span::text").extract_first().strip()
                else:
                    strFundsAmountText = root.css("div.campaignGoal-funds span.campaignGoal-fundsAmount span.currency span::text").extract_first().strip()
                intRaisedMoney = int(re.sub("[^0-9]", "", strFundsAmountText))
                self.dicParsedResultOfProject[strProjUrl]["intRaisedMoney"] = \
                    intRaisedMoney
                #intFundTarget
                if isIndemand:
                    intFundTarget = int(float(intRaisedMoney) / (float(intIndemandFundedPersentage) / 100 ))
                else:
                    strRaisedGoalText = root.css("span.campaignGoal-fundsRaisedGoal span.numeral::text").extract_first().strip()
                    intFundTarget = int(re.sub("[^0-9]", "", strRaisedGoalText))
                self.dicParsedResultOfProject[strProjUrl]["intFundTarget"] = intFundTarget
                #fFundProgress
                if isIndemand:
                    self.dicParsedResultOfProject[strProjUrl]["fFundProgress"] = float(intIndemandFundedPersentage) / 100
                else:
                    self.dicParsedResultOfProject[strProjUrl]["fFundProgress"] = float(intFundingPersentage) / 100
                #strCurrency
                if isIndemand:
                    strCurrencyText = root.css("div.preOrder-combinedBalance div.ng-binding span.currency em::text").extract_first().strip()
                else:
                    strCurrencyText = root.css("div.campaignGoal-funds span.campaignGoal-fundsAmount span.currency em::text").extract_first().strip()
                self.dicParsedResultOfProject[strProjUrl]["strCurrency"] = strCurrencyText
                #intBacker
                self.dicParsedResultOfProject[strProjUrl]["intBacker"] = \
                    int(root.css("span.i-tab:nth-of-type(4) span span::text").extract_first().strip())
                #intRemainDays = "" 由 parseCategoryPage 取得 ??
                #intUpdate
                self.dicParsedResultOfProject[strProjUrl]["intUpdate"] = \
                    int(root.css("span.i-tab:nth-of-type(2) span span::text").extract_first().strip())
                #intComment
                self.dicParsedResultOfProject[strProjUrl]["intComment"] = \
                    int(root.css("span.i-tab:nth-of-type(3) span span::text").extract_first().strip())
                #strEndDate = "" 由 parseCategoryPage 取得 ??
                #strStartDate = "" 無法取得
                #intFbLike
                strShareBannerText = root.css("div.shareBanner div.shareBanner-label div.shareBanner-labelText::text").extract_first().strip()
                intFbLike = self.utility.translateNumTextToPureNum(strShareBannerText)
                self.dicParsedResultOfProject[strProjUrl]["intFbLike"] = intFbLike
                #lstStrBacker = "" 已由 parseProjectBackersPage 取得
                #isDemand
                if isIndemand:
                    self.dicParsedResultOfProject[strProjUrl]["isDemand"] = True
                else:
                    self.dicParsedResultOfProject[strProjUrl]["isDemand"] = False
                #isAON
                strIStatusText = root.css("div.campaignGoal-goalFundingType span.i-status::text").extract_first()
                if strIStatusText != None and strIStatusText.strip() == "Flexible Funding":
                    self.dicParsedResultOfProject[strProjUrl]["isAON"] = True
                else:
                    self.dicParsedResultOfProject[strProjUrl]["isAON"] = False
                            
    #解析 _updates.html
    def parseProjectUpdatesPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        lstStrUpdatesHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_updates.html")
        for strProjUpdatesFilePath in lstStrUpdatesHtmlFilePath:
            with open(strProjUpdatesFilePath, "r") as projUpdatesHtmlFile:
                strProjHtmlFileName = os.path.basename(projUpdatesHtmlFile.name)
                strProjUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_updates.html$", strProjHtmlFileName).group(1)
                strPageSource = projUpdatesHtmlFile.read()
                root = Selector(text=strPageSource)
                #parse *_updates.html
                lstDicUpdateData = []
                #loop of append update data to lstDicUpdateData
                for elementUpdate in root.css("desktop-updates div.activityUpdate"):
                    dicUpdateData = {}
                    #strUrl
                    dicUpdateData["strUrl"] = strProjUrl
                    #strUpdateTitle 無法取得
                    #strUpdateContent
                    strUpdateContent = u""
                    lstStrUpdateContentParagraph = elementUpdate.css("div.ugcContent *::text").extract()
                    for strUpdateContentParagraph in lstStrUpdateContentParagraph:
                        strUpdateContent = strUpdateContent + strUpdateContentParagraph.strip()
                    dicUpdateData["strUpdateContent"] = strUpdateContent
                    #strUpdateDate
                    dicUpdateData["strUpdateDate"] = \
                        elementUpdate.css("h2.activityUpdate-timestamp::text").extract_first().strip()
                    #intComment 無法取得
                    #intLike 無法取得
                    lstDicUpdateData.append(dicUpdateData)
                self.dicParsedResultOfUpdate[strProjUrl] = lstDicUpdateData
        
    #解析 _comments.html
    def parseProjectCommentsPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        lstStrCommentsHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_comments.html")
        for strProjCommentsFilePath in lstStrCommentsHtmlFilePath:
            with open(strProjCommentsFilePath, "r") as projCommentsHtmlFile:
                strProjHtmlFileName = os.path.basename(projCommentsHtmlFile.name)
                strProjUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_comments.html$", strProjHtmlFileName).group(1)
                strPageSource = projCommentsHtmlFile.read()
                root = Selector(text=strPageSource)
                #parse *_comments.html
                lstDicCommentData = []
                #loop of append comment data to lstDicCommentData
                for elementComment in root.css("div.i-comments desktop-comment"):
                    dicCommentData = {}
                    #strUrl
                    dicCommentData["strUrl"] = strProjUrl
                    #strCommentName
                    dicCommentData["strCommentName"] = \
                        elementComment.css("div.commentLayout-header:nth-of-type(1) a.commentLayout-account::text").extract_first()
                    #isCreator
                    strPillText = elementComment.css("div.commentLayout-header:nth-of-type(1) span.i-annotation-pill::text").extract_first()
                    isCreator = False
                    if strPillText != None and strPillText.strip() == "Campaigner":
                        isCreator = True
                    dicCommentData["isCreator"] = isCreator
                    #strCommentContent
                    strCommentContent = u""
                    lstStrCommentContentParagraph = elementComment.css("div.commentLayout-text:nth-of-type(2) *::text").extract()
                    for strCommentContentParagraph in lstStrCommentContentParagraph:
                        strCommentContent = strCommentContent + strCommentContentParagraph.strip()
                    dicCommentData["strCommentContent"] = strCommentContent
                    #strCommentDate
                    dicCommentData["strCommentDate"] = \
                        elementComment.css("div.commentLayout-header:nth-of-type(1) span.commentNote::text").extract_first().strip()
                    lstDicCommentData.append(dicCommentData)
                self.dicParsedResultOfComment[strProjUrl] = lstDicCommentData
                
    #解析 _backers.html
    def parseProjectBackersPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        lstStrBackersHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_backers.html")
        for strProjBackersFilePath in lstStrBackersHtmlFilePath:
            with open(strProjBackersFilePath, "r") as projBackersHtmlFile:
                strProjHtmlFileName = os.path.basename(projBackersHtmlFile.name)
                strProjUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_backers.html$", strProjHtmlFileName).group(1)
                if strProjUrl not in self.dicParsedResultOfProject:
                    self.dicParsedResultOfProject[strProjUrl] = {}
                strPageSource = projBackersHtmlFile.read()
                root = Selector(text=strPageSource)
                #parse *_backers.html
                #lstStrBacker
                lstStrBacker = root.css("div.i-funder-row div.i-name-col div.i-name div.i-details-name::text,a.i-details-name::text").extract()
                self.dicParsedResultOfProject[strProjUrl]["lstStrBacker"] = lstStrBacker
                
    #解析 _story.html (INDIEGOGO 的 reward 資料置於 _story.html)
    def parseProjectRewardPage(self, strCategoryName=None):
        strProjectsHtmlFolderPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
        lstStrStoryHtmlFilePath = self.utility.getFilePathListWithSuffixes(strBasedir=strProjectsHtmlFolderPath, strSuffixes="_story.html")
        for strProjStoryFilePath in lstStrStoryHtmlFilePath:
            with open(strProjStoryFilePath, "r") as projStoryHtmlFile:
                strProjHtmlFileName = os.path.basename(projStoryHtmlFile.name)
                strProjUrl = "https://www.indiegogo.com/projects/" + re.search("^(.*)_story.html$", strProjHtmlFileName).group(1)
                strPageSource = projStoryHtmlFile.read()
                root = Selector(text=strPageSource)
                #parse *_story.html (for reward data)
                lstDicRewardData = []
                #loop of append reward data to lstDicRewardData
                for elementReward in root.css("div.perkItem-campaignPerkContainer"):
                    dicRewardData = {}
                    #strUrl
                    dicRewardData["strUrl"] = strProjUrl
                    #strRewardContent
                    strPerkTitleText = elementReward.css("perk-title div.perkItem-title::text").extract_first().strip()
                    strPerkDescriptionText = elementReward.css("perk-description div.perkItem-description::text").extract_first().strip()
                    strRewardContent = strPerkTitleText + "\n" + strPerkDescriptionText
                    dicRewardData["strRewardContent"] = strRewardContent
                    #intRewardMoney
                    strPerkAmountText = elementReward.css("amount-with-currency span.perkItem-perkAmount::text").extract_first().strip()
                    dicRewardData["intRewardMoney"] = \
                        int(re.sub("[^0-9]", "", strPerkAmountText))
                    #intRewardBacker and intRewardLimit
                    elementAvailability = elementReward.css("span.availability")
                    #intRewardBacker
                    dicRewardData["intRewardBacker"] = \
                        int(elementAvailability.css("b:nth-of-type(1)::text").extract_first().strip())
                    #intRewardLimit
                    intRewardLimit = 0
                    if len(elementAvailability.css("b").extract()) == 2:
                        intRewardLimit = int(elementAvailability.css("b:nth-of-type(2)::text").extract_first().strip())
                    dicRewardData["intRewardLimit"] = intRewardLimit
                    #strRewardShipTo
                    strShipsToText = elementReward.css("ships-to-countries span.shipsTo-label::text").extract_first()
                    strRewardShipTo = None
                    if strShipsToText != None:
                        strRewardShipTo = re.search("^Ships (.*)$", strShipsToText.strip()).group(1)
                    dicRewardData["strRewardShipTo"] = strRewardShipTo
                    #strRewardDeliveryDate
                    strRewardDeliveryDate = None
                    lstStrEstimateDeliveryText = elementReward.css("perk-description div[ng-if*=estimated_delivery_date] span::text").extract()
                    if len(lstStrEstimateDeliveryText) == 2 and lstStrEstimateDeliveryText[0].strip() == "Estimated delivery:":
                        strRewardDeliveryDate = lstStrEstimateDeliveryText[1].strip()
                    dicRewardData["strRewardDeliveryDate"] = strRewardDeliveryDate
                    #intRewardRetailPrice 無法取得
                    lstDicRewardData.append(dicRewardData)
                self.dicParsedResultOfReward[strProjUrl] = lstDicRewardData
                
        
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