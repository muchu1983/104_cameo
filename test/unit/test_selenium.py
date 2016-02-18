# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from selenium import webdriver
import time
import io
import random
import os

"""
測試 Selenium
"""

class SeleniumTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 selenium
    def test_selenium(self):
        chromedriver = ".\cameo_res\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver)
        time.sleep(random.randint(5,10))
        driver.get("https://www.indiegogo.com/projects/help-hanako-the-elephant--2#/")
        time.sleep(15)
        #cate_hrefs = driver.find_element_by_css_selector(".ng-scope > a")
        source = driver.page_source.encode("utf-8")
        f = io.open("animals.html", "w+", encoding="utf-8")
        f.write(unicode(source))
        f.close()
        


#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


