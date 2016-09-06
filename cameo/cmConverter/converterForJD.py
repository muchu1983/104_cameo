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
from cameo.utility import Utility as CameoUtility
from crawlermaster.utility import Utility as CmUtility

class ConverterForJD:
    
    #建構子
    def __init__(self):
        self.cmUtility = CmUtility()
        self.cameoUtility = CameoUtility()
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
            logging.info("convert: %s"%strIntroHtmlFilePath)
            strProjectId = re.search("^.*\\\\([\d]+)_intro.html$", strIntroHtmlFilePath).group(1)
            strProjUrl = u"http://z.jd.com/project/details/%s.html"%strProjectId
            if strProjUrl not in self.dicParsedResultOfProject:
                self.dicParsedResultOfProject[strProjUrl] = {}
            if strProjUrl not in self.dicParsedResultOfReward:
                self.dicParsedResultOfReward[strProjUrl] = {}
            # - 解析 project.json -
            #strSource
            self.dicParsedResultOfProject[strProjUrl]["strSource"] = u"JD"
            #strUrl
            self.dicParsedResultOfProject[strProjUrl]["strUrl"] = strProjUrl
            #strCrawlTime
            strCrawlTime = self.cmUtility.getCtimeOfFile(strFilePath=strIntroHtmlFilePath)
            self.dicParsedResultOfProject[strProjUrl]["strCrawlTime"] = strCrawlTime
            #strProjectName
            strProjectName = self.cmUtility.extractFirstInList(lstSource=dicIntroPageRawData.get("jd-project-name", []))
            self.dicParsedResultOfProject[strProjUrl]["strProjectName"] = strProjectName
            #strLocation
            self.dicParsedResultOfProject[strProjUrl]["strLocation"] = u"China"
            #strCity
            self.dicParsedResultOfProject[strProjUrl]["strCity"] = u"China"
            #strCountry
            self.dicParsedResultOfProject[strProjUrl]["strCountry"] = u"CN"
            #strContinent
            self.dicParsedResultOfProject[strProjUrl]["strContinent"] = u"AS"
            #strDescription (全是圖檔)
            self.dicParsedResultOfProject[strProjUrl]["strDescription"] = u""
            #strIntroduction (全是圖檔)
            self.dicParsedResultOfProject[strProjUrl]["strIntroduction"] = u""
            #strCreator
            strCreator = self.cmUtility.extractFirstInList(lstSource=dicIntroPageRawData.get("jd-creator-name", []))
            self.dicParsedResultOfProject[strProjUrl]["strCreator"] = strCreator.strip()
            #strCreatorUrl
            strCreatorUrl = self.cmUtility.extractFirstInList(lstSource=dicIntroPageRawData.get("jd-creator-url", []))
            self.dicParsedResultOfProject[strProjUrl]["strCreatorUrl"] = u"http://z.jd.com" + strCreatorUrl
            #strCategory
            strCategory = re.search("JD\\\\(.*)\\\\projects\\\\[\d]+_intro.html$", strIntroHtmlFilePath).group(1)
            self.dicParsedResultOfProject[strProjUrl]["strCategory"] = strCategory
            #strSubCategory
            self.dicParsedResultOfProject[strProjUrl]["strSubCategory"] = strCategory
            #intFundTarget
            strFundTarget = self.cameoUtility.stripTextArray(lstStrText=dicIntroPageRawData.get("jd-fund-target", []))
            intFundTarget = int(re.sub("[^\d]", "", strFundTarget.strip()))
            self.dicParsedResultOfProject[strProjUrl]["intFundTarget"] = intFundTarget
            #intRaisedMoney
            strRaisedMoney = self.cmUtility.extractFirstInList(dicIntroPageRawData.get("jd-raised-money", [])).strip()
            intRaisedMoney = int(strRaisedMoney)
            self.dicParsedResultOfProject[strProjUrl]["intRaisedMoney"] = intRaisedMoney
            #fFundProgress
            fFundProgress = int((float(intRaisedMoney)/float(intFundTarget))*100.0)
            self.dicParsedResultOfProject[strProjUrl]["fFundProgress"] = fFundProgress
            #intRemainDays
            strRemainDays = self.cmUtility.extractFirstInList(dicIntroPageRawData.get("jd-remain-days", [])).strip()
            intRemainDays = int(re.sub("[^\d]", "", strRemainDays.strip()))
            self.dicParsedResultOfProject[strProjUrl]["intRemainDays"] = intRemainDays
            #intStatus
            intStatus = 0
            if intRemainDays == 0:
                if fFundProgress >= 100:
                    intStatus = 1
                else:
                    intStatus = 2
            self.dicParsedResultOfProject[strProjUrl]["intStatus"] = intStatus
            #strCurrency
            self.dicParsedResultOfProject[strProjUrl]["strCurrency"] = u"CNY"
            #strEndDate
            strEndDate = self.cmUtility.extractFirstInList(dicIntroPageRawData.get("jd-end-date", [])).strip()
            strEndDate = self.cameoUtility.parseStrDateByDateparser(strOriginDate=strEndDate)
            self.dicParsedResultOfProject[strProjUrl]["strEndDate"] = strEndDate
            #strStartDate 無此資料
            self.dicParsedResultOfProject[strProjUrl]["strStartDate"] = None
            #intFbLike
            self.dicParsedResultOfProject[strProjUrl]["intFbLike"] = 0
            #intVideoCount
            self.dicParsedResultOfProject[strProjUrl]["intVideoCount"] = 0
            #intImageCount
            intImageCount = len(dicIntroPageRawData.get("jd-img-count", []))
            self.dicParsedResultOfProject[strProjUrl]["intImageCount"] = intImageCount
            #isPMSelect 無法取得
            self.dicParsedResultOfProject[strProjUrl]["isPMSelect"] = False
            #
            # - 解析 reward.json -
            #strUrl
            #strRewardContent
            #intRewardMoney
            #intRewardBacker
            #intRewardLimit
            #strRewardShipTo and strRewardDeliveryDate
            #intRewardRetailPrice
        #_progress.html raw data (update)
        lstDicProgressPageRawData = lstLstDicRawData[1]
        for dicProgressPageRawData in lstDicProgressPageRawData:
            strProgressHtmlFilePath = dicProgressPageRawData.get("meta-data-html-filepath", None)
            logging.info("convert: %s"%strProgressHtmlFilePath)
            strProjectId = re.search("^.*\\\\([\d]+)_progress.html$", strProgressHtmlFilePath).group(1)
            strProjUrl = u"http://z.jd.com/project/details/%s.html"%strProjectId
            if strProjUrl not in self.dicParsedResultOfUpdate:
                self.dicParsedResultOfUpdate[strProjUrl] = []
            # - 解析 project.json -
            #intUpdate
            strUpdate = self.cmUtility.extractFirstInList(dicProgressPageRawData.get("jd-update", [])).strip()
            intUpdate = int(re.sub("[^\d]", "", strUpdate.strip()))
            self.dicParsedResultOfProject[strProjUrl]["intUpdate"] = intUpdate
            # - 解析 update.json -
            lstStrUpdateContent = dicProgressPageRawData.get("jd-update-content", [])
            lstStrUpdateDate = dicProgressPageRawData.get("jd-update-date", [])
            lstDicUpdateData = []
            if len(lstStrUpdateContent) == len(lstStrUpdateDate):
                for indexOfUpdate in range(len(lstStrUpdateContent)):
                    dicUpdateData = {}
                    #strUrl
                    dicUpdateData["strUrl"] = strProjUrl
                    #strUpdateContent
                    dicUpdateData["strUpdateContent"] = lstStrUpdateContent[indexOfUpdate]
                    #strUpdateDate
                    strOriginUpdateDate = lstStrUpdateDate[indexOfUpdate].strip()
                    strBaseDate = self.cmUtility.getCtimeOfFile(strFilePath=strProgressHtmlFilePath)
                    strUpdateDate = self.cameoUtility.parseStrDateByDateparser(strOriginDate=strOriginUpdateDate, strBaseDate=strBaseDate)
                    dicUpdateData["strUpdateDate"] = strUpdateDate
                    #intComment 無此資料
                    dicUpdateData["intComment"] = 0
                    #intLike 無此資料
                    dicUpdateData["intLike"] = 0
                    #strUpdateTitle 無此資料
                    dicUpdateData["strUpdateTitle"] = None
                    lstDicUpdateData.append(dicUpdateData)
            self.dicParsedResultOfUpdate[strProjUrl] = lstDicUpdateData
        #_qanda.html raw data (comment)
        lstDicQandaPageRawData = lstLstDicRawData[2]
        for dicQandaPageRawData in lstDicQandaPageRawData:
            strQandaHtmlFilePath = dicQandaPageRawData.get("meta-data-html-filepath", None)
            logging.info("convert: %s"%strQandaHtmlFilePath)
            strProjectId = re.search("^.*\\\\([\d]+)_qanda.html$", strQandaHtmlFilePath).group(1)
            strProjUrl = u"http://z.jd.com/project/details/%s.html"%strProjectId
            if strProjUrl not in self.dicParsedResultOfComment:
                self.dicParsedResultOfComment[strProjUrl] = []
            if strProjUrl not in self.dicParsedResultOfQanda:
                self.dicParsedResultOfQanda[strProjUrl] = []
            # - 解析 project.json -
            #intComment
            strComment = self.cmUtility.extractFirstInList(dicQandaPageRawData.get("jd-comment", [])).strip()
            intComment = int(re.sub("[^\d]", "", strComment.strip()))
            self.dicParsedResultOfProject[strProjUrl]["intComment"] = intComment
            # - 解析 comment.json -
            lstStrCommentName = dicQandaPageRawData.get("jd-comment-name", [])
            lstStrCommentDate = dicQandaPageRawData.get("jd-comment-date", [])
            lstStrCommentContent = dicQandaPageRawData.get("jd-comment-content", [])
            lstDicCommentData = []
            if len(lstStrCommentName) == len(lstStrCommentDate) == len(lstStrCommentContent):
                for indexOfComment in range(len(lstStrCommentName)):
                    dicCommentData = {}
                    #strUrl
                    dicCommentData["strUrl"] = strProjUrl
                    #isCreator
                    dicCommentData["isCreator"] = False
                    #strCommentName
                    dicCommentData["strCommentName"] = lstStrCommentName[indexOfComment].strip()
                    #strCommentDate
                    strOriginCommentDate = lstStrCommentDate[indexOfComment].strip()
                    strBaseDate = self.cmUtility.getCtimeOfFile(strFilePath=strQandaHtmlFilePath)
                    strCommentDate = self.cameoUtility.parseStrDateByDateparser(strOriginDate=strOriginCommentDate, strBaseDate=strBaseDate)
                    dicCommentData["strCommentDate"] = strCommentDate
                    #strCommentContent
                    dicCommentData["strCommentContent"] = lstStrCommentContent[indexOfComment].strip()
                    lstDicCommentData.append(dicCommentData)
            self.dicParsedResultOfComment[strProjUrl] = lstDicCommentData
        #_sponsor.html raw data (backer)
        lstDicSponsorPageRawData = lstLstDicRawData[3]
        for dicSponsorPageRawData in lstDicSponsorPageRawData:
            strSponsorHtmlFilePath = dicSponsorPageRawData.get("meta-data-html-filepath", None)
            logging.info("convert: %s"%strSponsorHtmlFilePath)
            strProjectId = re.search("^.*\\\\([\d]+)_sponsor.html$", strSponsorHtmlFilePath).group(1)
            strProjUrl = u"http://z.jd.com/project/details/%s.html"%strProjectId
            if strProjUrl not in self.dicParsedResultOfProject:
                self.dicParsedResultOfProject[strProjUrl] = {}
            # - 解析 project.json -
            #intBacker
            strBacker = self.cmUtility.extractFirstInList(dicSponsorPageRawData.get("jd-backer", [])).strip()
            intBacker = int(re.sub("[^\d]", "", strBacker.strip()))
            self.dicParsedResultOfProject[strProjUrl]["intBacker"] = intBacker
            #lstStrBacker
            lstStrBacker = dicSponsorPageRawData.get("jd-backer-name", [])
            self.dicParsedResultOfProject[strProjUrl]["lstStrBacker"] = lstStrBacker
        
    #轉換 profile 資訊
    def convertProfile(self, lstLstDicRawData=[]):
        #_proj.html raw data
        lstDicProjPageRawData = lstLstDicRawData[0]
        for dicProjPageRawData in lstDicProjPageRawData:
            strProjHtmlFileName = dicProjPageRawData.get("meta-data-html-filepath", None)
            logging.info("convert: %s"%strProjHtmlFileName)
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
            lstStrCreatedProjectUrl = self.stripAndCompleteProjectUrlList(lstStrOriginUrl=dicProjPageRawData.get("jd-creator-CreatedProjectUrl", []))
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
            logging.info("convert: %s"%strOrderHtmlFileName)
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
            lstStrBackedProjectUrl = self.stripAndCompleteProjectUrlList(lstStrOriginUrl=dicOrderPageRawData.get("jd-creator-BackedProjectUrl", []))
            self.dicParsedResultOfProfile[strProfUrl]["lstStrBackedProjectUrl"] = lstStrBackedProjectUrl
        
    #去除 url list 中的 javascript:location.href 並加上 http://z.jd.com 組成完整的 JD url 
    def stripAndCompleteProjectUrlList(self, lstStrOriginUrl=[]):
        lstStrResultUrl = []
        for strOriginUrl in lstStrOriginUrl:
            pattern = re.compile("(/project/details/[\d]+\.html)")
            strResultUrl = u"http://z.jd.com" + pattern.search(strOriginUrl).group(1)
            lstStrResultUrl.append(strResultUrl)
        return lstStrResultUrl
        
    #將 project convert 結果寫入 project.json update.json reward.json qanda.json comment.json 
    def flushConvertedProjectDataToJsonFile(self, strJsonFolderPath=None):
        strJsonFilePath = strJsonFolderPath + u"\\project.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfProject, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"\\update.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfUpdate, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"\\reward.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfReward, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"\\qanda.json"
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfQanda, strJsonFilePath=strJsonFilePath)
        strJsonFilePath = strJsonFolderPath + u"\\comment.json"
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