# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from cameo.utility import Utility
from bennu.filesystemutility import FileSystemUtility
"""
CRUNCHBASE html 檔名重新命名
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    cameoUtility = Utility()
    filesysUtility = FileSystemUtility()
    strSettingsJsonFilePath = filesysUtility.getPackageResourcePath(strPackageName="cameo.automation", strResourceName="automationForRENAME_settings.json")
    dicSettings = cameoUtility.readObjectFromJsonFile(strJsonFilePath=strSettingsJsonFilePath)
    try:
        strSourceFolder = u"cameo_res\\source_html\\CRUNCHBASE\\other_organization"
        strTargetFolder = u"cameo_res\\source_html\\CRUNCHBASE\\organization"
        cameoUtility.crunchbaseOrganizationHtmlFileRename(strSourceFolder=strSourceFolder, strTargetFolder=strTargetFolder)
        logging.info("automation for RENAME SUCCESS")
        cameoUtility.sendEmail(
            strSubject="SUCCESS!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg="",
            lstStrTarget=dicSettings["lstStrMail"]
        )
    except Exception as e:
        logging.warning("automation for RENAME fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
        
if __name__ == "__main__":
    entry_point()