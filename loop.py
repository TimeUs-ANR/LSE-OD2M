# -*- coding: utf-8 -*-

""" Will run XML2TXT's main.py on multiple files placed in a directory names 'input' and located in the current directory."""


import os
import subprocess

CWD = os.path.dirname(os.path.abspath(__file__))
document = os.listdir(os.path.join(CWD, "input"))
clear_doc = []
for doc in document:
    name, ext = doc.split(".")
    if ext == "xml":
        clear_doc.append("input/" + name + "." + ext)
for d in clear_doc:
    subprocess.call(["python3", "main.py", "-i", d])