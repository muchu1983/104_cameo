# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from cameo.cameoshell import CameoShell
"""
程式進入點 (main)
"""
#進入點
def entry_point():
    shell = CameoShell()
    shell.openShell()

if __name__ == '__main__':
    entry_point()