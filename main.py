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

import sys
import coverage

url = sys.argv[3]
user = sys.argv[1]
password = sys.argv[2]
project_id = sys.argv[4]
depth = sys.argv[5]

coverage = coverage.Coverage(url, user, password)
coverage.get_sections(project_id)
coverage.write_csv_report(depth, True)
coverage.write_csv_report(depth, False)
