import requests

url = 'http://localhost:80/hooks/post-receive'

data = open('test_data.json').read()
payload = {'payload': data}

r = requests.post(url, data=payload)
print(r.text)
