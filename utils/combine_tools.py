import os
import re

from parse_templates.parse_templates_list import PARSE_TEMPLATES


def combine_data(selected_files):
    results = []
    for file_path in selected_files:
        result = parse_file(file_path)
        results.append(result)
    return results


def parse_file(file_path):
    result = {'error': False}
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.txt':
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    for template in PARSE_TEMPLATES:
                        if re.search(template.detector, line):
                            start = re.search(template.start, line)
                            if not start:
                                result['error'] = True  ##### TO HANDLE
                                continue
                            line = line[start.span()[1]:]
                            end = re.search(template.end, line)
                            if not end:
                                result['error'] = True  ##### TO HANDLE
                                continue
                            line = line[:end.span()[0]]
                            value = float(line)

                            result[template.title] = value
        except Exception as e:
            result['error'] = e  ##### TO HANDLE
    else:
        result['error'] = True  ##### TO HANDLE
    return result
