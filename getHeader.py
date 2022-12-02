#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: getHeader.py

import sys, os, re
from urllib import request
from kojpNames import kojpNames


class getHeader:

    def __init__(self, name):
        if name in kojpNames:
            self.name = kojpNames[name]
        else:
            self.name = name
        self.fileName = name

    def get(self):
        return self.__checkHaveName(self.name)

    def __checkHaveName(self, name):
        if name == "-" or name == "":
            return None
        for i in range(1, 4):
            url = "http://sinago.com/info/china_player.asp?ntn={}".format(i)
            req = request.urlopen(url)
            page = req.read().decode("gbk")
            req.close()
            if name + "</a>" in page:
                k = re.search("goGamer.*?" + name, page)[0]
                index = int(re.search("\'.*?\'", k)[0].replace("\'", ""))
                return self.__checkHaveHeader(index)
        return None

    def __checkHaveHeader(self, index):
        url = "http://sinago.com/info/china_player_history.asp?gno={}&ggrade=39&ntn=1".format(index)
        req = request.urlopen(url)
        page = req.read().decode("gbk")
        req.close()
        p = re.findall("gsphoto.*?jpg", page)
        if len(p) == 0:
            return None
        else:
            return "http://sinago.com/" + p[0]





if __name__ == "__main__":

    name1 = "李相勋"
    name2 = "古力"
    p = getHeader(name1, name2)
    print(p.get())
