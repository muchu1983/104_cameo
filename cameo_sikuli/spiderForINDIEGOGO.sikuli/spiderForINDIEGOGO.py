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
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
dicPng = {"chrome_close":Pattern("chrome_close.png").targetOffset(-24,-1),
          "chrome_home":"chrome_home.png",
          "chrome_stop": "chrome_stop.png",
          "chrome_reload":"chrome_reload.png",
          "chrome_download_finished":"chrome_download_finished.png",
          "page_end_about":"page_end_about.png",
          "page_end_camp":"page_end_camp.png",
          "page_cate_more":"page_cate_more.png",
          "page_ucb_more":"page_ucb_more.png",
          "papge_new_style_check":"page_new_style_check.png",
          "page_blur_story":"page_blur_story.png",
          "page_focus_story":"page_focus_story.png",
          "page_blur_updates":"page_blur_updates.png",
          "page_focus_updates":"page_focus_updates.png",
          "page_blur_comments":"page_blur_comments.png",
          "page_focus_comments":"page_focus_comments.png",
          "page_blur_backers":"page_blur_backers.png",
          "page_focus_backers":"page_focus_backers.png",
          "page_blur_gallery":"page_blur_gallery.png",
          "page_focus_gallery":"page_focus_gallery.png",
          "page_focus_profile":"page_focus_profile.png",
          "papge_story_details":"papge_story_details.png",
          "page_details_about":"page_details_about.png",
          "page_details_close":"page_details_close.png",
          "page_explore":"page_explore.png",
          "page_not_found":"page_not_found.png",
          "page_not_right":"page_not_right.png",
          "page_your_interruption":"page_your_interruption.png",
          "page_currently_updated":"currently_updated.png",
          "os_foldername_bar":Pattern("os_foldername_bar.png").targetOffset(10,0),
          "os_filename_bar":Pattern("os_filename_bar.png").targetOffset(36,0),
          "os_right_save_as":"os_right_save_as.png",
          "os_save_btn":"os_save_btn.png",
          }
sysClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
strBaseResFolderPath = r"C:\Users\Administrator\Desktop\pyWorkspace\CAMEO_git_code\cameo_res"
#open chrome
def openChrome():
    #close prev chrome
    if exists(dicPng["chrome_close"]):
        click(dicPng["chrome_close"])
    wait(2)
    #re-open new chrome
    App.open("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe --incognito")
    wait(2)#wait to running
    wait(dicPng["chrome_home"], 300)
    click(dicPng["chrome_home"])
    waitVanish(dicPng["chrome_stop"], 300)
    wait(dicPng["chrome_reload"], 300)
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
    wait(dicPng["page_end_about"], 300)
# open all project
def unfoldCategoryPage():
    rollToPageEnd()
    for uptime in range(6):
        type(Key.UP)
    wait(dicPng["page_end_camp"], 300)
    while(exists(dicPng["page_cate_more"])):
        click(dicPng["page_cate_more"])
        waitVanish(dicPng["page_end_camp"], 300)
        wait(5)
        rollToPageEnd()
        for uptime in range(6):
            type(Key.UP)
            wait(0.5)
        wait(dicPng["page_end_camp"], 300)
#unfold (updates comments backers) showmore
def unfoldUCBShowmore():
    while(not exists(dicPng["page_end_about"])):
        type(Key.PAGE_DOWN)
        wait(0.5)
        if exists(dicPng["page_ucb_more"]):
            click(dicPng["page_ucb_more"])
            waitVanish(dicPng["page_ucb_more"], 300)
            wait(2)
    type(Key.HOME)
    wait(dicPng["page_blur_story"], 300)
#pause if interruption page found
def checkAndPauseForYourInterruption():
    if exists(dicPng["page_your_interruption"]):
        popup(u"spider paused! （╯‵□′）╯︵┴─┴")
#type url on chrome
def typeUrlOnChrome(strUrlText=None):
    while True:
        type("l", KeyModifier.CTRL)
        wait(0.5)
        delOriginText()
        pasteClipboardText(strText=strUrlText)
        wait(0.5)
        type(Key.ENTER)
        wait(0.5)
        waitVanish(dicPng["chrome_stop"], 300)
        wait(dicPng["chrome_reload"], 300)
        #check page "something not right" show?
        if exists(dicPng["page_not_right"]):
            #restart chrome and run typeUrlOnChrome again
            openChrome()
        else:
            #ok everything is right, go out while loop
            break
# go to explore page
def goExplorePage():
    openChrome()
    typeUrlOnChrome(strUrlText="https://www.indiegogo.com/explore")
    wait(dicPng["page_explore"], 300)
    waitVanish(dicPng["chrome_stop"], 300)
    wait(dicPng["chrome_reload"], 300)
