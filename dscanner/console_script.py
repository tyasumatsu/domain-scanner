import sys
import argparse

# 単体で実行するとき用
#import qr
#import suffix
#import bit
#import typo
#import homo
#import combo

# 本番用
from . import qr
from . import suffix
from . import bit
from . import typo
#from . import homo
#from . import combo

import urllib.request
import urllib.error
import json
import socket 
from bs4 import BeautifulSoup
import socket
import urllib
from urllib.request import urlopen
from gglsbl import SafeBrowsingList
import time

def fetch_pdns_domain_info(domain_name, apikey):
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'
    parameters = {'domain': domain_name, 'apikey': apikey}
    response = urlopen('%s?%s' % (url, urllib.parse.urlencode(parameters))).read()

    response_dict = json.loads(response)
    return response_dict

def main():
    p = argparse.ArgumentParser()
    p.add_argument("domain_name")
    p.add_argument('-g', '--http', action="store_true", help="Get http response by each candidate domains")
    p.add_argument('--safe_site', default="", help="Get google safe sites tool information. must be followed by api key ")
    p.add_argument('--virustotal', default="", help="Get google safe sites tool information. must be followed by api key. VERY SLOW ")
    args = p.parse_args()

    # initialization ... いるの？
    # if args.safe_site:
    #     sbl = SafeBrowsingList('dummy')
    #     sbl.update_hash_prefix_cache()

    # URL候補を取得
    domains_dict = {}
    # TODO: 練習用にリストの長さを制限しているが、本番のときは制限をなくす
    domains_dict["qr"]     = qr.near_urls(args.domain_name)[:1]
    domains_dict["suffix"] = suffix.generate_domain(args.domain_name)[:1]
    domains_dict["bit"]   = bit.near_urls(args.domain_name)[:1]
    domains_dict["typo"]  = typo.near_urls(args.domain_name)[:1]
    #domains_dict["homo"]   = homo.near_urls(domain)
    #domains_dict["combo"]  = combo.near_urls(domain)
    
    result_dict = {}
    for domain_type_name, domain_list in domains_dict.items():
        domain_info_list = []
        for domain_name in domain_list:
            domain_info_dict = {}
            domain_info_dict["domain_name"] = domain_name
            
            # httpレスポンス情報を付加する
            if args.http:
                # TODO: httpステータスコードの取得をもっとマシなものにする
                # https://stackoverflow.com/questions/1726402/in-python-how-do-i-use-urllib-to-see-if-a-website-is-404-or-200
                http_status_code = 0
                try:
                    urllib.request.urlopen("http://" + domain_name, timeout=0.5)
                except urllib.error.HTTPError as e:
                    http_status_code = e.code
                # connection refusedなどになった場合。後でもっとうまく変えたほうがよいかも
                except urllib.error.URLError as e:
                    http_status_code = -1
                except socket.timeout:
                    http_status_code = -1
                except ConnectionResetError:
                    http_status_code = -1
                else:
                    # エラーにならないのは本当に200だけか...?301とかもあるかもしれないがとりあえず200
                    http_status_code = 200
                domain_info_dict["http_status_code"] = http_status_code
            
            if len(args.safe_site)>0:
                api_key_gsb = args.safe_site
                sbl = SafeBrowsingList(api_key_gsb)
                threat_list = sbl.lookup_url(domain_name)
                if threat_list == None:
                    domain_info_dict["site_threat"] = []
                else: 
                    domain_info_dict["site_threat"] = threat_list

            if len(args.virustotal)>0:
                api_key_vt = args.virustotal

                # TODO:関数とかに後でする
                interval_seconds_virustotal = 60/4
                retry_max_time = 2
                retry_sleep_seconds_virustotal = 1
                for _ in range(retry_max_time):
                    try:
                        info_virustotal = fetch_pdns_domain_info(domain_name, api_key_vt)
                    except:
                        # virustotalがrate limitなどなどで取得に失敗した場合はすこし待つ
                        time.sleep(retry_sleep_seconds_virustotal)
                    else:
                        domain_info_dict["virus_total"] = info_virustotal["Webutation domain info"]
                        # virustotalのrate limitにかからないように60/4 = 15秒ほど寝る
                        # 制限は1分間に4クエリなのだから、1クエリにつき15秒まつのではなく、4クエリ投げたら1分待つ方が正当だが面倒なのでこうした
                        time.sleep(interval_seconds_virustotal)
                        break

            # 追加例：
            # geoip情報を付加する
            # if args.geoip:
            #     domain_info_dict["geoip"] = country

            domain_info_list.append(domain_info_dict)
        result_dict[domain_type_name] = domain_info_list

    print(json.dumps(result_dict, indent=4, separators=(',', ': ')) )

if __name__ == '__main__':
    main()
