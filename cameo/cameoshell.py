# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from cameo.parserForINDIEGOGO import ParserForINDIEGOGO
from cameo.spiderForINDIEGOGO import SpiderForINDIEGOGO
"""
shell 操作介面
"""
class CameoShell:
    
    #建構子
    def __init__(self):
        self.intShellStateCode = 0 #0-已關閉，1-已開啟，
        self.strTargetSite = None
        self.dicSpiders = {"indiegogo":SpiderForINDIEGOGO()}
        self.dicParsers = {"indiegogo":ParserForINDIEGOGO()}
        
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
        
    #顯示 spider 訊息
    def printSpiderMessage(self):
        self.listSiteMessage()
        print(self.dicSpiders[self.strTargetSite].getUseageMessage())
        lstStrInputCommand = raw_input("spider[%s]>>>"%self.strTargetSite).split(" ")
        self.dicSpiders[self.strTargetSite].runSpider(lstStrInputCommand)
        
    #顯示 parser 訊息
    def printParserMessage(self):
        self.listSiteMessage()
        print(self.dicParsers[self.strTargetSite].getUseageMessage())
        lstStrInputCommand = raw_input("parser[%s]>>>"%self.strTargetSite).split(" ")
        self.dicParsers[self.strTargetSite].runParser(lstStrInputCommand)
        
    #開啟 shell
    def openShell(self):
        self.printHelpMessage()
        print("\n")
        self.listSiteMessage()
        self.intShellStateCode = 1
        while self.intShellStateCode != 0:
            input = raw_input("\n>>>")
            print("you just input: %s"%input)
            if input == "help":
                self.printHelpMessage()
            elif input == "lssite":
                self.listSiteMessage()
            elif input == "chsite":
                self.changeSiteMessage()
            elif input == "spider":
                self.printSpiderMessage()
            elif input == "parser":
                self.printParserMessage()
            elif input == "exit":
                self.intShellStateCode = 0
        