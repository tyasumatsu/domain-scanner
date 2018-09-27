# coding: utf-8
import re
import urllib
import pickle
from bs4 import BeautifulSoup

def get_soup(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    return soup

# ### ICANN公式のnew gTLDの一覧ページ
url = "https://newgtlds.icann.org/en/program-status/delegated-strings"
soup = get_soup(url)

NEW_TLD = []

for i, tld in enumerate(soup.find_all("td")):
    if i % 2 == 1:
        if not tld.find("span"):
            tld = str(tld.text)
        else:
            tld = str(tld.contents[1])
        if "xn--" in tld:
            tld = [i for i in tld.split(" ") if "xn--" in i][0]
            if "(" in tld:
                tld = tld[tld.find("(") + 1: tld.find(")")]
        if "xn―cg4bki" in tld: # ICANN公式がtypoしているという、、
            tld = "xn--cg4bki"
        tld = tld.lower()
        NEW_TLD.append(tld)


# ### pickleに保存
with open("new_gTLD.pickle", "wb") as f:
    pickle.dump(NEW_TLD, f)


# ### http://data.iana.org/TLD/tlds-alpha-by-domain.txt よりTLDの一覧を入手（基本的にはこれだけで良さそう？）
TLD = []
with open("./TLD.txt", "r") as f:
    line = f.readline()
    while line:
        TLD.append(line[:-1].lower())
        line = f.readline()
TLD = TLD[1:]
