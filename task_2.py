# Name:        Курс валют через API
# Author:      Panin Stanislav
# Created:     23.03.2021

import requests, sys, datetime


def get_element(url):
    """
    Just GET-request
    :param url:
    :return:
    """
    r = requests.get(url)
    r.encoding = 'windows-1251'
    result = r.content.decode(encoding=r.encoding)
    return result


def data_resource(url):
    """
    Get list of currencies and values
    Return in zip Object
    :param url:
    :return:
    """
    resource = get_element(url)
    importance = [el.split('</')[0] for el in resource.split('<CharCode>')[1:]]
    value = [float(el.split('</')[0].replace(',', '.')) for el in resource.split('<Value>')[1:]]
    par = [int(el.split('</')[0]) for el in resource.split('<Nominal>')[1:]]
    par_value = [round(x / y, 4) for x, y in zip(value, par)]
    return zip(importance, par_value)


def date_curr(url):
    """
    Get date and save in Object Date
    :param url:
    :return:
    """
    resource = get_element(url)
    get_date = [el.split('"')[0] for el in resource.split('Date="')[1:]]
    get_date = get_date[0].split('.')
    date = datetime.datetime(year=int(get_date[2]), month=int(get_date[1]), day=int(get_date[0]))
    return date.strftime('%d-%m-%Y')


def currency_rates(*abbr):
    """
    Accepts an abbreviation argument
    Conclusion: rate currencies
    :param abbr:
    :return:
    """
    dict_curr = {}
    result = []
    currency = data_resource('http://www.cbr.ru/scripts/XML_daily.asp')
    date = date_curr('http://www.cbr.ru/scripts/XML_daily.asp')
    for imp, val in currency:
        dict_curr[imp] = val

    for el in abbr:
        if isinstance(el, list):
            for arg in el:
                result.append(f'{date}\n{arg.upper()} = {dict_curr[arg.upper()]}\n')
        else:
            try:
                result.append(f'{date}\n{el.upper()} = {dict_curr[el.upper()]}\n')
            except KeyError:
                return None
    return '\n'.join(result)


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
    except ValueError:
        args = input('Введите параметр: ')
    print(currency_rates(args))
