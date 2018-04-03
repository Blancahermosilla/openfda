import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=10", None, headers) #4 is the total number of records matching the search
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

#of the 4 total matches two of them are empty dicts
for i in range(len(repos['results'])):
    if repos['results'][i]['openfda'] == {}:
        continue
    else:
        print(repos['results'][i]['openfda']['manufacturer_name'])
