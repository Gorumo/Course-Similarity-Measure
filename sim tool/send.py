import json
import requests
url = 'http://localhost:9000/similarity/gades'
data = {
"tasks": 
[{
"uri1" : 'http://www.semanticweb.org/MOOCOntology#CS101_Математика', 
"uri2" : 'http://www.semanticweb.org/MOOCOntology#CS100500_Продвинутая_математика'
}]}
r = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
print(r.status_code)
print(r.text)
