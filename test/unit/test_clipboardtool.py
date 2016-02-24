# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from cameo.clipboardtool import ClipboardTool

"""
測試 剪貼簿存取工具
"""

class ClipboardToolTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 access unicode text
    def test_accessUnicodetext(self):
        logging.info("ClipboardToolTest.test_accessUnicodetext")
        cbt = ClipboardTool()
        cbt.setUnicodeText(u"i-love-u")
        self.assertEquals(u"i-love-u", cbt.getUnicodeText())


#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


