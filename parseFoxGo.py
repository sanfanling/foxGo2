#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: parseFoxGo.py 

import os, sys, re
import requests



class parseFoxGo:
    
    def __init__(self):
        pass
        
    def getCatalog(self):
        baseUrl = "https://www.foxwq.com/qipu/index/p/"
        source = []
        page = ""
        for i in range(1, 5):
            url = baseUrl + "{}.html".format(i)
            res= requests.get(url)
            res.encoding = "utf8"
            page += res.text
            res.close()
        s = re.findall("href=\"/qipu/newlist/id/.*?</tr>", page, re.S)
        for j in s:
            key = re.search("\d{16}?", j)[0]
            game = re.search("<h4>.*?</h4>", j)[0].replace("<h4>", "").replace("</h4>", "").replace("&nbsp;", "")
            date = re.search("\d{4}-\d{2}-\d{2}", j)[0]
            
            source.append((game, date, key))
        return source

    def getSgf(self, key):
        url = "https://www.foxwq.com/qipu/newlist/id/{}.html".format(key)
        res = requests.get(url)
        res.encoding = "utf8"
        page = res.text
        res.close()
        sgf = re.search("\(;.*?</div>", page, re.S)[0]
        sgf = sgf.replace("</div>", "").strip()
        return sgf
        
