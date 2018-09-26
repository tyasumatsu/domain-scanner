import sys
from . import qr

def main():
    domain = sys.argv[1]

    print("searching urls have near codeword of QR...")
    print(qr.near_urls(domain))
