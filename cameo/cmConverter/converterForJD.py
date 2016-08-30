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
        self.dicParsedResultOfQanda = {} #qanda.json 資料
        self.dicParsedResultOfReward = {} #reward.json 資料
        self.dicParsedResultOfProfile = {} #profile.json 資料
        
    #轉換 project 資訊
    def convertProject(self, lstLstDicRawData=[]):
        pass
        
    #轉換 profile 資訊
    def convertProfile(self, lstLstDicRawData=[]):
        """
        範例：
        "http://z.jd.com/funderCenter.action?flag=2&id=10437": {
            "intBackedCount": 0, 
            "intCreatedCount": 2, 
            "intFailedProject": null, 
            "intFbFriend": null, 
            "intLiveProject": null, 
            "intSuccessProject": null, 
            "isBacker": false, 
            "isCreator": true, 
            "lstStrBackedProject": [], 
            "lstStrBackedProjectUrl": [], 
            "lstStrCreatedProject": [
                "莱仕邦智能电动折叠跑步机", 
                "莱仕邦办公走步机"
            ], 
            "lstStrCreatedProjectUrl": [
                "http://z.jd.com/project/details/23486.html", 
                "http://z.jd.com/project/details/10437.html"
            ], 
            "lstStrSocialNetwork": null, 
            "strCity": "China", 
            "strContinent": "AS", 
            "strCountry": "CN", 
            "strDescription": "LifeSpan莱仕邦总公司于2001年设立于美国盐湖城，在国际市场上提供全系列家用、商用和办公系列的健身器材，除了美国总部之外，LifeSpan莱仕邦也在世界主要国家设立经销商，以提供更完善的服务质量。将健康生活方式的理念结合高端科技，运用在办公走步机上，有效的落实个人健康管理，让人们迈向更好的生活。", 
            "strIdentityName": "LifeSpan莱仕邦", 
            "strLastLoginDate": null, 
            "strLocation": "China", 
            "strName": "LifeSpan莱仕邦", 
            "strUrl": "http://z.jd.com/funderCenter.action?flag=2&id=10437"
        }, ...
        """
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
        
    #將 convert 結果寫入 json
    def flushConvertedDataToJsonFile(self, strJsonFilePath=None):
        self.cmUtility.writeObjectToJsonFile(dicData=self.dicParsedResultOfProfile, strJsonFilePath=strJsonFilePath)
        self.dicParsedResultOfProfile = {}
        