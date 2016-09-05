# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import re
import dateparser
from crawlermaster.utility import Utility

class ConverterForJD:
    
    #建構子
    def __init__(self):
        self.cmUtility = Utility()
        self.dicParsedResultOfProject = {} #project.json 資料
        self.dicParsedResultOfUpdate = {} #update.json 資料
        self.dicParsedResultOfReward = {} #reward.json 資料
        self.dicParsedResultOfQanda = {} #qanda.json 資料
        self.dicParsedResultOfComment = {} #comment.json 資料
        self.dicParsedResultOfProfile = {} #profile.json 資料
        
    #轉換 project 資訊
    def convertProject(self, lstLstDicRawData=[]):
        #_intro.html raw data
        lstDicIntroPageRawData = lstLstDicRawData[0]
        for dicIntroPageRawData in lstDicIntroPageRawData:
            strIntroHtmlFilePath = dicIntroPageRawData.get("meta-data-html-filepath", None)
            strProjectId = re.search("^.*\\\\([\d]+)_intro.html$", strIntroHtmlFilePath).group(1)
            strProjUrl = u"http://z.jd.com/project/details/%s.html"%strProjectId
            if strProjUrl not in self.dicParsedResultOfProject:
                self.dicParsedResultOfProject[strProjUrl] = {}
            # - 解析 project.json -
            #strSource
            self.dicParsedResultOfProject[strProjUrl]["strSource"] = u"JD"
            #strUrl
            self.dicParsedResultOfProject[strProjUrl]["strUrl"] = strProjUrl
            #strCrawlTime
            strCrawlTime = self.cmUtility.getCtimeOfFile(strFilePath=strIntroHtmlFilePath)
            self.dicParsedResultOfProject[strProjUrl]["strCrawlTime"] = strCrawlTime
            #strProjectName
            #strLocation
            #strCity
            #strCountry
            #strContinent
            #strDescription
            #strIntroduction
            #intStatus
            #strCreator
            #strCreatorUrl
            #strCategory
            #strSubCategory
            #intFundTarget
            #intRaisedMoney
            #fFundProgress
            #strCurrency
            #intRemainDays
            #strEndDate
            #strStartDate
            #intUpdate
            #intBacker
            #intComment
            #intFbLike
            #intVideoCount
            #intImageCount
            #isPMSelect 無法取得
            #
            # - 解析 reward.json -
            #strUrl
            #strRewardContent
            #intRewardMoney
            #intRewardBacker
            #intRewardLimit
            #strRewardShipTo and strRewardDeliveryDate
            #intRewardRetailPrice
        #_progress.html raw data
        lstDicProgressPageRawData = lstLstDicRawData[1]
        #_qanda.html raw data
        lstDicQandaPageRawData = lstLstDicRawData[2]
        #_sponsor.html raw data
        lstDicSponsorPageRawData = lstLstDicRawData[3]
        
    #轉換 profile 資訊
    def convertProfile(self, lstLstDicRawData=[]):
        #_proj.html raw data
        lstDicProjPageRawData = lstLstDicRawData[0]
        for dicProjPageRawData in lstDicProjPageRawData:
            strProjHtmlFileName = dicProjPageRawData.get("meta-data-html-filepath", None)
            strProfileId = re.search("^.*\\\\([\d]+)_proj.html$", strProjHtmlFileName).group(1)
            strProfUrl = u"http://z.jd.com/funderCenter.action?flag=2&id=" + strProfileId
            if strProfUrl not in self.dicParsedResultOfProfile:
                self.dicParsedResultOfProfile[strProfUrl] = {}
            #strUrl
            self.dicParsedResultOfProfile[strProfUrl]["strUrl"] = strProfUrl
            #strName
            strName = self.cmUtility.extractFirstInList(lstSource=dicProjPageRawData.get("jd-creator", [])).strip()
            self.dicParsedResultOfProfile[strProfUrl]["strName"] = strName
            #strIdentityName 同 strName
            self.dicParsedResultOfProfile[strProfUrl]["strIdentityName"] = strName
            #strDescription
            strDescription = self.cmUtility.extractFirstInList(lstSource=dicProjPageRawData.get("jd-creator-descript", [])).strip()
            self.dicParsedResultOfProfile[strProfUrl]["strDescription"] = strDescription
            #strLocation
            self.dicParsedResultOfProfile[strProfUrl]["strLocation"] = u"China"
            #strCity
            self.dicParsedResultOfProfile[strProfUrl]["strCity"] = u"China"
            #strCountry
            self.dicParsedResultOfProfile[strProfUrl]["strCountry"] = u"CN"
            #strContinent
            self.dicParsedResultOfProfile[strProfUrl]["strContinent"] = u"AS"
            #intCreatedCount
            intCreatedCount = int(self.cmUtility.extractFirstInList(lstSource=dicProjPageRawData.get("jd-creator-CreatedCount", [])).strip())
            self.dicParsedResultOfProfile[strProfUrl]["intCreatedCount"] = intCreatedCount
            #isCreator
            isCreator = False
            if intCreatedCount > 0:
                isCreator = True
            self.dicParsedResultOfProfile[strProfUrl]["isCreator"] = isCreator
            #lstStrCreatedProject
            self.dicParsedResultOfProfile[strProfUrl]["lstStrCreatedProject"] = dicProjPageRawData.get("jd-creator-CreatedProject", [])
            #lstStrCreatedProjectUrl
            lstStrCreatedProjectUrl = self.stripAndCompleteJDUrlList(lstStrOriginUrl=dicProjPageRawData.get("jd-creator-CreatedProjectUrl", []))
            self.dicParsedResultOfProfile[strProfUrl]["lstStrCreatedProjectUrl"] = lstStrCreatedProjectUrl
            #intSuccessProject 無法取得
            self.dicParsedResultOfProfile[strProfUrl]["intSuccessProject"] = None
            #intFailedProject 無法取得
            self.dicParsedResultOfProfile[strProfUrl]["intFailedProject"] = None
            #intLiveProject 無法取得
            self.dicParsedResultOfProfile[strProfUrl]["intLiveProject"] = None
            #lstStrSocialNetwork 無法取得
            self.dicParsedResultOfProfile[strProfUrl]["lstStrSocialNetwork"] = None
            #intFbFriend 無法取得
            self.dicParsedResultOfProfile[strProfUrl]["intFbFriend"] = None
            #strLastLoginDate 無法取得
            self.dicParsedResultOfProfile[strProfUrl]["strLastLoginDate"] = None
        #_order.html raw data
        lstDicOrderPageRawData = lstLstDicRawData[1]
        for dicOrderPageRawData in lstDicOrderPageRawData:
            strOrderHtmlFileName = dicOrderPageRawData.get("meta-data-html-filepath", None)
            strProfileId = re.search("^.*\\\\([\d]+)_order.html$", strOrderHtmlFileName).group(1)
            strProfUrl = u"http://z.jd.com/funderCenter.action?flag=2&id=" + strProfileId
            if strProfUrl not in self.dicParsedResultOfProfile:
                self.dicParsedResultOfProfile[strProfUrl] = {}
            #intBackedCount
            intBackedCount = int(self.cmUtility.extractFirstInList(lstSource=dicOrderPageRawData.get("jd-creator-BackedCount", [])).strip())
            self.dicParsedResultOfProfile[strProfUrl]["intBackedCount"] = intBackedCount
            #isBacker
            isBacker = False
            if intBackedCount > 0:
                isBacker = True
            self.dicParsedResultOfProfile[strProfUrl]["isBacker"] = isBacker
            #lstStrBackedProject
            self.dicParsedResultOfProfile[strProfUrl]["lstStrBackedProject"] = dicOrderPageRawData.get("jd-creator-BackedProject", [])
            #lstStrBackedProjectUrl
            lstStrBackedProjectUrl = self.stripAndCompleteJDUrlList(lstStrOriginUrl=dicOrderPageRawData.get("jd-creator-BackedProjectUrl", []))
            self.dicParsedResultOfProfile[strProfUrl]["lstStrBackedProjectUrl"] = lstStrBackedProjectUrl
        
    #去除 url list 中的 javascript:location.href 並加上 http://z.jd.com 組成完整的 JD url 
    def stripAndCompleteJDUrlList(self, lstStrOriginUrl=[]):
        lstStrResultUrl = []
        for strOriginUrl in lstStrOriginUrl:
            pattern = re.compile("(/project/details/[\d]+\.html)")
            strResultUrl = u"http://z.jd.com" + pattern.search(strOriginUrl).group(1)
            lstStrResultUrl.append(strResultUrl)
        return lstStrResultUrl
        
    #將 project convert 結果寫入 project.json update.json reward.json qanda.json comment.json 
    def flushConvertedProjectDataToJsonFile(self, strJsonFolderPath=None):
        strJsonFilePath = strJsonFolderPath + u"project.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfProject, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"update.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfUpdate, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"reward.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfReward, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"qanda.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfQanda, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"comment.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfComment, strJsonFilePath=strJsonFilePath)
        #清空資料
        self.dicParsedResultOfProject = {}
        self.dicParsedResultOfUpdate = {}
        self.dicParsedResultOfReward = {}
        self.dicParsedResultOfQanda = {}
        self.dicParsedResultOfComment = {}
        
    #將 profile convert 結果寫入 profilejson
    def flushConvertedProfileDataToJsonFile(self, strJsonFilePath=None):
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfProfile, strJsonFilePath=strJsonFilePath)
        self.dicParsedResultOfProfile = {}