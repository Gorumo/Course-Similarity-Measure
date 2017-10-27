import json
import random
import uuid
import requests

sem_link = '###  http://www.semanticweb.org/MOOCOntology#'
courses = []
r = requests.get('https://api.oeplatform.ru/courses')
data = r.json()
# Правила замены ключей из api в формат онтологии
api = ['created_at', 'started_at', 'record_end_at', 'finished_at', 'institution_id', 'partner_id', 'experts_rating',
       'visitors_number', 'total_visitors_number', 'lectures_number', 'external_url', 'has_certificate', 'credits', 'teachers', 'feedback', 'directions', 'activities', 'requirements']
owl = ['createdAt', 'startedAt', 'recordEndAt', 'finishedAt', 'isProducedBy', 'isOrganizedBy',
       'expertsRating', 'visitorsNumber', 'totalVisitorsNumber', 'lecturesNumber', 'externalUrl', 'hasCertificate', 'hasCredit', 'isCreatedBy', 'hasFeedback', 'belongsToDirection', 'belongsToActivity', 'hasRequirements']
# аттрибуты из массивов
lists = ['hasCredit', 'isCreatedBy', 'hasFeedback']
# связи по ключам из внешних табилц
tables = ['isProducedBy', 'isOrganizedBy',
          'belongsToDirection', 'belongsToActivity']

for i in range(data['count']):
    global_id = data['results'][i]['global_id']
    spaces = len(':' + global_id + ' rdf:type ')
    row = [sem_link + global_id, ':' + global_id +
           ' rdf:type owl:NamedIndividual ,', ' ' * spaces + ':Course ;']
    r = requests.get('https://api.oeplatform.ru/courses/' + global_id)
    course_item = r.json()
    # global_id уже записан в необходимом формате
    course_item.pop('global_id')
    spaces = len(global_id) + 2
    for key in course_item.keys():
        individual = course_item[key]
        if individual:  # Пустые аттрибуты не парсим
            if key in api:
                key = owl[api.index(key)]
            if key == 'isProducedBy':
                row.append(' ' * spaces + ':%s :institution_%s ;' %
                           (key, individual))
            elif key == 'isOrganizedBy':
                row.append(' ' * spaces + ':%s :partner_%s ;' %
                           (key, individual))
            elif isinstance(individual, int):
                row.append(' ' * spaces + ':%s %s ;' % (key, individual))
            elif isinstance(individual, str):
                row.append(' ' * spaces + ''':%s '%s' ;''' % (key, individual))
            elif isinstance(individual, list):
                if key == 'hasCredit':
                    spaces = len(global_id) + 2
                    somecredit_uri = str(uuid.uuid4())
                    row.append(' ' * spaces + ':%s :%s .' %
                               (key, somecredit_uri))
                    row.append('\n')
                elif key == 'belongsToDirection':
                    for z in range(len(course_item['directions'])):
                        if len(course_item['directions']) == 1:
                            spaces = len(global_id) + 2
                            row.append(' ' * spaces + ':%s :direction_%s ;' %
                                       (key, course_item['directions'][z]))
                        elif z == 0:
                            spaces = len(global_id) + 2
                            row.append(' ' * spaces + ':%s :direction_%s ,' %
                                       (key, course_item['directions'][z]))
                        elif z == len(course_item['directions']) - 1:
                            spaces = len(
                                global_id + ':belongsToDirection ') + 2
                            row.append(' ' * spaces + ':direction_%s ;' %
                                       (course_item['directions'][z]))
                        else:
                            spaces = len(
                                global_id + ':belongsToDirection ') + 2
                            row.append(' ' * spaces + ':direction_%s ,' %
                                       (course_item['directions'][z]))
                elif key == 'belongsToActivity':
                    for z in range(len(course_item['activities'])):
                        if len(course_item['activities']) == 1:
                            spaces = len(global_id) + 2
                            row.append(' ' * spaces + ':%s :activity_%s ;' %
                                       (key, course_item['activities'][z]))
                        elif z == 0:
                            spaces = len(global_id) + 2
                            row.append(' ' * spaces + ':%s :activity_%s ,' %
                                       (key, course_item['activities'][z]))
                        elif z == len(course_item['activities']) - 1:
                            spaces = len(global_id + ':belongsToActivity ') + 2
                            row.append(' ' * spaces + ':activity_%s ;' %
                                       (course_item['activities'][z]))
                        else:
                            spaces = len(global_id + ':belongsToActivity ') + 2
                            row.append(' ' * spaces + ':activity_%s ,' %
                                       (course_item['activities'][z]))
                # elif key == 'isCreatedBy':
                #   someteacher_uri=str(uuid.uuid4())
                #   row.append(':%s :%s ;' % (key, someteacher_uri))
                # elif key == 'hasFeedback':
                #   somefeedback_uri=str(uuid.uuid4())
                #   row.append(':%s :%s ;' % (key, somefeedback_uri))
    spaces = len(':' + somecredit_uri + ' rdf:type ')
    row.extend([sem_link + somecredit_uri, ':' + somecredit_uri +
                ' rdf:type owl:NamedIndividual ,', ' ' * spaces + ':Credit ;'])
    # Создание individuals для перезачетов в других университетах
    for z in range(len(course_item['credits'])):
        if z == 0:
            spaces = len(somecredit_uri) + 2
            row.append(' ' * spaces + ':%s :institution_%s ,' % ('isAcceptedInInstitution',
                                                                 course_item['credits'][z]['institution_id']))
        elif z == len(course_item['credits']) - 1:
            spaces = len(somecredit_uri + ':isAcceptedInInstitution ') + 2
            row.append(' ' * spaces + ':institution_%s ;' %
                       (course_item['credits'][z]['institution_id']))
        else:
            spaces = len(somecredit_uri + ':isAcceptedInInstitution ') + 2
            row.append(' ' * spaces + ':institution_%s ,' %
                       (course_item['credits'][z]['institution_id']))
    for z in range(len(course_item['credits'])):
        if z == 0:
            spaces = len(somecredit_uri) + 2
            row.append(' ' * spaces + ':%s :direction_%s ,' % ('isgetForDirection',
                                                               course_item['credits'][z]['direction_id']))
        elif z == len(course_item['credits']) - 1:
            spaces = len(somecredit_uri + ':isgetForDirection ') + 2
            row.append(' ' * spaces + ':direction_%s .' %
                       (course_item['credits'][z]['direction_id']))
        else:
            spaces = len(somecredit_uri + ':isgetForDirection ') + 2
            row.append(' ' * spaces + ':direction_%s ,' %
                       (course_item['credits'][z]['direction_id']))
  # if isinstance(course_item[key],list):
            # print(key,course_item[key])
            # for keys in course_item[key].keys():
            #   print(keys)
    row.append('\n')
    with open('MOOC.ttl', 'a') as file:
        print(*row, file=file, sep='\n')

