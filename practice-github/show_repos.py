import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.github.com") #send a request
conn.request("GET", "/users/Blancahermosilla/repos", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
##print("total number of repos", len(repos))
print(repos)

repo = repos[0]
#print(repo)
for i in repo:
	repos = repo[i]
print(repo["full_name"])
print("The owner of the first repository is", repo['owner']['login'])
