# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from bennu.localdb import SQLite3Db
"""
本地端資料庫存取
"""
class LocalDbForTECHORANGE:
    
    #建構子
    def __init__(self):
        self.db = SQLite3Db(strResFolderPath="cameo_res")
        self.initialDb()
        
    #初取化資料庫
    def initialDb(self):
        strSQLCreateTable = ("CREATE TABLE IF NOT EXISTS techorange_news("
                             "id INTEGER PRIMARY KEY,"
                             "strNewsUrl TEXT NOT NULL,"
                             "isGot BOOLEAN NOT NULL)")
        self.db.commitSQL(strSQL=strSQLCreateTable)
        strSQLCreateTable = ("CREATE TABLE IF NOT EXISTS techorange_tag("
                             "id INTEGER PRIMARY KEY,"
                             "strTagName TEXT NOT NULL,"
                             "isGot BOOLEAN NOT NULL)")
        self.db.commitSQL(strSQL=strSQLCreateTable)
        strSQLCreateTable = ("CREATE TABLE IF NOT EXISTS techorange_newstag("
                             "id INTEGER PRIMARY KEY,"
                             "strNewsUrl TEXT NOT NULL,"
                             "strTagName TEXT NOT NULL)")
        self.db.commitSQL(strSQL=strSQLCreateTable)
        
    #若無重覆，儲存Tag
    def insertTagIfNotExists(self, strTagName=None):
        strSQL = "SELECT * FROM techorange_tag WHERE strTagName='%s'"%strTagName
        lstRowData = self.db.fetchallSQL(strSQL=strSQL)
        if len(lstRowData) == 0:
            strSQL = "INSERT INTO techorange_tag VALUES(NULL, '%s', 0)"%strTagName
            self.db.commitSQL(strSQL=strSQL)
            
    #取得所有未完成下載的 Tag 名稱
    def fetchallNotObtainedTagName(self):
        strSQL = "SELECT strTagName FROM techorange_tag WHERE isGot=0"
        lstRowData = self.db.fetchallSQL(strSQL=strSQL)
        lstStrTagName = []
        for rowData in lstRowData:
            lstStrTagName.append(rowData["strTagName"])
        return lstStrTagName
        
    #取得所有已完成下載的 Tag 名稱
    def fetchallCompletedObtainedTagName(self):
        strSQL = "SELECT strTagName FROM techorange_tag WHERE isGot=1"
        lstRowData = self.db.fetchallSQL(strSQL=strSQL)
        lstStrTagName = []
        for rowData in lstRowData:
            lstStrTagName.append(rowData["strTagName"])
        return lstStrTagName
        
    #更新 Tag 為已完成下載狀態
    def updateTagStatusIsGot(self, strTagName=None):
        strSQL = "UPDATE techorange_tag SET isGot=1 WHERE strTagName='%s'"%strTagName
        self.db.commitSQL(strSQL=strSQL)
        
    #儲存 news URL 以及 URL 所對應的 tag 
    def insertNewsUrlAndNewsTagMappingIfNotExists(self, strNewsUrl=None, strTagName=None):
        #insert news url if not exists
        strSQL = "SELECT * FROM techorange_news WHERE strNewsUrl='%s'"%strNewsUrl
        lstRowData = self.db.fetchallSQL(strSQL=strSQL)
        if len(lstRowData) == 0:
            strSQL = "INSERT INTO techorange_news VALUES(NULL, '%s', 0)"%strNewsUrl
            self.db.commitSQL(strSQL=strSQL)
        #insert news tag mapping if not exists
        strSQL = "SELECT * FROM techorange_newstag WHERE strNewsUrl='%s' AND strTagName='%s'"%(strNewsUrl, strTagName)
        lstRowData = self.db.fetchallSQL(strSQL=strSQL)
        if len(lstRowData) == 0:
            strSQL = "INSERT INTO techorange_newstag VALUES(NULL, '%s', '%s')"%(strNewsUrl, strTagName)
            self.db.commitSQL(strSQL=strSQL)
        
    #取得指定 tag 的 news url
    def fetchallNewsUrlByTagName(self, strTagName=None):
        strSQL = "SELECT * FROM techorange_newstag WHERE strTagName='%s'"%strTagName
        lstRowData = self.db.fetchallSQL(strSQL=strSQL)
        lstStrNewsUrl = []
        for rowData in lstRowData:
            lstStrNewsUrl.append(rowData["strNewsUrl"])
        return lstStrNewsUrl
        
    #檢查 news 是否已下載
    def checkNewsIsGot(self, strNewsUrl=None):
        isGot = True
        strSQL = "SELECT * FROM techorange_news WHERE strNewsUrl='%s'"%strNewsUrl
        lstRowData = self.db.fetchallSQL(strSQL=strSQL)
        for rowData in lstRowData:
            if rowData["isGot"] == 0:
                isGot = False
        return isGot
        
    #更新 news 為已完成下載狀態
    def updateNewsStatusIsGot(self, strNewsUrl=None):
        strSQL = "UPDATE techorange_news SET isGot=1 WHERE strNewsUrl='%s'"%strNewsUrl
        self.db.commitSQL(strSQL=strSQL)