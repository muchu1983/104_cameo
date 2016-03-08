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
        
    #轉換 簡化數字字串 成 純數字 (ex:26.3k -> 26300)
    def translateNumTextToPureNum(self, strNumText=None):
        strNumText = strNumText.lower()
        fPureNum = 0.0
        strFloatPartText = re.match("^([0-9\.]*)k?m?$", strNumText)
        if strFloatPartText != None:
            strFloatPartText = strFloatPartText.group(1)
            if strNumText.endswith("k"):
                fPureNum = float(strFloatPartText) * 1000
            elif strNumText.endswith("m"):
                fPureNum = float(strFloatPartText) * 1000000
            else:
                fPureNum = float(strFloatPartText) * 1
        return int(fPureNum)
        
    #轉換 剩餘日期表示字串 成 純數字 (ex:100 day left -> 100)
    def translateTimeleftTextToPureNum(self, strTimeleftText=None):
        strTimeleftText = strTimeleftText.lower().strip()
        intDays = 0
        if "hours left" in strTimeleftText:
            strHoursText = re.match("^([0-9]*) hours left$", strTimeleftText)
            if strHoursText != None:
                strHoursText = strHoursText.group(1)
                intDays = (int(strHoursText)+24)/24
        if "days left" in strTimeleftText:
            strDaysText = re.match("^([0-9]*) days left$", strTimeleftText)
            if strDaysText != None:
                strDaysText = strDaysText.group(1)
                intDays = int(strDaysText)
        return intDays