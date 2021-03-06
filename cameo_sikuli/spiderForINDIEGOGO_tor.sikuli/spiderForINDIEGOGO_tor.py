# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import sys
import re
import logging
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
screen = Screen()
dicRegion = {"regUp":Region(0,0,screen.getW(),screen.getH()/2),
          "regDown":Region(0,screen.getH()/2,screen.getW(),screen.getH()/2),
          "regLeft":Region(0,0,screen.getW()/2,screen.getH()),
          "regRight":Region(screen.getW()/2,0,screen.getW()/2,screen.getH()),
          "regNE":Region(screen.getW()/2,0,screen.getW()/2,screen.getH()/2),
          "regSE":Region(screen.getW()/2,screen.getH()/2,screen.getW()/2,screen.getH()/2),
          "regSW":Region(0,screen.getH()/2,screen.getW()/2,screen.getH()/2),
          "regNW":Region(0,0,screen.getW()/2,screen.getH()/2),
          "regCenter":Region(screen.getW()/4,screen.getH()/4,screen.getW()/2,screen.getH()/2)
         }
dicPng = {"tor_close":Pattern("tor_close.png").targetOffset(-14,0),
        "tor_maximized_window":"tor_maximized_window.png",
        "tor_home":"tor_home.png",
        "tor_stop":"tor_stop.png",
        "tor_reload":"tor_reload.png",
        "tor_not_now":"tor_not_now.png",
        "tor_download_finished":"tor_download_finished.png",
        "page_end_about":"page_end_about.png",
        "page_end_camp":"page_end_camp.png",
        "page_cate_more":"page_cate_more.png",
        "page_ucb_more":"page_ucb_more.png", #different between before click and after click
        "page_new_style_check":"page_new_style_check.png",
        "page_blur_story":"page_blur_story.png",
        "page_focus_profile":"page_focus_profile.png", 
        "page_story_details":"page_story_details.png",
        "page_details_about":"page_details_about.png",
        "page_explore":"page_explore.png",
        "page_not_found":"page_not_found.png",
        "page_not_found_2":"page_not_found_2.png",
        "page_not_right":"page_not_right.png",
        "page_your_interruption":"page_your_interruption.png",
        "page_proxy_error":"page_proxy_error.png",
        "page_currently_updated":"currently_updated.png",
        "page_under_review":"page_under_review.png",
        "os_foldername_bar":Pattern("os_foldername_bar.png").targetOffset(10,0),
        "os_filename_bar":Pattern("os_filename_bar.png").targetOffset(48,0),
        "os_right_save_as":"os_right_save_as.png",
        "os_save_btn":"os_save_btn.png",
        }
lstStrCategoryName = ["animals", "art", "comic", "community", "dance",
                "design", "education", "environment", "fashion",
                "film", "food", "gaming", "health", "music", "photography",
                "politics", "religion", "small_business", "sports",
                "technology", "theatre", "transmedia", "video_web", "writing"]
sysClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
strBaseResFolderPath = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res"
#open tor brower
def openTor():
    #close prev tor
    if dicRegion["regNW"].exists(dicPng["tor_close"]):
        dicRegion["regNW"].click(dicPng["tor_close"])
    wait(10)
    #re-open new tor
    App.open("C:\\Users\\Administrator\\Desktop\\Tor Browser\\Browser\\firefox.exe")
    wait(10)#wait to running
    dicRegion["regNW"].wait(dicPng["tor_home"], 300)
    dicRegion["regNW"].click(dicPng["tor_home"])
    dicRegion["regNE"].waitVanish(dicPng["tor_stop"], 300)
    dicRegion["regNE"].wait(dicPng["tor_reload"], 300)
    #maximized tor window
    if dicRegion["regUp"].exists(dicPng["tor_maximized_window"]):
        dicRegion["regUp"].click(dicPng["tor_maximized_window"])
        wait(2)
# delete origin text
def delOriginText():
    type("a", KeyModifier.CTRL)
    wait(0.5)
    type(Key.BACKSPACE)
    wait(0.5)
# paste text by using clipboard
def pasteClipboardText(strText=None):
    sysClipboard.setContents(StringSelection(u""+strText), None)
    wait(0.5)
    type("v", KeyModifier.CTRL)
    wait(0.5)
#roll to page end
def rollToPageEnd():
    type(Key.END)
    dicRegion["regLeft"].wait(dicPng["page_end_about"], 300)
# open all project
def unfoldCategoryPage():
    rollToPageEnd()
    for uptime in range(6):
        type(Key.UP)
    dicRegion["regLeft"].wait(dicPng["page_end_camp"], 300)
    while(dicRegion["regCenter"].exists(dicPng["page_cate_more"])):
        dicRegion["regCenter"].click(dicPng["page_cate_more"])
        dicRegion["regLeft"].waitVanish(dicPng["page_end_camp"], 300)
        wait(5)
        rollToPageEnd()
        for uptime in range(6):
            type(Key.UP)
            wait(0.5)
        dicRegion["regLeft"].wait(dicPng["page_end_camp"], 300)
