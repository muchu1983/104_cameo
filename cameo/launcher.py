# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import sys
import time
from subprocess import call
from cameo.parserForINDIEGOGO import ParserForINDIEGOGO
"""
程式進入點 (main)
"""
parser = ParserForINDIEGOGO()
#下載及解析 explore 頁面
def handleExplorePage(arg1=None):
    #download html
    call([r"cameo_sikuli\runsikulix.cmd",
          r"-r", r"cameo_sikuli\spiderForINDIEGOGO.sikuli",
          r"--args", r"explore"])
    time.sleep(10) #wait download complete
    #parse explore.html
    parser.parseExplorePage()
    
#下載及解析 category 頁面
def handleCategoryPage(arg1=None):
    call([r"cameo_sikuli\runsikulix.cmd",
          r"-r", r"cameo_sikuli\spiderForINDIEGOGO.sikuli",
          r"--args", r"category"])
    time.sleep(10) #wait download complete
    #parse category.html
    parser.parseCategoryPage()

#下載及解析 project 頁面
def handleProjectPage(arg1=None):
    call([r"cameo_sikuli\runsikulix.cmd",
          r"-r", r"cameo_sikuli\spiderForINDIEGOGO.sikuli",
          r"--args", r"project", arg1])
    time.sleep(10) #wait download complete
    parser.parseProjectDetailsPage(arg1)
    #parser.parseProjectStoryPage(arg1)
    #parser.parseProjectUpdatesPage(arg1)
    #parser.parseProjectCommentsPage(arg1)
    #parser.parseProjectBackersPage(arg1)
    #parser.parseProjectRewardPage(arg1)

#下載及解析 individuals 頁面
def handleIndividualsPage(arg1=None):
    call([r"cameo_sikuli\runsikulix.cmd",
          r"-r", r"cameo_sikuli\spiderForINDIEGOGO.sikuli",
          r"--args", r"individuals", arg1])
    time.sleep(10) #wait download complete
    parser.parseIndividualsPage(arg1)

#進入點
def entry_point():
    #lstStrArgs = sys.argv
    lstStrArgs = ["launcher.py", "individuals", "art"]
    dicSubCommandHandler = {"explore":handleExplorePage,
                            "category":handleCategoryPage,
                            "project":handleProjectPage,
                            "individuals":handleIndividualsPage,}
    strSubCommand = lstStrArgs[1]
    strSubCommandArg1 = None
    if len(lstStrArgs) == 3:
        strSubCommandArg1 = lstStrArgs[2]
    dicSubCommandHandler[strSubCommand](strSubCommandArg1)

if __name__ == '__main__':
    entry_point()