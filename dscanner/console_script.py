import sys
import argparse
#from . import qr
import qr
#from . import bit
#from . import typo
#from . import homo
#from . import combo

#import suffix

import urllib.request
import urllib.error
import json
import socket 

def main():
    p = argparse.ArgumentParser()
    p.add_argument("domain_name")
    p.add_argument('-g', '--http', action="store_true", help="Get http response by each candidate domains")
    args = p.parse_args()

    # URL候補を取得
    domains_dict = {}
    domains_dict["qr"] = qr.near_urls(args.domain_name)[:15]
    #domains_dict["suffix"] = suffix.main
    #domains_dict["bit"] = bit.near_urls(args.domain_name)
    #domains_dict["typo"] = typo.near_urls(args.domain_name)
    #result_dict["homo"] = homo.near_urls(domain)
    #result_dict["combo"] = combo.near_urls(domain)
    
    result_dict = {}
    for domain_type_name, domain_list in domains_dict.items():
        domain_info_list = []
        for domain_name in domain_list:
            domain_info_dict = {}
            domain_info_dict["domain_name"] = domain_name
            # httpレスポンス情報を付加する
            if args.http:
                http_status_code = 0
                # https://stackoverflow.com/questions/1726402/in-python-how-do-i-use-urllib-to-see-if-a-website-is-404-or-200
                try:
                    _ = urllib.request.urlopen("http://" + domain_name, timeout=0.5)
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
                    # ほんとに200だけか？
                    http_status_code = 200
                domain_info_dict["http_status_code"] = http_status_code
            # 例：
            # geoip情報を付加する
            # if args.geoip:
            #     domain_info_dict["geoip"] = country
            domain_info_list.append(domain_info_dict)
        result_dict[domain_type_name] = domain_info_list

    print(json.dumps(result_dict, indent=4, separators=(',', ': ')) )

                
main()