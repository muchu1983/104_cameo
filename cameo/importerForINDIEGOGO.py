#coding: utf-8
import os
import sys
import time
import datetime
import dateparser
import math
import re
import logging
from cameo.utility import Utility
from cameo.externaldb import ExternalDbForJsonImporter
#from cameo.localdb import LocalDbForJsonImporter #測試用本地端 db

class ImporterForINDIEGOGO:
    
    #建構子
    def __init__(self):
        self.utility = Utility()
        self.db = ExternalDbForJsonImporter().mongodb
        #self.db = LocalDbForJsonImporter().mongodb #測試用本地端 db
        self.dicSubCommandHandler = {"import":[self.importJsonData]}
        self.dicCategoryMapping = None
        self.lstStrCategory = [
            "animals", "art", "comic", "community", "dance",
            "design", "education", "environment", "fashion",
            "film", "food", "gaming", "health", "music", "photography",
            "politics", "religion", "small_business", "sports",
            "technology", "theatre", "transmedia", "video_web", "writing"
        ]
        
    #取得 importer 使用資訊
    def getUseageMessage(self):
        return (
            "- INDIEGOGO -\n"
            "useage:\n"
            "import - import json to database \n"
        )
        
    #執行 importer
    def runImporter(self, lstSubcommand=None):
        strSubcommand = lstSubcommand[0]
        strArg1 = None
        if len(lstSubcommand) == 2:
            strArg1 = lstSubcommand[1]
        for handler in self.dicSubCommandHandler[strSubcommand]:
            handler(strArg1)
            
    def importJsonData(self, uselessArg1=None):
        #讀取 分類對應表
        self.loadCategoryMapping()
        #逐一分類匯入
        for strCategory in self.lstStrCategory:
            self.importProjectJson(strCategory)
            self.importPersonJson(strCategory)
            
    def importProjectJson(self, strCategory):
        logging.info("[Import %s]"%strCategory)
        dicTotalProject = self.utility.readObjectFromJsonFile(strJsonFilePath=self.getParsedProjectFilePath(strCategory))
        dicTotalUpdate = self.utility.readObjectFromJsonFile(strJsonFilePath=self.getParsedUpdateFilePath(strCategory))
        dicTotalReward = self.utility.readObjectFromJsonFile(strJsonFilePath=self.getParsedRewardFilePath(strCategory))
        dicTotalComment = self.utility.readObjectFromJsonFile(strJsonFilePath=self.getParsedCommentFilePath(strCategory))    
        collectionProj = self.db.ModelFundProject
        for strUrl, dicProject in dicTotalProject.items():
            if("fFundProgress" not in dicProject):
                continue
            logging.info("[Import project]: %s"%strUrl)
            dicCategory = self.dicCategoryMapping[dicProject["strCategory"]]
            bIsNew = collectionProj.count({"strUrl": strUrl}) == 0
            dateDelta = datetime.datetime.now() - datetime.datetime.strptime(dicProject["strCrawlTime"], "%Y-%m-%d")
            #project: 固定資訊只有在db上沒有時才會匯入，status為變動資訊，每次匯入時會確認是否為新的，若是新的則會匯入
            if(bIsNew):
                logging.info(dicProject["strEndDate"])
                if(dicProject["strEndDate"] != "indemand" and dicProject["strEndDate"] != "closed"):
                    dicProject["strEndDate"] = self.getCorrectFormatDateTime(dicProject["strEndDate"])
                else:
                    dicProject["strEndDate"] = None
                dicProject.setdefault("lstIntCategoryId", [dicCategory["intCategoryId"]])
                dicProject.setdefault("lstStrCategory", [dicCategory["strCategory"]])
                dicProject.setdefault("lstIntSubCategoryId", [dicCategory["intSubCategoryId"]])
                dicProject.setdefault("lstStrSubCategory", [dicCategory["strSubCategory"]])
                dicProject.setdefault("lstDicComment", [])
                dicProject.setdefault("lstDicQna", [])
                dicProject.setdefault("lstDicReward", [])
                dicProject.setdefault("lstDicUpdate", [])
                dicProject.setdefault("lstDicStatus", [])
                collectionProj.insert_one(dicProject).inserted_id
            else:
                pass
            dicStatus = {}
            dicStatus.setdefault("intStatus", dicProject.pop("intStatus", 0))
            dicStatus.setdefault("intRemainDays", dicProject.pop("intRemainDays", 0))
            dicStatus.setdefault("fFundProgress", dicProject.pop("fFundProgress", .0))
            dicStatus.setdefault("intRaisedMoney", dicProject.pop("intRaisedMoney", 0))
            dicStatus.setdefault("intUpdate", dicProject.pop("intUpdate", 0))
            dicStatus.setdefault("intBacker", dicProject.pop("intBacker", 0))
            dicStatus.setdefault("intComment", dicProject.pop("intComment", 0))
            dicStatus.setdefault("intFbLike", dicProject.pop("intFbLike", 0))
            dicStatus.setdefault("isDemand", dicProject.pop("isDemand", False))
            dicStatus.setdefault("isAON", dicProject.pop("isAON", False))
            dicStatus.setdefault("strDate", self.getCorrectFormatDateTime(dicProject["strCrawlTime"]))
            collectionProj.update({"strUrl": strUrl},  {"$addToSet":{"lstDicStatus":dicStatus}}, upsert = True)
            collectionProj.update({"strUrl": strUrl}, {"$set": {"strCrawlTime": self.getCorrectFormatDateTime(dicProject["strCrawlTime"])}})
            #lstStrTag
            lstStrTag = self.makeTagFieldOnModelFundProject(
                strCategory=dicProject["strCategory"],
                strSubCategory=dicProject["strSubCategory"],
                lstStrCategory=[dicCategory["strCategory"]],
                lstStrSubCategory=[dicCategory["strSubCategory"]]
            )
            collectionProj.update_one(
                {"strUrl": strUrl},
                {
                    "$set":{
                        "lstStrTag":lstStrTag
                    }
                },
                upsert=True
            )
            #Backer: 如果有新的backer會加入db
            collectionProj.update({"strUrl": strUrl},  {"$addToSet":{"lstStrBacker": {"$each":dicProject["lstStrBacker"]}}})
            #Comment: 使用新的array蓋掉原來array
            lstDicComment = dicTotalComment[strUrl]
            for dicComment in lstDicComment:
                if(dicComment["strCommentDate"] != None and len(dicComment["strCommentDate"]) > 0):
                    dicComment["strCommentDate"] = dicComment["strCommentDate"].replace("over ", "").replace("almost ", "")
                    dateComment = dateparser.parse(dicComment["strCommentDate"]) - dateDelta
                    dicComment["strCommentDate"] = dateComment.strftime("%Y/%m/%d")
            collectionProj.update({"strUrl": strUrl},  {"$set":{"lstDicComment": lstDicComment}})
            #Reward: 使用新的array蓋掉原來array
            lstDicReward = dicTotalReward[strUrl]
            for dicReward in lstDicReward:
                if(dicReward["strRewardDeliveryDate"] != None and len(dicReward["strRewardDeliveryDate"]) > 0):
                    dicReward["strRewardDeliveryDate"] = dateparser.parse(dicReward["strRewardDeliveryDate"]).strftime("%Y/%m/%d")
            collectionProj.update({"strUrl": strUrl},  {"$set":{"lstDicReward": lstDicReward}})
            #Update: 使用新的array蓋掉原來array
            lstDicUpdate = dicTotalUpdate[strUrl]
            for dicUpdate in lstDicUpdate:
                if(dicUpdate["strUpdateDate"] != None and len(dicUpdate["strUpdateDate"]) > 0):
                    dicUpdate["strUpdateDate"] = dicUpdate["strUpdateDate"].replace("over ", "").replace("almost ", "")
                    dateUpdate = dateparser.parse(dicUpdate["strUpdateDate"]) - dateDelta
                    dicUpdate["strUpdateDate"] = dateUpdate.strftime("%Y/%m/%d")
            collectionProj.update({"strUrl": strUrl},  {"$set":{"lstDicUpdate": lstDicUpdate}})
    
    def makeTagFieldOnModelFundProject(self, strCategory=None, strSubCategory=None, lstStrCategory=[], lstStrSubCategory=[]):
        lstStrTag = []
        lstStrTag.append(strCategory)
        lstStrTag.append(strSubCategory)
        lstStrTag = lstStrTag + lstStrCategory
        lstStrTag = lstStrTag + lstStrSubCategory
        lstStrTag = list(set(lstStrTag))
        return lstStrTag
    
    def importPersonJson(self, strCategory):
        dicTotalPerson = self.utility.readObjectFromJsonFile(strJsonFilePath=self.getParsedProfileFilePath(strCategory))
        collectionPerson = self.db.ModelRewardPerson
        for strUrl, dicPerson in dicTotalPerson.items():
            logging.info("[Import person]: %s"%strUrl)
            dicPerson.setdefault("strSource", "INDIEGOGO")
            #collectionPerson.update({"strUrl": strUrl},  dicPerson, upsert = True)
            bIsNew = collectionPerson.count({"strUrl": dicPerson["strUrl"]}) == 0
            if(bIsNew):
                collectionPerson.insert_one(dicPerson)
            else:
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"lstStrCreatedProjectUrl": dicPerson["lstStrCreatedProjectUrl"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"lstStrBackedProjectUrl": dicPerson["lstStrBackedProjectUrl"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"intSuccessProject": dicPerson["intSuccessProject"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"intLiveProject": dicPerson["intLiveProject"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"intFailedProject": dicPerson["intFailedProject"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"intCreatedCount": dicPerson["intCreatedCount"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"intBackedCount": dicPerson["intBackedCount"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"intFbFriend": dicPerson["intFbFriend"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"isCreator": dicPerson["isCreator"]}})
                collectionPerson.update({"strUrl": strUrl},  {"$set":{"isBacker": dicPerson["isBacker"]}})
    
    def strParsedResultPath(self):
        return u"cameo_res/parsed_result/INDIEGOGO"
    
    def getParsedProjectFilePath(self, strCategory):
        return self.strParsedResultPath() + "/" + strCategory + "/projects/project.json"
    
    def getParsedUpdateFilePath(self, strCategory):
        return self.strParsedResultPath() + "/" + strCategory + "/projects/update.json"
    
    def getParsedCommentFilePath(self, strCategory):
        return self.strParsedResultPath() + "/" + strCategory + "/projects/comment.json"
    
    def getParsedRewardFilePath(self, strCategory):
        return self.strParsedResultPath() + "/" + strCategory + "/projects/reward.json"
    
    def getParsedProfileFilePath(self, strCategory):
        return self.strParsedResultPath() + "/" + strCategory + "/profiles/profile.json"
    
    def getCorrectFormatDateTime(self, strDate):
        return datetime.datetime.strptime(strDate, "%Y-%m-%d").strftime("%Y/%m/%d")
    
    def loadCategoryMapping(self):
        strCategoryMappingFilePath = u"cameo_res/categoryMappingForINDIEGOGO.json"
        self.dicCategoryMapping = self.utility.readObjectFromJsonFile(strJsonFilePath=strCategoryMappingFilePath)
