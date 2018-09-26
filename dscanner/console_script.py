import sys

def main():
    domain = sys.argv[1]
    domain = domain.split('.')
    
    for i, d in enumerate(domain[::-1]):
        print(i+1, "th domain is", d)
