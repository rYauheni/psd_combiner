import os
import re

from parse_templates.parse_templates_list import PARSE_TEMPLATES
from utils.errors_messages import get_error_message


def combine_data(selected_files):
    results = []
    for file_path in selected_files:
        result = parse_file(file_path)
        results.append(result)
    return results


def parse_file(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.txt':
        result = {
            'file': '',
            'content': '',
            'data': {},
            'errors': []
        }
        try:
            with open(file_path, 'r') as file:
                result['file'] = os.path.basename(file.name)
                result['data'] = {template.title: {'template': template, 'value': 0, 'quantity': 0} for template in
                                  PARSE_TEMPLATES}
                # result['content'] = file.read()
                for line in file:
                    if line == '\n':
                        continue
                    result['content'] += line
                    for template in PARSE_TEMPLATES:
                        tt = template.title
                        if re.search(template.detector, line):
                            start = re.search(template.start, line)
                            if not start:
                                result['errors'].append(get_error_message(template.title, 'unlimited'))
                                continue
                            line = line[start.span()[1]:]
                            end = re.search(template.end, line)
                            if not end:
                                result['errors'].append(get_error_message(template.title, 'unlimited'))
                                continue
                            line = line[:end.span()[0]]
                            try:
                                value = float(line)
                                result['data'][tt]['value'] = value
                                result['data'][tt]['quantity'] += 1
                            except ValueError:
                                result['errors'].append(get_error_message(template.title, 'unknown'))

        except Exception as e:
            result['errors'].append(get_error_message(template.title, str(e)))

        for k, v in result['data'].items():
            if v['quantity'] > 1:
                result['errors'].append(get_error_message(k, 'multiple'))
            elif v['quantity'] == 0 and v['template'].required:
                result['errors'].append(get_error_message(k, 'notfound'))

        return result
    return None
