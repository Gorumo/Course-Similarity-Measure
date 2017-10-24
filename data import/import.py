import json
import random
import uuid
from pprint import pprint

with open('data.json') as data_file:    
    data = json.load(data_file)
#f = open('export.ttl', 'a')
courses = []
for i in range(2): #Количество курсов
	i=random.randint(1,len(data["Course"]))
	course_id=uuid.uuid4().hex
	#Генерация курсов
	row = ['###  http://www.semanticweb.org/MOOCOntology#'+course_id,':'+course_id+' rdf:type owl:NamedIndividual ,',':Course .',':courseTitle "'+data["Course"][i]+'"']
	courses.append(row)
	with open("export.ttl", "a") as file:
		print(*row, file=file, sep="\n")
#print(courses)
#f.write("%s\n" % item)
#f.close()    :courseTitle "CS101 Математика" .  data["Course"][i]