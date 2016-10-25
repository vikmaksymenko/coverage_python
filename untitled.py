from flask import Flask
from testrail import *

client = APIClient('https://ecflow.testrail.net/')
client.user = 'vmaksime@electric-cloud.com'
client.password = '88ba3jer'

sections = client.send_get('get_sections/1')
print(sections)

for section in sections:
    print(section['name'])
    cases = client.send_get('get_cases/1&section_id=' + str(section['id']))
    automated = 0
    for case in cases:
        if case['custom_automated']:
            automated += 1

    print('Total cases number: ' + str(len(cases)))
    print('Automated: ' + str(automated))






# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     case = client.send_get('get_case/1446')
#     print(case)
#     return case
#
#
# if __name__ == '__main__':
#     app.run()