#choose folder at save progress
def typeFolderPath(strFolderPath=None):
    wait(dicPng["os_foldername_bar"], 300)
    click(dicPng["os_foldername_bar"])
    wait(0.5)
    delOriginText()
    pasteClipboardText(strText=strFolderPath)
    wait(0.5)
    type(Key.ENTER)
    wait(0.5)
#rightclick on image to save current page
def rightClickSaveCurrentPage(onImage=None, strFolderPath=None, strFilename=None):
    waitVanish(dicPng["chrome_stop"], 300)
    wait(dicPng["chrome_reload"], 300)
    checkAndPauseForYourInterruption()
    rightClick(onImage)
    wait(dicPng["os_right_save_as"], 300)
    click(dicPng["os_right_save_as"])
    wait(dicPng["os_save_btn"], 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    click(dicPng["os_filename_bar"])
    wait(0.5)
    delOriginText()
    wait(0.5)
    pasteClipboardText(strText=strFilename)
    wait(0.5)
    click(dicPng["os_save_btn"])
    wait(0.5)
    wait(dicPng["chrome_download_finished"], 600)#wait save complete
#ask chrome save current page
def saveCurrentPage(strFolderPath=None, strFilename="default.html"):
    waitVanish(dicPng["chrome_stop"], 300)
    wait(dicPng["chrome_reload"], 300)
    checkAndPauseForYourInterruption()
    type("s", KeyModifier.CTRL)
    wait(dicPng["os_save_btn"], 300)
    if strFolderPath != None:
        typeFolderPath(strFolderPath)
    click(dicPng["os_filename_bar"])
    wait(0.5)
    delOriginText()
    wait(0.5)
    pasteClipboardText(strText=strFilename)
    wait(0.5)
    click(dicPng["os_save_btn"])
    wait(0.5)
    wait(dicPng["chrome_download_finished"], 600)#wait save complete
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
        strCategoryName = r"" + re.search("^https://www.indiegogo.com/explore/(.*)$" ,strCategoryUrl).group(1)
        strCategoryFolderPath = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s"%(strCategoryName)
        if not os.path.exists(strCategoryFolderPath):
            os.mkdir(strCategoryFolderPath) #mkdir category
        strCategoryFilePath = strCategoryFolderPath + r"\category.html"
        if not os.path.exists(strCategoryFilePath):#check category.html
            openChrome()
            typeUrlOnChrome(strUrlText=strCategoryUrl)
            waitVanish(dicPng["chrome_stop"], 300)
            wait(dicPng["chrome_reload"], 300)
            unfoldCategoryPage()
            saveCurrentPage(strFolderPath=strCategoryFolderPath, strFilename="category.html")
    catUrlListFile.close()
#download project pages
def downloadProjectPages(strTargetCategory=None):
    strProjUrlListFilePathTemplate = strBaseResFolderPath + r"\parsed_result\INDIEGOGO\%s\project_url_list.txt"
    strProjectsFolderPathTemplate = strBaseResFolderPath + r"\source_html\INDIEGOGO\%s\projects"   
    strProjectsFolderPath = strProjectsFolderPathTemplate % (strTargetCategory)
    if not os.path.exists(strProjectsFolderPath):
        os.mkdir(strProjectsFolderPath)#mkdir source_html/INDIEGOGO/Category/pojects/
    strProjUrlListFilePath = strProjUrlListFilePathTemplate % (strTargetCategory)
    projUrlListFile = open(strProjUrlListFilePath, "r") 
    for strProjUrl in projUrlListFile:
        strProjName = re.search("^https://www.indiegogo.com/projects/(.*)/.{4}$", strProjUrl).group(1)
        #check html file exists
        isProjHtmlFileMissing = False
        strProjDetailsFilename = strProjName+"_details.html"
        strProjDetailsFilePath = strProjectsFolderPath + "\\" + strProjDetailsFilename
        if not os.path.exists(strProjDetailsFilePath):#check detail.html
            isProjHtmlFileMissing = True
        strProjStoryFilename = strProjName+"_story.html"
        strProjStroyFilePath = strProjectsFolderPath + "\\" + strProjStoryFilename
        if not os.path.exists(strProjStroyFilePath):#check story.html
            isProjHtmlFileMissing = True
        strProjUpdatesFilename = strProjName+"_updates.html"
        strProjUpdatesFilePath = strProjectsFolderPath + "\\" + strProjUpdatesFilename
        if not os.path.exists(strProjUpdatesFilePath):#check updates.html
            isProjHtmlFileMissing = True
        strProjCommentsFilename = strProjName+"_comments.html"
        strProjCommentsFilePath = strProjectsFolderPath + "\\" + strProjCommentsFilename
        if not os.path.exists(strProjCommentsFilePath):#check comments.html
            isProjHtmlFileMissing = True
        strProjBackersFilename = strProjName+"_backers.html"
        strProjBackersFilePath = strProjectsFolderPath + "\\" + strProjBackersFilename
        if not os.path.exists(strProjBackersFilePath):#check backers.html
            isProjHtmlFileMissing = True
        #open chrome 
        if isProjHtmlFileMissing:
            openChrome()
            typeUrlOnChrome(strUrlText=strProjUrl)
            wait(0.5)
            #check page "style" or "something not right" show?
            while(exists(dicPng["papge_new_style_check"]) or exists(dicPng["page_not_right"])):
                openChrome() #reopen chrome for load standard style
                typeUrlOnChrome(strUrlText=strProjUrl)
                wait(0.5)
            if exists(dicPng["page_currently_updated"]):
                #page is currently updated, skip this url
                continue
        else:
            continue #skip this url
        #check page not found
        if exists(dicPng["page_not_found"]):
            continue #skip this url
        #wait load completed
        wait(dicPng["page_focus_story"], 300)
        wait(0.5)
        if not os.path.exists(strProjDetailsFilePath):#check detail.html
            while(not exists(dicPng["papge_story_details"])):
                type(Key.PAGE_DOWN)
                wait(0.5)
            click(dicPng["papge_story_details"])
            wait(dicPng["page_details_about"], 300)
            #save see more details
            rightClickSaveCurrentPage(onImage=dicPng["page_details_about"], strFolderPath=strProjectsFolderPath, strFilename=strProjDetailsFilename)
            #close details
            click(dicPng["page_details_close"])
            wait(dicPng["papge_story_details"], 300)
            type(Key.HOME)       
            wait(dicPng["page_focus_story"], 300)
        if not os.path.exists(strProjStroyFilePath):#check story.html
            #save story
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjStoryFilename)
        if not os.path.exists(strProjUpdatesFilePath):#check updates.html
            #save updates
            wait(dicPng["page_blur_updates"], 300)
            click(dicPng["page_blur_updates"])
            wait(dicPng["page_focus_updates"], 300)
            #unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjUpdatesFilename)
        if not os.path.exists(strProjCommentsFilePath):#check comments.html
            #save comments
            wait(dicPng["page_blur_comments"], 300)
            click(dicPng["page_blur_comments"])
            wait(dicPng["page_focus_comments"], 300)
            #unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjCommentsFilename)
        if not os.path.exists(strProjBackersFilePath):#check backers.html
            #save backers
            wait(dicPng["page_blur_backers"], 300)
            click(dicPng["page_blur_backers"])
            wait(dicPng["page_focus_backers"], 300)
            #unfoldUCBShowmore()
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjBackersFilename)
        #gallery may not exists
        strProjGalleryFilename = strProjName+"_gallery.html"
        strProjGalleryFilePath = strProjectsFolderPath + "\\" + strProjGalleryFilename            
        if (not os.path.exists(strProjGalleryFilePath)) and exists(dicPng["page_blur_gallery"]):#check gallery.html
            #save gallery
            wait(dicPng["page_blur_gallery"], 300)
            click(dicPng["page_blur_gallery"])
            wait(dicPng["page_focus_gallery"], 300)
            saveCurrentPage(strFolderPath=strProjectsFolderPath, strFilename=strProjGalleryFilename)
    projUrlListFile.close()
