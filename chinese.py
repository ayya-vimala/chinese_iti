# -*- coding: utf-8 -*-
""" 

"""

import re
import os
import json


class HeadingRoot:
    """docstring for HeadingRoot"""
    def __init__(self, textname, textwriter, textsub):
        self.textname = textname
        self.textwriter = textwriter
        self.textsub = textsub

def addHeader(counter, heading):

    root_list = {}
    reference_list = {}
    html_list = {}

    root_list["lzh-iti"+str(counter)+":0.1"] = heading.textname
    root_list["lzh-iti"+str(counter)+":0.2"] = heading.textsub
    root_list["lzh-iti"+str(counter)+":0.3"] = "("+str(counter)+")"
    root_list["lzh-iti"+str(counter)+":0.4"] = heading.textwriter
    reference_list["lzh-iti"+str(counter)+":0.1"] = "t17.0765"

    html_list["lzh-iti"+str(counter)+":0.1"] = "<article id='lzh-iti"+str(counter)+"'><header><ul><li class='division'>{}</li>"
    html_list["lzh-iti"+str(counter)+":0.2"] = "<li class='subdivision'>{}</li></ul>"
    html_list["lzh-iti"+str(counter)+":0.3"] = "<h1 class='sutta-title'>{}</h1></header>"
    html_list["lzh-iti"+str(counter)+":0.4"] = "<li class='subheading'>{}</li>"

    return root_list, reference_list, html_list


base_dir = os.environ['HOME']+'/chinese_iti/cbeta_json_code/'
outputroot_dir = os.environ['HOME']+'/chinese_iti/root/'
outputreference_dir = os.environ['HOME']+'/chinese_iti/reference/'
outputhtml_dir = os.environ['HOME']+'/chinese_iti/html/'

parcounter = 1
secparcounter = 1
filecounter = 1
counter = 1

while filecounter < 2:
    print("0765_00"+str(filecounter)+'.json')
    fileIn = open(base_dir+"0765_00"+str(filecounter)+'.json','r', encoding='utf8').read()
    jsonobject = json.loads(fileIn)
    headingnrs = [jsonobject[0]["segmentnr"], jsonobject[1]["segmentnr"], jsonobject[2]["segmentnr"]]
    heading=HeadingRoot(jsonobject[0]["original"], jsonobject[1]["original"], jsonobject[2]["original"])

    for item in jsonobject:
        if item["original"] == "吾從世尊聞如是語：" or item["original"] == "復從世尊聞如是語：" or item["segmentnr"] == "t0699b13":
            if 'fileOut' in locals():
                if item["segmentnr"] == "t0699b13":
                    root_list["lzh-iti"+str(counter)+":"+str(parcounter)+'.'+str(secparcounter)] = item["original"]
                    reference_list["lzh-iti"+str(counter)+":"+str(parcounter)+'.'+str(secparcounter)] = item["segmentnr"]
                    html_list["lzh-iti"+str(counter)+":"+str(parcounter)+'.'+str(secparcounter)] = item["code_begin"]+"{}"+item["code_end"]
                fileOut.write(json.dumps(root_list, ensure_ascii=False, indent=2))
                fileOutReference.write(json.dumps(reference_list, ensure_ascii=False, indent=2))
                fileOuthtml.write(json.dumps(html_list, ensure_ascii=False, indent=2))
                counter += 1

            print(counter)


            root_list, reference_list, html_list = addHeader(counter, heading)

            root_list["lzh-iti"+str(counter)+":1.0"] = item["original"]
            reference_list["lzh-iti"+str(counter)+":1.0"] = item["segmentnr"]
            html_list["lzh-iti"+str(counter)+":1.0"] = item["code_begin"]+"{}"+item["code_end"]

            fileOut = open(outputroot_dir+'lzh-iti'+str(counter)+'_root-lzh-sct.json','w', encoding='utf8')
            fileOutReference = open(outputreference_dir+'lzh-iti'+str(counter)+'_reference.json','w', encoding='utf8')
            fileOuthtml = open(outputhtml_dir+'lzh-iti'+str(counter)+'_html.json','w', encoding='utf8')

            parcounter = 1
            secparcounter = 1

        else:
            if item["segmentnr"] not in headingnrs:
                if "<p>" in item["code_begin"]:
                    parcounter += 1
                    secparcounter = 0
                root_list["lzh-iti"+str(counter)+":"+str(parcounter)+'.'+str(secparcounter)] = item["original"]
                html_list["lzh-iti"+str(counter)+":"+str(parcounter)+'.'+str(secparcounter)] = item["code_begin"]+"{}"+item["code_end"]
                if not item["segmentnr"] in reference_list.values():
                    reference_list["lzh-iti"+str(counter)+":"+str(parcounter)+'.'+str(secparcounter)] = item["segmentnr"]
                secparcounter += 1
    filecounter += 1

            