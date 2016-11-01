# coding: utf-8
import pymongo
import json
import datetime

class MonitorUtility:
    
    def __init__(self, strIp=None, strCrawlerName=None):
        self.client = None
        self.strIp = strIp
        self.strCrawlerName = strCrawlerName
    
    
    def getClient(self):
        strURL = "mongodb://203.66.65.239/"
        if(self.client == None):
            self.client = pymongo.MongoClient(strURL)
        return self.client

    def getDatabase(self):
        return self.getClient().tier
        
    def updateMonitorStatus(self,
        strIp=None,
        strCrawlerName=None,
        strJob=None,
        strCrawlerUrl=None,
        dtCrawlerJobTime=None,
        dtStratCrawlingTime=None,
        dtParsingTime=None,
        dtImporterTime=None,
        dtUploadingFTPTime=None,
        dtErrorMsgTime=None,
        strErrorMsg=None
    ):
        collectionMonitor = self.getDatabase().ModelCrawlerMonitor
        if strCrawlerName:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strCrawlerName":strCrawlerName
                    }
                },
                upsert=True
            )
        if strJob:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strJob":strJob
                    }
                },
                upsert=True
            )
        if strCrawlerUrl:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strCrawlerUrl":strCrawlerUrl
                    }
                },
                upsert=True
            )
        if dtCrawlerJobTime:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strCrawlerJobTime":dtCrawlerJobTime.strftime("%Y/%m/%d %H:%M:%S")
                    }
                },
                upsert=True
            )
        if dtStratCrawlingTime:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strStratCrawlingTime":dtStratCrawlingTime.strftime("%Y/%m/%d %H:%M:%S")
                    }
                },
                upsert=True
            )
        if dtParsingTime:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strParsingTime":dtParsingTime.strftime("%Y/%m/%d %H:%M:%S")
                    }
                },
                upsert=True
            )
        if dtImporterTime:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strImporterTime":dtImporterTime.strftime("%Y/%m/%d %H:%M:%S")
                    }
                },
                upsert=True
            )
        if dtUploadingFTPTime:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strUploadingFTPTime":dtUploadingFTPTime.strftime("%Y/%m/%d %H:%M:%S")
                    }
                },
                upsert=True
            )
        if dtErrorMsgTime:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strErrorMsgTime":dtErrorMsgTime.strftime("%Y/%m/%d %H:%M:%S")
                    }
                },
                upsert=True
            )
        if strErrorMsg:
            collectionMonitor.update_one(
                {"strIp": self.strIp},
                {
                    "$set":{
                        "strErrorMsg":strErrorMsg
                    }
                },
                upsert=True
            )
        