# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from cameo.mongoDbRepairman import MongoDbRepairman
"""
MongoDB 自動化 修復
"""
#進入點
def entry_point():
    logging.basicConfig(level=logging.INFO)
    repairman = MongoDbRepairman()
    try:
        repairman.makeViewStartupAndInvestment()
        repairman.makeViewStartupAndSeries()
        #repairman.replaceNullStrCurrencyToEmptyString()
        #repairman.removeModelStartupInvestorAndModelRewardPersonUnnecessaryData()
        #repairman.makeTagFieldOnModelFundProject()
        #repairman.makeTagFieldOnModelStartup()
    except Exception as e:
        logging.warning("automation for MongoDbRepairman fail: %s"%str(e))
        
if __name__ == "__main__":
    entry_point()