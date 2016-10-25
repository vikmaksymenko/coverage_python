##
# Script for getting automation test cases coverage from TestRail
#
# Usage:
#
# perl coverage.py <user_login> <user_password> <URL> <project_id>
# URL and project_id are optional
# 'https://ecflow.testrail.net/' and 1 (id of platform project) will be used by default
#
# With any questions contact
# vmaksime@electric-cloud.com


# from flask import Flask
from testrail import *
import sys
import printProgress


print(sys.argv[0])

# url = sys.argv[3]
# client = APIClient(url)
# client.user = sys.argv[1]
# client.password = sys.argv[2]
# project_id = sys.argv[4] | 1

# sections = client.send_get('get_sections/' + str(project_id))
# # print(sections)
#
# sections = sorted(sections, key=lambda k: k['depth'], reverse=True)
#
# print(sections)
#
# # Set up sections dictionary with blank cases counters
# sections_dict = {}
# for section in sections:
#     section['cases_number'] = 0
#     section['automated_cases_number'] = 0
#     section['total_cases_number'] = 0
#     section['total_automated_cases_number'] = 0
#     sections_dict[section['id']] = section
#
# i = 0
# l = len(sections)
# print('Getting cases for each section:')
# printProgress.printProgress(i, l, prefix='Progress:', suffix='Complete', barLength=50)
#
# for key, section in sections_dict.items():
#     cases = client.send_get('get_cases/1&section_id=' + str(section['id']))
#     section['cases_number'] = len(cases)
#     section['automated_cases_number'] = 0
#
#     for case in cases:
#         if case['custom_automated']:
#             section['automated_cases_number'] += 1
#
#     if section['parent_id'] is not None:
#         parent = sections_dict[section['parent_id']]
#         parent['total_cases_number'] = parent['cases_number'] + section['cases_number']
#         parent['total_automated_cases_number'] = parent['automated_cases_number'] + section['automated_cases_number']
#
#     i += 1
#     printProgress.printProgress(i, l, prefix='Progress:', suffix='Complete', barLength=50)
#
# for key, section in sections_dict.items():
#     if section['parent_id'] is None:
#         print('===== ' + section['name'])
#         print('Total cases number: ' + str(section['total_cases_number']))
#         print('Automated: ' + str(section['total_automated_cases_number']))

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
