# -*- coding: utf-8 -*-
""" 

"""

import re
import os
import json


class SegmentObject:
    """docstring for HeadingRoot"""
    def __init__(self, segmentnr, original, code_begin, code_end):
        self.object = {"segmentnr": segmentnr, "original": original, "code_begin": code_begin, "code_end": code_end}


base_dir = os.environ['HOME']+'/chinese_iti/cbeta_json/'
output_dir = os.environ['HOME']+'/chinese_iti/cbeta_json_code/'

filecounter = 1
startblock = False
new_json = []

while filecounter < 2:
    print("0765_00"+str(filecounter)+'.json')
    fileIn = open(base_dir+"0765_00"+str(filecounter)+'.json','r', encoding='utf8').read()
    jsonobject = json.loads(fileIn)
    fileOut = open(output_dir+"0765_00"+str(filecounter)+'.json','w', encoding='utf8')

    code_begin = ""
    code_end = ""

    for item in jsonobject:
        if item["original"].endswith("¶") and startblock == False:
            code_end = "</p>"
            new_item = SegmentObject(item["segmentnr"],item["original"].strip("¶"),code_begin,code_end).object
            code_begin="<p>"
            code_end = ""
        elif item["original"] == "吾從世尊聞如是語：" or item["original"] == "復從世尊聞如是語：":
            code_begin="<p>"
            new_item = SegmentObject(item["segmentnr"],item["original"],code_begin,code_end).object
            code_begin = ""
            code_end = ""
        elif item["original"].startswith("&"):
            code_begin = "<blockquote class='gatha'><p><span class='verse-line'>"
            new_item = SegmentObject(item["segmentnr"],item["original"].strip("&"),code_begin,code_end).object
            code_begin = ""
            code_end = "</span>"
            startblock = True
        elif item["original"].endswith("@"):
            code_end = "</span></p></blockquote>"
            new_item = SegmentObject(item["segmentnr"],item["original"].strip("@"),code_begin,code_end).object
            code_begin = "<p>"
            code_end = ""
            startblock = False
        elif startblock == True:
            if item["original"].endswith("¶"):
                code_end = "</span></p>"
                new_item = SegmentObject(item["segmentnr"],item["original"].strip("¶"),code_begin,code_end).object
                code_begin="<p><span class='verse-line'>"
                code_end = ""
            else:
                if code_end:
                    new_item = SegmentObject(item["segmentnr"],item["original"],code_begin,code_end).object
                    code_end = ""
                    code_begin = "<span class='verse-line'>"
                else:
                    new_item = SegmentObject(item["segmentnr"],item["original"],code_begin,code_end).object
                    code_end = "</span>"
                    code_begin = ""
        else:
            new_item = SegmentObject(item["segmentnr"],item["original"],code_begin,code_end).object
            code_begin = ""
            code_end = ""

        new_json.append(new_item)

    fileOut.write(json.dumps(new_json, ensure_ascii=False, indent=2))

    filecounter += 1

            