#download individuals pages
def downloadIndividualsPages(strTargetCategory=None):
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
        strIndividualsProfileFilename = strIndividualsId+"_profile.html"
        strIndividualsProfileFilePath = strIndividualsFolderPath + "\\" + strIndividualsProfileFilename
        if not os.path.exists(strIndividualsProfileFilePath):#check profile.html
            isIndividualsHtmlFileMissing = True
        strIndividualsCampaignsFilename = strIndividualsId+"_campaigns.html"
        strIndividualsCampaignsFilePath = strIndividualsFolderPath + "\\" + strIndividualsCampaignsFilename
        if not os.path.exists(strIndividualsCampaignsFilePath):#check campaigns.html  
            isIndividualsHtmlFileMissing = True
        #open chrome
        if isIndividualsHtmlFileMissing:
            openChrome()
            typeUrlOnChrome(strUrlText=strIndividualsUrl)
            wait(0.5)
        else:
            continue #skip this url
        #check page not found
        if exists(dicPng["page_not_found"]):
            continue #skip this url
        #wait load completed
        wait(dicPng["page_focus_profile"], 300)
        if not os.path.exists(strIndividualsProfileFilePath):#check profile.html
            saveCurrentPage(strFolderPath=strIndividualsFolderPath, strFilename=strIndividualsProfileFilename)
        if not os.path.exists(strIndividualsCampaignsFilePath):#check campaigns.html
            strIndividualsCampaignsUrl = strIndividualsUrl + u"/campaigns"
            openChrome()
            typeUrlOnChrome(strUrlText=strIndividualsCampaignsUrl)
            wait(0.5)
            saveCurrentPage(strFolderPath=strIndividualsFolderPath, strFilename=strIndividualsCampaignsFilename)
    individualsUrlListFile.close()
#main entry point
if __name__ == "__main__":
    try:
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
        popup(u"spider error! >_<||")
    finally:
        exit()