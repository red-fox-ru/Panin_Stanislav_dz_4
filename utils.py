# Name:        Курс валют через имортированный модуль
# Author:      Panin Stanislav
# Created:     23.03.2021

from task_2 import currency_rates


def main():
    print(currency_rates('AMD'))
    print(currency_rates('MDL', 'TRY'))


if __name__ == '__main__':
    main()
