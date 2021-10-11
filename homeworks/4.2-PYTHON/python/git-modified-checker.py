#!/usr/bin/env python3

import os
import sys

if len(sys.argv) > 1 and not os.path.isdir(sys.argv[1]):
    sys.exit('project not founded, check directory path: ' + sys.argv[1])

project_folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
print('project_folder: ' + project_folder)
bash_command = ["cd " + project_folder, 'git status']
result_os = os.popen(' && '.join(bash_command)).read()

for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(project_folder + '/' + prepare_result)