#unfold (updates comments backers) showmore
def unfoldUCBShowmore():
    while(not dicRegion["regLeft"].exists(dicPng["page_end_about"])):
        type(Key.PAGE_DOWN)
        wait(0.5)
        if dicRegion["regDown"].exists(dicPng["page_ucb_more"]):
            dicRegion["regDown"].click(dicPng["page_ucb_more"])
            dicRegion["regDown"].waitVanish(dicPng["page_ucb_more"], 300)
            wait(2)
    type(Key.HOME)
    dicRegion["regSW"].wait(dicPng["page_blur_story"], 300)
#pause if interruption page found
def checkAndPauseBeforeSave():
    if dicRegion["regLeft"].exists(dicPng["page_your_interruption"]):
        popup(u"distil networks found us! （╯‵□′）╯︵┴─┴")
    if dicRegion["regUp"].exists(dicPng["page_proxy_error"]):
        popup(u"proxy error! （╯‵□′）╯︵┴─┴")
#type url on tor
def typeUrlOnTor(strUrlText=None):
    while True:
        type("l", KeyModifier.CTRL)
        wait(0.5)
        delOriginText()
        pasteClipboardText(strText=strUrlText)
        wait(0.5)
        type(Key.ENTER)
        wait(0.5)
        dicRegion["regNE"].waitVanish(dicPng["tor_stop"], 300)
        dicRegion["regNE"].wait(dicPng["tor_reload"], 300)
        wait(5)
        #recheck for server may redirect to home page
        dicRegion["regNE"].waitVanish(dicPng["tor_stop"], 300)
        dicRegion["regNE"].wait(dicPng["tor_reload"], 300)
        wait(0.5)
        #click tor_not_now popup
        if dicRegion["regNW"].exists(dicPng["tor_not_now"]):
           dicRegion["regNW"].click(dicPng["tor_not_now"])
        #check page "something not right" show?
        if dicRegion["regUp"].exists(dicPng["page_not_right"]):
            #restart tor and run typeUrlOnTor again
            openTor()
        else:
            #ok everything is right, go out while loop
            break
# go to explore page
def goExplorePage():
    openTor()
    typeUrlOnTor(strUrlText="https://www.indiegogo.com/explore")
    dicRegion["regUp"].wait(dicPng["page_explore"], 300)
    dicRegion["regNE"].waitVanish(dicPng["tor_stop"], 300)
    dicRegion["regNE"].wait(dicPng["tor_reload"], 300)
#choose folder at save progress
def typeFolderPath(strFolderPath=None):
    dicRegion["regNW"].wait(dicPng["os_foldername_bar"], 300)
    dicRegion["regNW"].click(dicPng["os_foldername_bar"])
    wait(0.5)
    delOriginText()
    pasteClipboardText(strText=strFolderPath)
    wait(0.5)
    type(Key.ENTER)
    wait(0.5)
