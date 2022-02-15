import requests
import json

url = 'http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=1077'

def scrape():
    profs = dict()
    depts = set()

    data = requests.get(url)
    data = json.loads(data.text)
    numProfs = data['searchResultsTotal']
    print(numProfs)
    for i in range(numProfs//20):
        data = json.loads(requests.get('http://www.ratemyprofessors.com/filter/professor/?&page=' + str(i) + '&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=1077').text)
        for p in data['professors']:
            key = p['tLname'].upper() + (' ' + p['tFname'][0].upper() if p['tFname'] else '') + (' ' + p['tMiddlename'][0].upper() if p['tMiddlename'] else '')
            profs[key] = (p['tid'], p['overall_rating'], p['tDept'])
            depts.add(p['tDept'])

    f = open('data/profs.txt', 'w+')
    f.write(json.dumps(profs))
    f.close()

    f = open('data/depts.txt', 'w+')
    f.write(json.dumps(sorted(list(depts))))
    f.close()

scrape()