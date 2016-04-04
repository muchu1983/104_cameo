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
        strSQLCreateTable = ("CREATE TABLE IF NOT EXISTS techorange_project("
                             "id INTEGER PRIMARY KEY,"
                             "strUrl TEXT,"
                             "isDownloaded BOOLEAN)")
        self.db.commitSQL(strSQL=strSQLCreateTable)
        strSQLCreateTable = ("CREATE TABLE IF NOT EXISTS techorange_tag("
                             "id INTEGER PRIMARY KEY,"
                             "strName TEXT)")
        self.db.commitSQL(strSQL=strSQLCreateTable)
        strSQLCreateTable = ("CREATE TABLE IF NOT EXISTS techorange_project_tag("
                             "id INTEGER PRIMARY KEY,"
                             "strProjectUrl TEXT,"
                             "strTagName TEXT)")
        self.db.commitSQL(strSQL=strSQLCreateTable)