#rightclick on image to save current page
def rightClickSaveCurrentPage(onImage=None, strFolderPath=None, strFilename=None):
    logging.info("prepare to save " + strFilename)
    dicRegion["regNE"].waitVanish(dicPng["tor_stop"], 300)
    dicRegion["regNE"].wait(dicPng["tor_reload"], 300)
    checkAndPauseBeforeSave()
    rightClick(onImage)
    dicRegion["regUp"].wait(dicPng["os_right_save_as"], 300)
    dicRegion["regUp"].click(dicPng["os_right_save_as"])
    dicRegion["regCenter"].wait(dicPng["os_save_btn"], 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    dicRegion["regLeft"].click(dicPng["os_filename_bar"])
    wait(0.5)
    delOriginText()
    wait(0.5)
    pasteClipboardText(strText=strFilename)
    wait(0.5)
    dicRegion["regCenter"].click(dicPng["os_save_btn"])
    wait(0.5)
    dicRegion["regSW"].wait(dicPng["tor_download_finished"], 600)#wait save complete
#ask tor save current page
def saveCurrentPage(strFolderPath=None, strFilename=None):
    logging.info("prepare to save " + strFilename)
    dicRegion["regNE"].waitVanish(dicPng["tor_stop"], 300)
    dicRegion["regNE"].wait(dicPng["tor_reload"], 300)
    checkAndPauseBeforeSave()
    type("s", KeyModifier.CTRL)
    dicRegion["regCenter"].wait(dicPng["os_save_btn"], 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    dicRegion["regLeft"].click(dicPng["os_filename_bar"])
    wait(0.5)
    delOriginText()
    wait(0.5)
    pasteClipboardText(strText=strFilename)
    wait(0.5)
    dicRegion["regCenter"].click(dicPng["os_save_btn"])
    wait(0.5)
    dicRegion["regSW"].wait(dicPng["tor_download_finished"], 600)#wait save complete
#download explore pages
def downloadExplorePages():
    goExplorePage()
    strExploreFolderPath = strBaseResFolderPath + r"\source_html\INDIEGOGO"
    if not os.path.exists(strExploreFolderPath):
        os.mkdir(strExploreFolderPath)
    saveCurrentPage(strFolderPath=strExploreFolderPath, strFilename="explore.html")
#download category pages
def downloadCategoryPages():
    strCategoryUrlListFilePath = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\category_url_list.txt"
    catUrlListFile = open(strCategoryUrlListFilePath)
    for strCategoryUrl in catUrlListFile:#category loop
        strCategoryName = r"" + re.search("^https://www.indiegogo.com/explore#/browse/(.*)$" ,strCategoryUrl).group(1)
        strCategoryFolderPath = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s"%(strCategoryName)
        if not os.path.exists(strCategoryFolderPath):
            os.mkdir(strCategoryFolderPath) #mkdir category
        strCategoryFilePath = strCategoryFolderPath + r"\category.html"
        if not os.path.exists(strCategoryFilePath):#check category.html
            openTor()
            typeUrlOnTor(strUrlText=strCategoryUrl)
            dicRegion["regNE"].waitVanish(dicPng["tor_stop"], 300)
            dicRegion["regNE"].wait(dicPng["tor_reload"], 300)
            unfoldCategoryPage()
            saveCurrentPage(strFolderPath=strCategoryFolderPath, strFilename="category.html")
    catUrlListFile.close()
#download project pages
def downloadProjectPages(strTargetCategory=None):
    if strTargetCategory == "automode": #自動抓取所有分類的專案 html
        for strCategoryName in lstStrCategoryName:
            downloadProjectPages(strTargetCategory=strCategoryName)
        return #自動完成就 return
    strProjUrlListFilePathTemplate = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\%s\project_url_list.txt"
    strProjectsFolderPathTemplate = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s\projects"   
    strProjectsFolderPath = strProjectsFolderPathTemplate % (strTargetCategory)
    if not os.path.exists(strProjectsFolderPath):
        os.mkdir(strProjectsFolderPath)#mkdir source_html/INDIEGOGO/Category/pojects/
    strProjUrlListFilePath = strProjUrlListFilePathTemplate % (strTargetCategory)
    projUrlListFile = open(strProjUrlListFilePath, "r") 
    for strProjUrl in projUrlListFile:
        strProjName = re.search("^https://www.indiegogo.com/projects/(.*)/.{4}$", strProjUrl).group(1)
        strProjUrl = strProjUrl.strip()[:-5] # remove "/pica"
        #check html file exists
        isProjHtmlFileMissing = False
        lstStrProjHtmlFileExtension = ["_details.html", "_story.html", "_updates.html", "_comments.html", "_backers.html"]
        for strProjHtmlFileExtension in lstStrProjHtmlFileExtension:
            strProjHtmlFilePath = strProjectsFolderPath + os.sep + strProjName + strProjHtmlFileExtension
            if not os.path.exists(strProjHtmlFilePath):
                isProjHtmlFileMissing = True
        if isProjHtmlFileMissing:
            wait(10) #wait 10 sec per project
            #delete remaining project html files
            for strProjHtmlFileExtension in lstStrProjHtmlFileExtension:
                strProjHtmlFilePath = strProjectsFolderPath + os.sep + strProjName + strProjHtmlFileExtension
                if os.path.exists(strProjHtmlFilePath):
                    os.remove(strProjHtmlFilePath)
            openTor() #open tor 
            typeUrlOnTor(strUrlText=strProjUrl)
            wait(0.5)
            #check page "something not right" show?
            while(dicRegion["regUp"].exists(dicPng["page_not_right"])):
                openTor() #reopen tor for reload current page
                typeUrlOnTor(strUrlText=strProjUrl)
                wait(0.5)
        else:
            continue #skip this url
        #check page not found or is currently updated or under review
        if dicRegion["regUp"].exists(dicPng["page_not_found"]) or dicRegion["regUp"].exists(dicPng["page_not_found_2"]) or dicRegion["regUp"].exists(dicPng["page_currently_updated"]) or dicRegion["regUp"].exists(dicPng["page_under_review"]):
            continue #skip this url
        #wait load completed
        dicRegion["regRight"].wait(dicPng["page_new_style_check"], 300)
        #save story html
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjName + "_story.html")
        #save see more details html 
        dicRegion["regCenter"].wait(dicPng["page_story_details"], 300)
        dicRegion["regCenter"].click(dicPng["page_story_details"])
        dicRegion["regUp"].wait(dicPng["page_details_about"], 300)
        rightClickSaveCurrentPage(onImage=dicPng["page_details_about"], strFolderPath=strProjectsFolderPath, strFilename=strProjName + "_details.html")
        #save updates html
        openTor()
        typeUrlOnTor(strUrlText=strProjUrl + "#/updates")
        wait(0.5)
        #unfoldUCBShowmore()
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjName + "_updates.html")
        #save comments html
        openTor()
        typeUrlOnTor(strUrlText=strProjUrl + "#/comments")
        wait(0.5)
        #unfoldUCBShowmore()
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjName + "_comments.html")
        #save backers html
        openTor()
        typeUrlOnTor(strUrlText=strProjUrl + "#/backers")
        wait(0.5)
        #unfoldUCBShowmore()
        saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjName + "_backers.html")
    projUrlListFile.close()
