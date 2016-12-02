# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from pymongo import MongoClient
"""
外部資料庫存取
"""
#外部資料庫 cameo 210.65.11.231
class CameoMongoDb:
    
    #建構子
    def __init__(self):
        logging.info("connect to cameo 210.65.11.231 mongo db.")
        self.client = MongoClient("mongodb://root:CameoRoot12#$@210.65.11.231/")
        
    #解構子
    def __del__(self):
        logging.info("close cameo 210.65.11.231 mongo db connection.")
        self.client.close() #關閉資料庫連線
        
    #取得 mongodb client
    def getClient(self):
        return self.client
        
#外部資料庫 cameo 203.66.65.239
class CameoMongoDbForMonitor:
    
    #建構子
    def __init__(self):
        logging.info("connect to cameo 203.66.65.239 mongo db.")
        self.client = MongoClient("mongodb://203.66.65.239/")
        
    #解構子
    def __del__(self):
        logging.info("close cameo 203.66.65.239 mongo db connection.")
        self.client.close() #關閉資料庫連線
        
    #取得 mongodb client
    def getClient(self):
        return self.client
        
#cameo mongodb tier
class ExternalDbOfCameo:
    #建構子
    def __init__(self):
        self.mongodb = CameoMongoDb().getClient().tier
    
#匯入json
class ExternalDbForJsonImporter:
    
    #建構子
    def __init__(self):
        self.mongodb = CameoMongoDb().getClient().tier
        
#匯率API
class ExternalDbForCurrencyApi:
    
    #建構子
    def __init__(self):
        self.mongodb = CameoMongoDb().getClient().tier
        