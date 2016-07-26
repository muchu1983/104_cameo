# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import time
from selenium import webdriver

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
    
    #測試 firefox selenium
    def test_firefox_selenium(self):
        for i in range(100):
            time.sleep(5)
            driver = webdriver.Firefox()
            driver.get("https://www.kickstarter.com/")
            time.sleep(5)
            driver.quit()
            driver = None
    
    #測試 chrome selenium
    def test_chrome_selenium(self):
        chromedriver = ".\cameo_res\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver)
        driver.get("https://www.crowdcube.com/")
        source = driver.page_source
        #f = open("currency.html", "w+")
        #f.write(source.encode("utf-8"))
        #f.close()
        driver.quit()
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


