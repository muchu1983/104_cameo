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
"""
清理不需要的資料
"""
class CleanerForINDIEGOGO:
    
    def __init__(self):
        self.strBasedir = "cameo_res\\source_html\\INDIEGOGO"
    
    def removeReadonly(self, funcRmtree, strPath, _):
        print(type(strPath), strPath)
        os.chmod(strPath.decode("utf-8"), stat.S_IWRITE)
        funcRmtree(strPath)
    
    def clean(self):
        for base, dirs, files in os.walk(self.strBasedir):
            for dir in dirs:
                if dir.endswith("_files"):
                    strDirPath = base + "\\" + dir
                    shutil.rmtree(strDirPath, onerror=self.removeReadonly)
