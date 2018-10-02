import tldextract
# 単体で実行した時用の書き方?
#from constants import ALPHABETS
# 単体で実行した時は明示的なrelative importが上手くうごかない...?　
from .constants import ALPHABETS

import itertools

# pythonはUTF-8で文字を扱うが、URLはネットワーク機器ではIDN(国際化ドメイン名)でもピュニコードとか使って結局asciiの範囲で扱われる？のかよくわからないがとりあえずasciiに合わせて8bit
# とりあえず1bitだけ反転。複数bit反転が必要なら後で直します
def bit_invert(chars, num_bit_per_char=8):
    cand = []
    for ind_char in range(len(chars)):
        target_char_code = ord(chars[ind_char])
        for ind_bit_inversed in range(num_bit_per_char):
            mask = 0b1 << ind_bit_inversed
            target_char_code_inversed = target_char_code ^ mask
            
            # URLとしてinvalidな文字の場合、弾く
            if not chr(target_char_code_inversed) in ALPHABETS:
                continue

            chars_bit_inversed = chars[:ind_char] + chr(target_char_code_inversed) + chars[ind_char+1:]
            
            cand.append(chars_bit_inversed)
    return cand
    
def near_urls(FQDN):
    extractResult = tldextract.extract(FQDN)
    # とりあえずTLDはビット反転させない
    # "http;//www.example.com"でいう、wwwとexampleのみ対象とする
    domain = extractResult.domain
    subdomain = extractResult.subdomain

    cand_domains_inverted = bit_invert(domain)
    cand_subdomains_inverted = bit_invert(subdomain)
   
    suffix = extractResult.suffix
    cand_FQDN = []
    # www.example.comでいうexampleの部分が1bit反転したもの
    for cand in cand_domains_inverted:
        cand_FQDN.append( '.'.join(part for part in [subdomain, cand, suffix] if part) )
        #cand_FQDN.append(subdomain +"."+ cand +"."+ suffix)
    # www.example.comでいうwwwの部分が1bit反転したもの
    for cand in cand_subdomains_inverted:
        cand_FQDN.append( '.'.join(part for part in [cand, domain, suffix] if part) )
        #cand_FQDN.append(cand +"." + domain +"."+ suffix)

    return cand_FQDN

if __name__ == '__main__':
    domain = "http://www.example.com"
    print(near_urls(domain))

    #実行結果例(URLスキームが削られているので必要なら後で直します)：
    #['www.examplg.com', 'www.exampla.com', 'www.examplm.com', 'ww7.example.com', 'ww7.example.com', ...]
