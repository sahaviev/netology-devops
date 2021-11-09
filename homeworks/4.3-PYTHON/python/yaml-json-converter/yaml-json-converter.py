#!/usr/bin/env python3

import os
import sys
import json
import yaml


def get_filename_from_params():
    if len(sys.argv) < 2:
        sys.exit('filename is required')
    if not os.path.isfile(sys.argv[1]):
        sys.exit('file not founded, check filename: ' + sys.argv[1])
    if not sys.argv[1].lower().endswith(('.json', '.yaml', '.yml')):
        sys.exit('file must be with YAML or JSON content')
    return sys.argv[1]


def load_file(_filename):
    with open(_filename, "r") as f:
        return f.read()


def detect_format(_data):
    _valid_json = True
    _valid_yaml = True
    exception = False
    print("Start format detection")
    # noinspection PyBroadException
    try:
        print("Trying to load in JSON format")
        json.loads(_data)
        print("Is valid JSON")
    except Exception as e:
        print("Error trying to load the file in JSON format")
        _valid_json = False
        exception = e

    # noinspection PyBroadException
    try:
        print("Trying to load in YAML format")
        yaml.safe_load(_data)
        print("Is valid YAML")
    except Exception as e:
        print("Error trying to load the file in YAML format")
        _valid_yaml = False
        exception = e

    return _valid_json, _valid_yaml, exception


def save_to_yaml(_filename, _data):
    with open(_filename, 'w') as f:
        f.write(yaml.dump(_data, indent=4, explicit_start=True))


def save_to_json(_filename, _data):
    with open(_filename, 'w') as f:
        f.write(json.dumps(_data, indent=4))


def convert(_full_filename):
    filename, extension = os.path.splitext(_full_filename)

    json_extension = extension == '.json'
    yaml_extension = extension in ('.yaml', '.yml')

    data = load_file(full_filename)
    valid_json, valid_yaml, exception = detect_format(data)

    if not valid_json and not valid_yaml:
        quit(exception)

    if json_extension:
        data_dict = json.loads(data)
    elif yaml_extension:
        data_dict = yaml.load(data, Loader=yaml.FullLoader)
    else:
        return 'unknown file extension %s' % extension

    if json_extension and valid_json:
        new_filename = filename + '.yaml'
        save_to_yaml(new_filename, data_dict)
        return '%s with valid JSON converted to %s with YAML' % (full_filename, new_filename)

    if json_extension and valid_yaml:
        new_filename = filename + '-converted.json'
        save_to_json(new_filename, data_dict)
        return '%s with valid YAML converted to %s with JSON' % (full_filename, new_filename)

    if yaml_extension and valid_json:
        new_filename = filename + '-converted.yaml'
        save_to_yaml(new_filename, data_dict)
        return '%s with valid JSON converted to %s with YAML' % (full_filename, new_filename)

    if yaml_extension and valid_yaml:
        new_filename = filename + '.json'
        save_to_json(new_filename, data_dict)
        return '%s with valid YAML converted to %s with JSON' % (full_filename, new_filename)


full_filename = get_filename_from_params()
print(convert(full_filename))
