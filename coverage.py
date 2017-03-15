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
import printProgress
import csv


class Coverage:

    def __init__(self, url, user, password):
        self.client = APIClient(url)
        self.client.user = user
        self.client.password = password

    def _get_sections(self, project_id):
        self.sections = self.client.send_get('get_sections/' + str(project_id))
        self.sections = sorted(self.sections, key=lambda k: k['depth'], reverse=True)

    def _do_sections_dict(self):
        self.sections_dict = {}
        for section in self.sections:
            section['cases_number'] = 0
            section['automated_cases_number'] = 0
            section['total_cases_number'] = 0
            section['total_automated_cases_number'] = 0
            self.sections_dict[section['id']] = section

    def _get_cases_in_section(self, project_id):
        i = 0
        l = len(self.sections)
        print('Getting cases for each section:')
        printProgress.printProgress(i, l, prefix='Progress: {} of {}'.format(str(i), str(l)), suffix='Complete', barLength=50)

        for key, section in self.sections_dict.items():
            cases = self.client.send_get('get_cases/' + str(project_id) + '&section_id=' + str(section['id']))
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

    def _get_total_cases_number_in_section(self):
        for section in self.sections:

            # Debug
            # aSection = sections_dict[section['id']]
            # print("======")
            # print("Section: " + aSection['name'])
            # print("Section cases: " + str(aSection['total_cases_number']))
            # print("Section automated cases: " + str(aSection['total_automated_cases_number']))

            if section['parent_id'] is not None:
                parent = self.sections_dict[section['parent_id']]
                child = self.sections_dict[section['id']]
                parent['total_cases_number'] += child['total_cases_number']
                parent['total_automated_cases_number'] += child['total_automated_cases_number']

                # Debug
                # print("Parent: " + parent['name'])
                # print("Parent cases: " + str(parent['total_cases_number']))
                # print("Parent automated cases: " + str(parent['total_automated_cases_number']))

            # Debug
            # print("=====\n")

    def _get_section_full_name(self, section):
        path = section['name']
        cur_section = section

        while cur_section['parent_id'] is not None:
            cur_section = self.sections_dict[cur_section['parent_id']]
            path = cur_section['name'] + " - " + path

    def _write_csv_report_vertical(self, depth):
        with open('coverage.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Section', 'Total Cases Number', 'Automated Cases Number'])
            for key, section in self.sections_dict.items():
                if section['parent_id'] is None:
                    print('===== ' + section['name'])
                    print('\tTotal cases number: ' + str(section['total_cases_number']))
                    print('\tAutomated: ' + str(section['total_automated_cases_number']))

                    writer.writerow([section['name'], section['total_cases_number'], section['total_automated_cases_number']])

    def _write_csv_report_horisontal(self, depth):
        with open('coverage2.csv', 'w', newline='') as csvfile:
            labels = ['']
            automated = ['Automated']
            non_automated = ['Not Automated']

            for key, section in self.sections_dict.items():
                if section['parent_id'] is None:
                    labels.append(section['name'])
                    automated.append(section['total_automated_cases_number'])
                    non_automated.append(section['total_cases_number'] - section['total_automated_cases_number'])

            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(labels)
            writer.writerow(automated)
            writer.writerow(non_automated)

    def get_sections(self, project_id):
        self._get_sections(project_id)
        self._do_sections_dict()
        self._get_cases_in_section(project_id)
        self._get_total_cases_number_in_section()

    def write_csv_report(self, depth, cases_in_row):
        if cases_in_row:
            self._write_csv_report_vertical(depth)
        else:
            self._write_csv_report_horisontal(depth)
