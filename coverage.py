##
# Script for getting automation test cases coverage from TestRail
#
# Usage:
#
# python coverage.py <user_login> <user_password> <URL> <project_id>
# URL and project_id are optional
# 'https://ecflow.testrail.net/' and 1 (id of platform project) will be used by default
# As a result, coverage.csv file will be created
#
# With any questions contact
# vmaksime@electric-cloud.com

from testrail import *
import sys
import printProgress
import csv

url = sys.argv[3] if len(sys.argv) > 3 else 'https://ecflow.testrail.net/'
client = APIClient(url)
client.user = sys.argv[1]
client.password = sys.argv[2]
project_id = sys.argv[4] if len(sys.argv) > 4 else 1

sections = client.send_get('get_sections/' + str(project_id))
sections = sorted(sections, key=lambda k: k['depth'], reverse=True)

sections_dict = {}
for section in sections:
    section['cases_number'] = 0
    section['automated_cases_number'] = 0
    section['total_cases_number'] = 0
    section['total_automated_cases_number'] = 0
    sections_dict[section['id']] = section

i = 0
l = len(sections)
print('Getting cases for each section:')
printProgress.printProgress(i, l, prefix='Progress: {} of {}'.format(str(i), str(l)), suffix='Complete', barLength=50)

for key, section in sections_dict.items():
    cases = client.send_get('get_cases/1&section_id=' + str(section['id']))
    section['cases_number'] = len(cases)
    section['automated_cases_number'] = 0

    for case in cases:
        if case['custom_automated']:
            section['automated_cases_number'] += 1

    section['total_cases_number'] = section['cases_number']
    section['total_automated_cases_number'] = section['automated_cases_number']

    i += 1
    prefix = 'Progress: {} of {}'.format(str(i), str(l))
    printProgress.printProgress(i, l, prefix=prefix, suffix='Complete', barLength=50)

for section in sections:
    if section['parent_id'] is not None:
        parent = sections_dict[section['parent_id']]
        parent['total_cases_number'] += section['cases_number']
        parent['total_automated_cases_number'] += section['automated_cases_number']

with open('coverage.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Section', 'Total Cases Number', 'Automated Cases Number'])
    for key, section in sections_dict.items():
        if section['parent_id'] is None:
            print('===== ' + section['name'])
            print('\tTotal cases number: ' + str(section['total_cases_number']))
            print('\tAutomated: ' + str(section['total_automated_cases_number']))

            writer.writerow([section['name'], section['total_cases_number'], section['total_automated_cases_number']])

