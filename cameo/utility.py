# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import re
import json
#共用工具程式
class Utility:
    
    #將 dict 物件的內容寫入到 json 檔案內
    def writeObjectToJsonFile(self, dicData=None, strJsonFilePath=None):
        with open(strJsonFilePath, "w+") as jsonFile:
            jsonFile.write(json.dumps(dicData, ensure_ascii=False, indent=4, sort_keys=True).encode("utf-8"))
    
    #取得 strBasedir 目錄中，檔名以 strSuffixes 結尾的檔案路徑
    def getFilePathListWithSuffixes(self, strBasedir=None, strSuffixes=None):
        lstStrFilePathWithSuffixes = []
        for base, dirs, files in os.walk(strBasedir): 
            if base == strBasedir:#just check base dir
                for strFilename in files:
                    if strFilename.endswith(strSuffixes):#find target files
                        strFilePath = base + "\\" + strFilename
                        lstStrFilePathWithSuffixes.append(strFilePath)
        return lstStrFilePathWithSuffixes
        
    #轉換文字成數字 (ex:26.3k -> 26300)
    def translateNumTextToPureNum(self, strNumText=None):
        strNumText = strNumText.lower()
        fPureNum = 0.0
        fFloatPartText = re.match("^([0-9\.]*)k?m?$", strNumText)
        if fFloatPartText != None:
            fFloatPartText = fFloatPartText.group(1)
            if strNumText.endswith("k"):
                fPureNum = float(fFloatPartText) * 1000
            elif strNumText.endswith("m"):
                fPureNum = float(fFloatPartText) * 1000000
            else:
                fPureNum = float(fFloatPartText) * 1
        return int(fPureNum)
        