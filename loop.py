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
    subprocess.call(["python3", "xml2txt_0.2.py", "-i", d])