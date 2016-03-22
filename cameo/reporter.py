# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
from cameo.utility import Utility
"""
INDIEGOGO 分析報告
"""
class ReporterForINDIEGOGO:
    
    #建構子
    def __init__(self):
        self.strSourceBasedir = "cameo_res\\source_html\\INDIEGOGO"
        self.strResultBasedir = "cameo_res\\parsed_result\\INDIEGOGO"
        self.utility = Utility()
    
    #計算已下載的專案數量
    def CountDownloadedProject(self):
        pass
        
    #計算已解析的專案數量
    def CountParsedProject(self):
        #find json file path
        lstStrProjectJsonFilePath = []
        for base, dirs, files in os.walk(self.strResultBasedir): 
            for strFilename in files:
                if strFilename.endswith("project.json"):
                    strFilePath = base + "\\" + strFilename
                    lstStrProjectJsonFilePath.append(strFilePath)
        #read json file and count
        intParsedProject = 0
        for strProjectJsonFilePath in lstStrProjectJsonFilePath:
            dicProject =  self.utility.readObjectFromJsonFile(strJsonFilePath=strProjectJsonFilePath)
            print(strProjectJsonFilePath, len(dicProject))
            intParsedProject = intParsedProject + len(dicProject)
        print(intParsedProject)

"""
WEBACKERS 分析報告
"""
class ReporterForWEBACKERS:
    
    #建構子
    def __init__(self):
        self.strSourceBasedir = "cameo_res\\source_html\\WEBACKERS"
        self.strResultBasedir = "cameo_res\\parsed_result\\WEBACKERS"
        self.utility = Utility()
    
    #計算已下載的專案數量
    def CountDownloadedProject(self):
        pass
        
    #計算已解析的專案數量
    def CountParsedProject(self):
        pass
    