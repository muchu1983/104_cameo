# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
"""
shell 操作介面
"""
class CameoShell:
    
    #建構子
    def __init__(self):
        self.intShellStateCode = 0 #0-已關閉，1-已開啟，
        self.strTargetSite = None
        self.dicSpiders = {"indiegogo":"spiderForINIDEGOGO"}
        self.dicParsers = {"indiegogo":"parserForINIDEGOGO"}
        
    #顯示目前的目標網站
    def listSiteMessage(self):
        if self.strTargetSite == None:
            print("you have not select any site.")
            print("use chsite to select one.")
        else:
            print("current target site: %s"%self.strTargetSite)
    #選擇目標網站
    def changeSiteMessage(self):
        print("type one of site name below:\n")
        for strSiteName in self.dicSpiders:
            print(strSiteName+"\n")
        strInputSiteName = raw_input(">>>")
        if strInputSiteName in self.dicSpiders:
            self.strTargetSite = strInputSiteName
            print("current target site: %s"%self.strTargetSite)
        else:
            self.strTargetSite = None
            print("not found site with name: %s"%strInputSiteName)
            print("you have not select any site.")
    #顯示幫助訊息
    def printHelpMessage(self):
        strHelpText = """- HELP -
useage:
help - print this message
exit - close shell
lssite - list current site
chsite - change site
spider - run spider
parser - run parser"""
        print(strHelpText)
        
    #開啟 shell
    def openShell(self):
        self.printHelpMessage()
        self.intShellStateCode = 1
        while self.intShellStateCode != 0:
            input = raw_input(">>>")
            print("you just input: %s"%input)
            if input == "help":
                self.printHelpMessage()
            elif input == "lssite":
                self.listSiteMessage()
            elif input == "chsite":
                self.changeSiteMessage()
            elif input == "exit":
                self.intShellStateCode = 0
        