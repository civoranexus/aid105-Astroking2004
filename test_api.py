import requests
import json

# Test recommendations endpoint
payload = {
    'age': 25,
    'income': 300000,
    'state': 'karnataka',
    'needs': ['training']
}

print("Testing /recommendations endpoint...")
resp = requests.post('http://127.0.0.1:8001/recommendations', json=payload)
print(f'Status: {resp.status_code}')

if resp.status_code == 200:
    recs = resp.json()
    print(f'Recommendations returned: {len(recs)}')
    if recs:
        rec = recs[0]
        print(f'\nFirst recommendation:')
        print(f'  Name: {rec.get("name")}')
        print(f'  Level: {rec.get("level")}')
        print(f'  Category: {rec.get("schemeCategory")}')
        print(f'  Has eligibility: {bool(rec.get("eligibility"))}')
        print(f'  Keys: {list(rec.keys())}')
else:
    print(f'Error: {resp.text[:500]}')
