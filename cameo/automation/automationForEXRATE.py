# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from cameo_api import flaskrunner
"""
EXRATE 自動化 更新匯率
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    try:
        flaskrunner.start_flask_server()
        cameoUtility.sendEmail(
            strSubject="SUCCESS!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg="",
            lstStrTarget=dicSettings["lstStrMail"]
        )
    except Exception as e:
        logging.warning("automation for EXRATE fail: %s"%str(e))
        cameoUtility.sendEmail(
            strSubject="Failed!",
            strFrom=dicSettings["strMachine"],
            strTo="me",
            strMsg=str(e),
            lstStrTarget=dicSettings["lstStrMail"]
        )
        
if __name__ == "__main__":
    entry_point()