r = requests.get('https://api.oeplatform.ru/institutions')
data = r.json()
for inst in data:
    inst_id = 'institution_' + str(inst['id'])
    spaces = len(':' + inst_id + ' rdf:type ')
    row = [sem_link + inst_id, ':' + inst_id +
           ' rdf:type owl:NamedIndividual ,', ' ' * spaces + ':Institution ;']
    spaces = len(':' + inst_id + ' ')
    row.append(' ' * spaces + ''':institutionTitle '%s' ;''' % inst['title'])
    row.append(' ' * spaces + ''':institutionDescription '%s' ;''' %
               inst['description'])
    row.append(' ' * spaces + ''':institutionImage '%s' ;''' % inst['image'])
    row.append(' ' * spaces + ''':institutionUrl '%s' .''' % inst['url'])
    row.append('\n')
    with open('MOOC.ttl', 'a') as file:
        print(*row, file=file, sep='\n')

r = requests.get('https://api.oeplatform.ru/partners')
data = r.json()
for partn in data:
    partner_id = 'partner_' + str(partn['id'])
    spaces = len(':' + partner_id + ' rdf:type ')
    row = [sem_link + partner_id, ':' + partner_id +
           ' rdf:type owl:NamedIndividual ,', ' ' * spaces + ':Partner ;']
    spaces = len(':' + partner_id + ' ')
    row.append(' ' * spaces + ''':partnerTitle '%s' ;''' % partn['title'])
    row.append(' ' * spaces + ''':partnerDescription '%s' ;''' %
               partn['description'])
    row.append(' ' * spaces + ''':partnerImage '%s' ;''' % partn['image'])
    row.append(' ' * spaces + ''':partnerUrl '%s' .''' % partn['url'])
    row.append('\n')
    with open('MOOC.ttl', 'a') as file:
        print(*row, file=file, sep='\n')

r = requests.get('https://api.oeplatform.ru/directions')
data = r.json()
for direct in data:
    direction_id = 'direction_' + str(direct['id'])
    spaces = len(':' + direction_id + ' rdf:type ')
    row = [sem_link + direction_id, ':' + direction_id +
           ' rdf:type owl:NamedIndividual ,', ' ' * spaces + ':Direction ;']
    spaces = len(':' + direction_id + ' ')
    row.append(' ' * spaces + ''':directionTitle '%s' ;''' % direct['title'])
    row.append(' ' * spaces + ''':directionCode '%s' .''' % direct['code'])
    row.append('\n')
    with open('MOOC.ttl', 'a') as file:
        print(*row, file=file, sep='\n')

r = requests.get('https://api.oeplatform.ru/activities')
data = r.json()
for activ in data:
    activity_id = 'activity_' + str(activ['id'])
    spaces = len(':' + activity_id + ' rdf:type ')
    row = [sem_link + activity_id, ':' + activity_id +
           ' rdf:type owl:NamedIndividual ,', ' ' * spaces + ':Activity ;']
    spaces = len(':' + activity_id + ' ')
    row.append(' ' * spaces + ''':activityTitle '%s' .''' % activ['title'])
    row.append('\n')
    with open('MOOC.ttl', 'a') as file:
        print(*row, file=file, sep='\n')
#row = [sem_link + data['id'], ':' + global_id +' rdf:type owl:NamedIndividual ,', ' '*spaces+':Course ;']
    # courses.append(row)
    # print(row)
# print(courses)


# with open('Import Template.json') as data_file:
    # data = json.load(data_file)


# print(data['Properties']['formsCompetency'][0])

# f.close()    :courseTitle 'CS101 Математика' .  data['Course'][i]
