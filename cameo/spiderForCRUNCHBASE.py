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
    
    #建立 category 清單
    def createCategoryListJsonFile(self):
        strFundingRoundsResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\CRUNCHBASE")
        if not os.path.exists(strFundingRoundsResultFolderPath):
            #mkdir parsed_result/CRUNCHBASE/
            os.mkdir(strFundingRoundsResultFolderPath)
        strCategoryListFilePath = strFundingRoundsResultFolderPath + u"\\category_list.json"
        #若不存在，建立新的 category_list.json
        if not os.path.exists(strCategoryListFilePath):
            dicCategory = {
                "intMinRange":1,
                "intMaxRange":121,
                "1":"Artificial Intelligence",
                "2":"Operating Systems",
                "3":"UX Design",
                "4":"Cloud Computing",
                "5":"Big Data",
                "6":"Web Development",
                "7":"Internet",
                "8":"Computer",
                "9":"Electronics",
                "10":"3D Technology",
                "11":"Virtual Reality",
                "12":"Apps",
                "13":"Software",
                "14":"Enterprise Software",
                "15":"Software Engineering",
                "16":"E-Commerce",
                "17":"Online to offline",
                "18":"PaaS",
                "19":"B2B",
                "20":"Sharing Economy",
                "21":"Transaction Processing",
                "22":"Social Media",
                "23":"Social Network",
                "24":"Content",
                "25":"Mobile",
                "26":"Mobile Devices",
                "27":"GPS",
                "28":"Communications Infrastructure",
                "29":"ICT",
                "30":"Wearables",
                "31":"Robotics",
                "32":"Internet of Things",
                "33":"Drones",
                "34":"Embedded Systems",
                "35":"Biotechnology",
                "36":"Medical",
                "37":"Pharmaceutical",
                "38":"Health Care",
                "39":"Lifestyle",
                "40":"Consumer",
                "41":"Housekeeping Service",
                "42":"Personalization",
                "43":"Communities",
                "44":"Women's",
                "45":"Men's",
                "46":"Elderly",
                "47":"Food Processing",
                "48":"Cosmetics",
                "49":"Children",
                "50":"Food and Beverage",
                "51":"Shopping",
                "52":"Fashion",
                "53":"Home and Garden",
                "54":"Real Estate",
                "55":"Restaurants",
                "56":"Transportation",
                "57":"Pet",
                "58":"FinTech",
                "59":"Property Management",
                "60":"Finance",
                "61":"Venture Capital",
                "62":"Insurance",
                "63":"Rental",
                "64":"Digital Media",
                "65":"Advertising",
                "66":"Travel",
                "67":"Gaming",
                "68":"Sports",
                "69":"Digital Entertainment",
                "70":"Leisure",
                "71":"Outdoors",
                "72":"Professional Services",
                "73":"Business Intelligence",
                "74":"Homeland Security",
                "75":"Infrastructure",
                "76":"Consulting",
                "77":"Local",
                "78":"Procurement",
                "79":"Product Research",
                "80":"Brand Marketing",
                "81":"Marketing",
                "82":"CRM",
                "83":"Human Resources",
                "84":"Logistics",
                "85":"Outsourcing",
                "86":"Small and Medium Businesses",
                "87":"Trading Platform",
                "88":"Music",
                "89":"Fashion",
                "90":"Product Design",
                "91":"Publishing",
                "92":"Photography",
                "93":"Art",
                "94":"Creative Agency",
                "95":"Animation",
                "96":"Jewelry",
                "97":"Education",
                "98":"Charter Schools",
                "99":"E-Learning",
                "100":"Training",
                "101":"Energy",
                "102":"Natural Resources",
                "103":"Recycling",
                "104":"Geospatial",
                "105":"Advanced Materials",
                "106":"Social Entrepreneurship",
                "107":"Innovation Management",
                "108":"Public Relations",
                "109":"Politics",
                "110":"Charity",
                "111":"National Security",
                "112":"Manufacturing",
                "113":"Printing",
                "114":"Construction",
                "115":"Architecture",
                "116":"Industrial",
                "117":"Retail",
                "118":"Chemical",
                "119":"Aerospace",
                "120":"Freelance",
                "121":"Funerals",
            }
            self.utility.writeObjectToJsonFile(dicData=dicCategory, strJsonFilePath=strCategoryListFilePath)
        else:
            pass
    
    #下載 funding rounds 頁面
    def handleSearchFundingRoundsPage(self, arg1=None):
        self.createCategoryListJsonFile()
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
        self.createCategoryListJsonFile()
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
        strOrganizationResultFolderPath = self.PARSED_RESULT_BASE_FOLDER_PATH + (u"\\CRUNCHBASE\\organization")
        if not os.path.exists(strOrganizationResultFolderPath):
            #mkdir parsed_result/CRUNCHBASE/organization/
            os.mkdir(strOrganizationResultFolderPath)
        lstStrOrganizationUrl = self.db.fetchallNotObtainedOrganizationUrl()
        strOrganizationUrlListFilePath = strOrganizationResultFolderPath + u"\\organization_url_list.json"
        #刪除原本的 organization_url_list.json
        if os.path.exists(strOrganizationUrlListFilePath):
            os.remove(strOrganizationUrlListFilePath)
        #建立新的 organization_url_list.json
        dicLstStrOrganizationUrl = {"organization_url_list": lstStrOrganizationUrl}
        self.utility.writeObjectToJsonFile(dicData=dicLstStrOrganizationUrl, strJsonFilePath=strOrganizationUrlListFilePath)
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
            "organization - download organization.html and investors.html \n"
        )
        
    #執行 spider
    def runSpider(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        self.dicSubCommandHandler[strSubcommand](strArg1)