#download individuals pages
def downloadIndividualsPages(strTargetCategory=None):
    if strTargetCategory == "automode": #自動抓取所有分類的個人資料 html
        for strCategoryName in lstStrCategoryName:
            downloadIndividualsPages(strTargetCategory=strCategoryName)
        return #自動完成就 return
    strIndividualsUrlListFilePathTemplate = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\%s\individuals_url_list.txt"
    strIndividualsFolderPathTemplate = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s\profiles"
    strIndividualsFolderPath = strIndividualsFolderPathTemplate % (strTargetCategory)
    if not os.path.exists(strIndividualsFolderPath):
        os.mkdir(strIndividualsFolderPath)#mkdir source_html/INDIEGOGO/Category/profiles/
    strIndividualsUrlListFilePath = strIndividualsUrlListFilePathTemplate % (strTargetCategory)
    individualsUrlListFile = open(strIndividualsUrlListFilePath, "r") 
    for strIndividualsUrl in individualsUrlListFile:
        strIndividualsId = re.search("^https://www.indiegogo.com/individuals/(.*)$", strIndividualsUrl).group(1)
        #check html exists
        isIndividualsHtmlFileMissing = False
        lstStrIndividualsHtmlFileExtension = ["_profile.html", "_campaigns.html"]
        for strIndividualsHtmlFileExtension in lstStrIndividualsHtmlFileExtension:
            strIndividualsHtmlFilePath = strIndividualsFolderPath + os.sep + strIndividualsId + strIndividualsHtmlFileExtension
            if not os.path.exists(strIndividualsHtmlFilePath):
                isIndividualsHtmlFileMissing = True
        if isIndividualsHtmlFileMissing:
            #delete remaining project html files
            for strIndividualsHtmlFileExtension in lstStrIndividualsHtmlFileExtension:
                strIndividualsHtmlFilePath = strIndividualsFolderPath + os.sep + strIndividualsId + strIndividualsHtmlFileExtension
                if os.path.exists(strIndividualsHtmlFilePath):
                    os.remove(strIndividualsHtmlFilePath)
            openTor() #open tor
            typeUrlOnTor(strUrlText=strIndividualsUrl)
            wait(0.5)
        else:
            continue #skip this url
        #check page not found
        if dicRegion["regUp"].exists(dicPng["page_not_found"]):
            continue #skip this url
        #wait load completed
        dicRegion["regLeft"].wait(dicPng["page_focus_profile"], 300)
        #save profile html
        saveCurrentPage(strFolderPath=strIndividualsFolderPath, strFilename=strIndividualsId + "_profile.html")
        #save campaigns html 
        strIndividualsCampaignsUrl = strIndividualsUrl + u"/campaigns"
        openTor()
        typeUrlOnTor(strUrlText=strIndividualsCampaignsUrl)
        wait(0.5)
        saveCurrentPage(strFolderPath=strIndividualsFolderPath, strFilename=strIndividualsId + "_campaigns.html")
    individualsUrlListFile.close()
#main entry point
if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        lstStrArgs = sys.argv
        if lstStrArgs[1] == "explore":
            downloadExplorePages()
        if lstStrArgs[1] == "category":
            downloadCategoryPages()
        if lstStrArgs[1] == "project": 
            #lstStrArgs[2] is target category arg
            downloadProjectPages(strTargetCategory=lstStrArgs[2])
        if lstStrArgs[1] == "individuals":
            #lstStrArgs[2] is target category arg
            downloadIndividualsPages(strTargetCategory=lstStrArgs[2])
        popup(u"spider action completed. ^.^y")
    except FindFailed, ff:
        print(str(ff))
        popup(u"spider cant find png error! >_<||")
    except Exception, ex:
        print(str(ex))
        popup(u"spider unknow error! >_<||")
    finally:
        exit()