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
        self.SOURCE_HTML_BASE_FOLDER_PATH = u"./cameo_res/source_html"
        self.PARSED_RESULT_BASE_FOLDER_PATH = u"./cameo_res/parsed_result"
        self.CATEGORY_URL_LIST_FILENAME = u"category_url_list.txt"
        self.PROJ_URL_LIST_FILENAME = u"_proj_url_list.txt"
        
    #解析 explore.html
    def parseExplorePage(self):
        strExploreHtmlPath = self.SOURCE_HTML_BASE_FOLDER_PATH + u"/INDIEGOGO/explore.html"
        strExploreResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + u"/INDIEGOGO"
        if not os.path.exists(strExploreResultFolderPath):
            os.mkdir(strExploreResultFolderPath) #mkdir parsed_result/INDIEGOGO/
        with open(strExploreHtmlPath, "r") as expHtmlFile:
            strPageSource = expHtmlFile.read()
        root = Selector(text=strPageSource)
        lstStrCategoryUrls = root.css("explore-category-link-www a.i-uncolored-link::attr(href)").extract()
        strCategoryUrlListFilePath = strExploreResultFolderPath + u"/" + self.CATEGORY_URL_LIST_FILENAME
        with open(strCategoryUrlListFilePath, "w+") as catUrlListFile:
            for strCategoryUrl in lstStrCategoryUrls:
                catUrlListFile.write(strCategoryUrl + u"\n")
        
    #解析 category.html
    def parseCategoryPage(self):
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
                            
    #解析 project page(s)
    def parseProjectDetailsPage(self, strCategoryName):
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
                    
    def parseProjectStoryPage(self, strCategoryName):
        strProjectUrlListFilePath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/project_url_list.txt"%(strCategoryName))
        for strProjUrl in open(strProjectUrlListFilePath, "r"):
            strProjectName = re.search("^https://www.indiegogo.com/projects/(.*)/....$" ,strProjUrl).group(1)
            strProjectStoryHtmlPath = self.SOURCE_HTML_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects/%s_story.html"%(strCategoryName, strProjectName))
            if os.path.exists(strProjectStoryHtmlPath):#check *_story.html exists
                strProjectsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"/INDIEGOGO/%s/projects"%strCategoryName)
                if not os.path.exists(strProjectsResultFolderPath):
                    os.mkdir(strProjectsResultFolderPath) #mkdir parsed_result/INDIEGOGO/category/projects/
                with open(strProjectStoryHtmlPath, "r") as projStoryHtmlFile: #open *_story.html
                    strPageSource = projStoryHtmlFile.read()
                    root = Selector(text=strPageSource)
                    #parse *_story.html then save json to parsed_result/*/projects/
                    pass #TODO
                    
    def parseProjectUpdatesPage(self):
        pass
    def parseProjectCommentsPage(self):
        pass
    def parseProjectBackersPage(self):
        pass
    def parseProjectRewardPage(self):
        pass
        
    #解析 individuals.html
    def parseIndividualsPage(self, strCategoryName):
        pass