import tldextract
# 単体で実行した時用の書き方?
from constants import ALPHABETS
# 単体で実行した時は明示的なrelative importが上手くうごかない...?　
#from .constants import ALPHABETS
import itertools


# pythonはUTF-8で文字を扱うが、URLはネットワーク機器ではIDN(国際化ドメイン名)でもピュニコードとか使って結局asciiの範囲で扱われる？のかよくわからないがとりあえずasciiに合わせて8bit
# とりあえず1bitだけ反転。複数bit反転が必要なら後で直します
def bit_invert(chars, num_bit_per_char=8):
    cand = []
    print(chars)
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
    # ビット反転したドメインとサブドメイン(言葉の使い方おかしいけど)の全組み合わせ
    perm = list(itertools.product(cand_subdomains_inverted, cand_domains_inverted))
    
    cand_FQDN = []
    suffix = extractResult.suffix
    for comb in perm:
        cand_FQDN.append(comb[0] +"."+ comb[1] +"."+ suffix)

    return cand_FQDN

if __name__ == '__main__':
    domain = "http://www.example.com"
    print(near_urls(domain))

    #実行結果例(URLスキームが削られているので必要なら後で直します)：
    #['ww7.examplg.com', 'ww7.exampla.com', 'ww7.examplm.com', 'ww7.examplu.com', 'ww7.examplE.com', ...]
