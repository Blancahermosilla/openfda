import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #send a request
conn.request("GET","/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
##print("The id is", repos['results'][0]['id'])
#print("The purpose is", repos['results'][0]['purpose'])
#print("The name if the manufacturer is", repos['results'][0]['openfda']['manufacturer_name'])

for i in range(len(repos['results'])):
    print(repos['results'][i]['id'])
