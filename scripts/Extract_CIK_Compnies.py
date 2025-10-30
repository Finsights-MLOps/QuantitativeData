import requests

user_agent = "Karthik Raja (University Project; karthikraja.ai.project@gmail.com)"

# Extracting company ticker and CIK
url = 'https://www.sec.gov/files/company_tickers.json'
headers = {'User-Agent': user_agent}

res = requests.get(url, headers=headers)
data = res.json()

# Convert JSON -> dict mapping ticker -> padded CIK
companies = {
    entry["ticker"]: str(entry["cik_str"]).zfill(10)
        for entry in list(data.values())[:2]
}

# Print first few for verification
print(companies)
