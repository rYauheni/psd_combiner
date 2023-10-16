import os
import re
import copy

from parse_templates.parse_templates_list import TEMPLATES_TITLES, PARSE_TEMPLATES
from utils.errors_messages import get_error_message, get_general_error_message
from utils.rounding_func import round_dec

from сurrency_сonvertion.currencies import CURRENCIES_SYMBOLS_CODES_DICT, CURRENCIES_SYMBOLS
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
                metrics[f'{TEMPLATES_TITLES["buy_in"]}']['total'][
                    'convert'] += convert_buy_in + convert_buy_in * re_entry

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
                lines = file.readlines()
                for line in lines:
                    if line == '\n':
                        continue
                    result['content'] += line
                    result = parse_line(line=line, templates=PARSE_TEMPLATES, result=result)

                check_errors(result=result)

                # processing files that do not correspond to standard PARSE_TEMPLATES
                if result['errors']:
                    alt_result = create_result()

                    if 'freeroll' in lines[0].lower():
                        pt_list = list(PARSE_TEMPLATES)
                        t_buy_in = [template for template in pt_list if template.title == TEMPLATES_TITLES['buy_in']][0]
                        index_t_buy_in = pt_list.index(t_buy_in)
                        pt_list.pop(index_t_buy_in)

                        alt_result['data']['buy_in']['value'] = 0
                        alt_result['data']['buy_in']['quantity'] = 1

                        for line in lines:
                            if line == '\n':
                                continue
                            alt_result['content'] += line
                            alt_result = parse_line(line=line, templates=pt_list, result=alt_result)

                    # elif 'stage' in lines[0].lower():
                    else:
                        for line in lines:
                            if line == '\n':
                                continue
                            alt_result['content'] += line
                            alt_result = parse_line_stage(line=line, alt_result=alt_result)

                    check_errors(result=alt_result)
                    if not alt_result['errors']:
                        result = copy.deepcopy(alt_result)

        except Exception as e:
            result['errors'].append(get_error_message('other', str(e)))

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


def parse_line(line, templates, result):
    for template in templates:
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


def parse_line_stage(line, alt_result):
    symbols = CURRENCIES_SYMBOLS
    line = line.lower()

    # buy-in template
    if 'buy-in' in line:
        try:
            elements = re.findall(r'\d+\.\d+|\d+', line)
            elements = [elem.replace(',', '') for elem in elements]
            buy_in = sum(float(elem) for elem in elements) + 4.5
            alt_result['data']['buy_in']['value'] += buy_in
            alt_result['data']['buy_in']['quantity'] += 1
        except Exception as e:
            alt_result['errors'].append(get_error_message('buy_in', str(e)))

    # currency template and knock out prize (total received template)
    elif 'hero' in line:
        try:
            for symbol in symbols:
                if symbol in line:
                    currency = symbol
                    alt_result['data']['currency']['value'] = currency
                    alt_result['data']['currency']['quantity'] += 1

                    try:
                        find_prize = line.count(currency)
                        if find_prize == 2:
                            elements = re.findall(fr'{currency}(\d+)', line)
                            prize = float(elements[1].replace(',', ''))
                            alt_result['data']['total_received']['value'] += prize
                            alt_result['data']['total_received']['quantity'] += 1
                    except Exception as e:
                        alt_result['errors'].append(get_error_message('total_received', str(e)))

                    break

        except Exception as e:
            alt_result['errors'].append(get_error_message('currency', str(e)))

    # total received template
    elif 'received a total' in line:
        try:
            for symbol in symbols:
                if symbol in line:
                    currency = symbol
                    elements = re.search(fr'{currency}([\d,]+(?:\.\d+)?)', line)
                    if elements:
                        prize = float(elements.group(1).replace(',', ''))
                        alt_result['data']['total_received']['value'] += prize
                        if not alt_result['data']['total_received']['quantity']:
                            alt_result['data']['total_received']['quantity'] += 1

                    break
        except Exception as e:
            alt_result['errors'].append(get_error_message('currency', str(e)))

    # total received template
    elif 'chips' in line:
        alt_result['data']['total_received']['value'] += 0
        if not alt_result['data']['total_received']['quantity']:
            alt_result['data']['total_received']['quantity'] += 1

    # re-entry template
    if 're-entries' in line:  # 'if' is correct (not 'elif')
        try:
            elements = re.search(r'(\d+)\sre-entries', line)
            if elements:
                re_entries = int(elements.group(1))
                alt_result['data']['re_entry']['value'] += re_entries
                alt_result['data']['re_entry']['quantity'] += 1
        except Exception as e:
            alt_result['errors'].append(get_error_message('re_entry', str(e)))

    return alt_result


def check_errors(result):
    for tt, tt_data in result['data'].items():
        if tt_data['quantity'] > 1:
            result['errors'].append(get_error_message(tt, 'multiple'))
        elif tt_data['quantity'] == 0 and tt_data['template'].required:
            result['errors'].append(get_error_message(tt, 'notfound'))
