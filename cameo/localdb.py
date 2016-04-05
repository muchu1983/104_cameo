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
    def insertTagIFNotExists(self, strTagName=None):
        strSQL = "SELECT * FROM techorange_tag WHERE strTagName='%s'"%strTagName
        fetchedData = self.db.fetchallSQL(strSQL=strSQL)
        if len(fetchedData) == 0:
            strSQL = "INSERT INTO techorange_tag VALUES(NULL, '%s', 0)"%strTagName
            self.db.commitSQL(strSQL=strSQL)