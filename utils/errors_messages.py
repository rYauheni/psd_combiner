def get_error_message(template, error='error'):
    if error == 'notfound':
        return f'ERROR: Template {template} not found in file'
    elif error == 'unknown':
        return f'ERROR: Template {template} not parsed in line'
    elif error == 'unlimited':
        return f'ERROR: Limits (start or(and) end) of template {template} not parsed in line'
    elif error == 'multiple':
        return f'ERROR: Template {template} more than once in file'
    else:
        return f'ERROR: Template {template} - unknown error - {error}'


def get_general_error_message(error='error'):
    if error == 'static':
        return 'WARNING: Static exchange rate applied'
    elif error == 'notcurrency':
        return 'ERROR: exchange rate is not determined'


