import json
import requests
url = 'http://localhost:9000/similarity/gades'
data = {
"tasks": 
[{
"uri1" : 'http://www.semanticweb.org/EdxOntology/Main#5964fec656c02c4382a94a3d', 
"uri2" : 'http://www.semanticweb.org/EdxOntology/Main#59651a0f56c02c021ca949f6'
}]}
r = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
print(r.status_code)
print(r.text)
