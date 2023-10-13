import os
import re
import copy

from parse_templates.parse_templates_list import TEMPLATES_TITLES, PARSE_TEMPLATES
from utils.errors_messages import get_error_message, get_general_error_message
from utils.rounding_func import round_dec

from сurrency_сonvertion.currencies import CURRENCIES_SYMBOLS_CODES_DICT
from сurrency_сonvertion.сonverter import set_rates, convert, EXCHANGE_RATE, EXCHANGE_RATE_STATIC

# del
import pprint
pp = pprint.PrettyPrinter(indent=4)


def combine_data(selected_files):
    tournament_checklist = []
    metrics = create_metrics()
    errors = {
        'general_errors': [],
        'file_errors': []
    }

    set_exchange_rates = set_rates()
    if not set_exchange_rates:
        errors['general_errors'].append(get_general_error_message(error='fixed'))
    elif set_exchange_rates == 2:
        errors['general_errors'].append(get_general_error_message(error='static'))

    for file_path in selected_files:
        result = parse_file(file_path)
        # pp.pprint(result)
        if not result['errors']:
            if result['content'] in tournament_checklist:
                metrics['doubles'] += 1
                continue

            tournament_checklist.append(result['content'])

            metrics['tournaments_n'] += 1  # проверка на дубли должна быть
            metrics['re_entries_n'] += result['data'][f'{TEMPLATES_TITLES["re_entry"]}']['value']

            currency_symbol = result['data'][f'{TEMPLATES_TITLES["currency"]}']['value']
            currency_code = CURRENCIES_SYMBOLS_CODES_DICT[currency_symbol]

            # BUI_IN
            buy_in = round_dec(result['data'][f'{TEMPLATES_TITLES["buy_in"]}']['value'])
            re_entry = result['data'][f'{TEMPLATES_TITLES["re_entry"]}']['value']
            metrics[f'{TEMPLATES_TITLES["buy_in"]}']['first_entries'][currency_code] += buy_in
            metrics[f'{TEMPLATES_TITLES["buy_in"]}']['re_entries'][currency_code] += buy_in * re_entry
            metrics[f'{TEMPLATES_TITLES["buy_in"]}']['total'][currency_code] += buy_in + buy_in * re_entry
            # ЗДЕСЬ НУЖНО ДОПОЛНИТЬ КОНВЕРТАЦИЕЙ ВАЛЮТ
            if currency_code == 'USD':
                convert_buy_in = buy_in
            else:
                convert_buy_in = round_dec(convert(currency=currency_code, amount=buy_in))
            if set_exchange_rates:
                metrics[f'{TEMPLATES_TITLES["buy_in"]}']['first_entries']['convert'] += convert_buy_in
                metrics[f'{TEMPLATES_TITLES["buy_in"]}']['re_entries']['convert'] += convert_buy_in * re_entry
                metrics[f'{TEMPLATES_TITLES["buy_in"]}']['total']['convert'] += convert_buy_in + convert_buy_in * re_entry

            # TOTAL_RECEIVED
            total_received = round_dec(result['data'][f'{TEMPLATES_TITLES["total_received"]}']['value'])
            metrics[f'{TEMPLATES_TITLES["total_received"]}'][currency_code] += total_received
            # ЗДЕСЬ НУЖНО ДОПОЛНИТЬ КОНВЕРТАЦИЕЙ ВАЛЮТ
            if currency_code == 'USD':
                convert_total_received = total_received
            else:
                convert_total_received = round_dec(convert(currency=currency_code, amount=total_received))
            if set_exchange_rates:
                metrics[f'{TEMPLATES_TITLES["total_received"]}']['convert'] += convert_total_received

        else:
            error_dict = {
                'file': result['file'],
                'content': result['content'],
                'errors': result['errors']
            }
            errors['file_errors'].append(error_dict)

    metrics['total_entries_n'] = metrics['tournaments_n'] + metrics['re_entries_n']
    metrics['profit'] = metrics[f'{TEMPLATES_TITLES["total_received"]}']['convert'] - \
                    metrics[f'{TEMPLATES_TITLES["buy_in"]}']['total']['convert']

    pp.pprint(metrics)

    pp.pprint(errors)


def create_metrics() -> dict:
    currency_metric_dict = {'convert': 0} | {code: 0 for code in CURRENCIES_SYMBOLS_CODES_DICT.values()}

    finance_metric_dict = {
        'total': copy.deepcopy(currency_metric_dict),
        'first_entries': copy.deepcopy(currency_metric_dict),
        're_entries': copy.deepcopy(currency_metric_dict)
    }

    metrics = {
        'tournaments_n': 0,
        're_entries_n': 0,
        'total_entries_n': 0,
        'doubles': 0,

        f'{TEMPLATES_TITLES["buy_in"]}': copy.deepcopy(finance_metric_dict),

        f'{TEMPLATES_TITLES["total_received"]}': copy.deepcopy(currency_metric_dict),

        'profit': 0
    }

    return metrics


def parse_file(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.txt':
        result = create_result()

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                result['file'] = os.path.basename(file.name)
                for line in file:
                    if line == '\n':
                        continue
                    result['content'] += line
                    result = parse_line(line=line, result=result)

        except Exception as e:
            result['errors'].append(get_error_message('other', str(e)))

        for k, v in result['data'].items():
            if v['quantity'] > 1:
                result['errors'].append(get_error_message(k, 'multiple'))
            elif v['quantity'] == 0 and v['template'].required:
                result['errors'].append(get_error_message(k, 'notfound'))

        return result
    return None


def create_result() -> dict:
    data = {template.title: {'template': template, 'value': 0, 'quantity': 0} for template in PARSE_TEMPLATES}

    result = {
        'file': '',
        'content': '',
        'data': copy.deepcopy(data),
        'errors': []
    }

    return result


def parse_line(line, result):
    for template in PARSE_TEMPLATES:
        tt = template.title
        if re.search(template.detector, line):
            start = re.search(template.start, line)
            if not start:
                result['errors'].append(get_error_message(template.title, 'unlimited'))
                continue
            extract_line = line[start.span()[1]:]
            end = re.search(template.end, extract_line)
            if not end:
                result['errors'].append(get_error_message(template.title, 'unlimited'))
                continue
            extract_line = extract_line[:end.span()[0]]
            extract_line = re.sub(',', '', extract_line)
            try:
                type_func = result['data'][tt]['template'].ttype
                value = type_func(extract_line)
                result['data'][tt]['value'] = value
                result['data'][tt]['quantity'] += 1
            except ValueError:
                result['errors'].append(get_error_message(template.title, 'unknown'))
    return result
