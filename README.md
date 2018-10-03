# Install

1. `git clone https://github.com/toshs/domain-scanner.git`
2. `python3 setup.py install` or `pip3 install -e ./`

# Usage
## Generate domains
`dscan <domainname>`

## Generate and check domains with GET request
`dscan <domainname> --http`
### Result
	{
	    "qr": [
	        {
	            "domain_name": "aoogle.com",
	            "http_status_code": 200
	        },
			  ...
	    ],
	    "typo": [
	    	 { 
	    	 ...
	    	 }
	    ]
	}
## Generate and check domains with Virus Total
`dscan <domainname> --http --virustotal <here VirusTotal API key>`  
VERY SLOW.  
### Result

	{
	    "qr": [
	        {
	            "domain_name": "aoogle.com",
	            "http_status_code": -1,
	            "virus_total": {
	                "Safety score": 70,
	                "Adult content": "no",
	                "Verdict": "unsure"
	            }
	        }
	    ],
	    "suffix": [
	        {
	            "domain_name": "google.ac",
	            "http_status_code": 200,
	            "virus_total": {
	                "Safety score": 100,
	                "Adult content": "no",
	                "Verdict": "safe"
	            }
	        }
	    ]
	}

## Generate and check domains with Google Safe Browsing
`dscan <domainname> --http --safe_site <here Google Safe Browsing API key>`
### Result
Empty `site_threat` means safe.  

	{
	    "qr": [
	        {
	            "domain_name": "aoogle.com",
	            "http_status_code": 200,
	            "site_threat": []
	        }
	    ],
	    "suffix": [
	        {
	            "domain_name": "google.ac",
	            "http_status_code": 200,
	            "site_threat": []
	        }
	    ]
	}

