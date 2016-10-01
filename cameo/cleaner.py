# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import shutil
import os
import stat
import logging
"""
清理不需要的資料
"""
class CleanerForINDIEGOGO:
    
    def __init__(self):
        self.strBasedir = "cameo_res\\source_html\\INDIEGOGO"
    
    #rmtree 失敗時呼叫此方法
    def rmtreeOnError(self, funcRmtree, strPath, _):
        logging.warning("rmtree 發生錯誤，嘗試修改檔案為可寫入模式，再進行刪除。")
        os.chmod(strPath, stat.S_IWRITE) #chmod to writeable
        if os.path.isdir(strPath):
            #處理資料夾 (使用遞迴)
            funcRmtree(strPath, onerror=self.rmtreeOnError)
        else:
            #處理檔案
            os.remove(strPath)
    
    #清除 _files 資料夾及其下所有內容
    def clean(self):
        for base, dirs, files in os.walk(self.strBasedir):
            for dir in dirs:
                if dir.endswith("_files"):
                    strDirPath = u"" + base + "\\" + dir
                    shutil.rmtree(strDirPath, onerror=self.rmtreeOnError)
