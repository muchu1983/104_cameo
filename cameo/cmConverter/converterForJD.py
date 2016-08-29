# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import re
import dateparser
from crawlermaster.utility import Utility

class ConverterForJdIntroPage:
    
    #建構子
    def __init__(self):
        self.cmUtility = Utility()
    
    def convert(self, strHtmlFilePath=None, dicRawData=None):
        logging.info("convert %s"%strHtmlFilePath)
        try:
            pass
        except Exception as e:
            logging.warning(str(e))
            logging.warning("parse failed skip: %s"%strHtmlFilePath)
        
    def flushConvertedDataToJsonFile(self, strJsonFilePath=None):
        pass
        