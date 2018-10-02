# coding: utf-8
import urllib
from bs4 import BeautifulSoup

SUFFIX_URL = "https://publicsuffix.org/list/public_suffix_list.dat"

# htmlを抽出する
def get_soup(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    return soup

# TLDのリストを作成する
def make_list():
    res = get_soup(SUFFIX_URL).text.split("\n")
    tmp = [suffix for suffix in res if suffix != ""]
    tld_list = [suffix if "*" not in suffix else suffix.split(".")[-1] for suffix in tmp if suffix[0] != "/"]

    return tld_list


# TLDを付け替える
def generate_domain(domain):
    tld_list = make_list()
    if "www." in domain:
        domain = domain.split(".")[1]
    else:
        domain = domain.split(".")[0]
    check_list = [domain + "." + tld for tld in tld_list]

    return check_list

if __name__  == "__main__":
    check_list = generate_domain("example.com")
    print(check_list)
