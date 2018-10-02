# Install
1. `git clone https://github.com/toshs/domain-scanner.git`
2. `python3 setup.py install` or `pip3 install -e ./`

# Usage
## Generate domains
`dscan <domainname>`

## Generate and check domains
`dscan <domainname> --http`
### Result
	{
	    "qr": [
	        {
	            "domain_name": "aoogle.com",
	            "http_status_code": 200
	        },
	        {
	            "domain_name": "boogle.com",
	            "http_status_code": -1
	        }
	    ],
	    "typo": [
	    	 { 
	    	 ...
	}
