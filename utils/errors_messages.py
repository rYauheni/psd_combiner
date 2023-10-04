def get_error_message(template, error='error'):
    if error == 'notfound':
        return f'Template {template} not found in file'
    elif error == 'unknown':
        return f'Template {template} not parsed in line'
    elif error == 'unlimited':
        return f'Limits (start or(and) end) of template {template} not parsed in line'
    elif error == 'multiple':
        return f'Template {template} more than once in file'
    else:
        return f'Template {template} - unknown error - {error}'
