import qrcode
from dscanner.constants import ALPHABETS

def make_word(string):
    qr = qrcode.QRCode(version=2)
    qr.add_data(string)
    qr.make()
    return qr.data_cache

def diff_word(src, dst):
    count = 0
    for s, d in zip(src, dst):
        if s != d:
            count += 1

    return count

def hamming(string, dist=1):
    words = []
    for i, c in enumerate(string):
        for a in ALPHABETS:
            if c != a:
                words.append(string[:i]+a+string[i+1:])

    return words

def near_urls(domain):
    src_word = make_word(domain)

    domain = domain.split('.')
    ham_words = hamming(domain[-2])

    cand = []
    for w in ham_words:
        domain[-2] = w
        cand_domain = '.'.join(domain)
        dst_word = make_word(cand_domain)
        distance = diff_word(src_word, dst_word)
        if distance == 17:
            cand.append(cand_domain)
            
    return cand
    

if __name__ == '__main__':
    domain = "http://www.example.com"
    print(near_urls(domain))
