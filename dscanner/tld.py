# coding: utf-8
import re
import urllib
import pickle
from bs4 import BeautifulSoup

# ICANN公式のnew gTLDの一覧ページ
ICANN_URL = "https://newgtlds.icann.org/en/program-status/delegated-strings"

# htmlを抽出する
def get_soup(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    return soup

 # ICANN公式からnew gTLDのリストを抜いてくる
 # むしろnew gTLDに絞ってチェックした方が良いのかもしれない（悪用率が高いため）
def get_new_gtld(url):
    new_gtld = []
    soup = get_soup(url)
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
            new_gtld.append(tld)
    return new_gtld

# http://data.iana.org/TLD/tlds-alpha-by-domain.txt よりTLDの一覧を入手できる
# すべてのTLDを対象
def get_all_tld(file_name):
    all_tld = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            all_tld.append(line[:-1].lower())
            line = f.readline()
    return all_tld[1:]

if __name__  == "__main__":
    new_gtld = get_new_gtld(ICANN_URL)
    all_tld = get_all_tld("./TLD.txt")
    target_tld = set(all_tld)|set(new_gtld) # チェック対象TLD（set型）
    # print(len(target_tld)) # 1552個のTLDが対象
