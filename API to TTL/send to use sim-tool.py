import json
import requests
url = 'http://localhost:9000/similarity/gades'

#r = requests.post(url, data=json.dumps(data), headers={
#                  "Content-Type": "application/json"})
#print(r.status_code)
#print(r.text)

api = requests.get('https://api.oeplatform.ru/courses')
data = api.json()
ids = []
course_number = data['count']
for i in range(data['count']):
    ids.append(data['results'][i]['global_id'])
data = {
    "tasks":[]}
for i in range(course_number):
	for j in range(i+1,course_number):
		d=dict(uri1='http://www.semanticweb.org/MOOCOntology#'+ids[i], uri2='http://www.semanticweb.org/MOOCOntology#'+ids[j])
		data["tasks"].append(d)
r = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
print(r.status_code)
print(r.text)