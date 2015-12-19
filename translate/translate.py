#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''translate.translate: provides main() entry point.'''

__version__ = '0.1.0'


import logging
import argparse

import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

logging.basicConfig(
        filename = '.log',
        filemode = 'a+',
        level    = logging.INFO,
        format   = '%(asctime)s | %(levelname)s | %(message)s',
        datefmt  = '%m/%d/%Y %H:%M:%S'
        )


def main():
    ''' Parse the arguments and start running what needs to be running '''

    parser = argparse.ArgumentParser()
    parser.add_argument(
            'dictionary', nargs='?', type=str, default='',
            help='Dictionary to use for translation. To translate from english to french, it should take the value enfr, for english to italian, enit, etc.'
            )
    parser.add_argument(
            'word', nargs='?', type=str, default='',
            help='Word to be translated'
            )
    parser.add_argument(
            '-l', '--list', action='store_true',
            help='Returns the list of available dictionaries.'
            )
    args = parser.parse_args()
    logging.info('Arguments parsed')

    dictionaries = get_dictionaries()
    if args.list:
        logging('Attempting to print the list of available dictionaries')
        print()
        print('**** Available dictionaries:')
        print(dictionaries.table)
        logging.info('Printed the list of available dictionaries')

    if args.word and args.dictionary:
        translate_word(args.dictionary, args.word)
    else:
        if not args.list:
            logging.info('User didn\'t pass the correct arguments. Displaying the help message and shutting down')
            print('Please enter a dictionary and a word.')
            print('\tEnter -l or --list to get a list of all available dictionaries.')
            print('Enter -h or --help for help.')


def get_dictionaries():
    ''' 
    Requests wordreference.com homepage and parse the list of availables
    dictionaries 
    '''

    url = 'http://www.wordreference.com'
    logging.info('Requesting {} for parsing'.format(url))
    r = requests.get(url)
    if r.status_code != 200:
        logging.info('Request failed with status {}'.format(r.status_code))
        return -1
    logging.info('Request for {} successful'.format(url))
    
    logging.info('Attempting to parse the html and extract the list of dictionaries')
    soup = BeautifulSoup(r.content, 'html.parser')
    options = soup.find_all('option')
    dictionaries = [ ['Key', 'Dictionary'] ]
    dictionaries += [ [option['id'], option.get_text()] for option in options 
            if option['id'][:2] != option['id'][2:4]      # No definition option
            and len(option['id']) == 4                 # No synonyms or conjugation option
            ]
    
    logging.info('List of dictionaries extracted')
    table = AsciiTable(dictionaries)
    return table


def translate_word(dictionary, word):
    ''' 
    Requests the page for the translation of "word" using the dictionary
    "dictionary".
    Print a formatted version of the response
    '''
    
    # Iniital checks
    if not isinstance(dictionary, str) or len(dictionary) != 4:
        raise TypeError('''The "dictionary" argument must be a string of length 4,
                with the first two letters being the acronym of the original
                language, and the last two letters, the acronym of the language
                you would like to translate to.''')
    if not isinstance(word, str):
        raise TypeError('The "word" argument must be a string (type {} passed)'.format(type(word)))
    
    # Building the url (and formatting it) and get the html from GET
    base_url = 'http://www.wordreference.com/'
    url = base_url + dictionary + '/' + word.replace(' ', '%20')

    logging.info('Requesting {} for parsing'.format(url))
    r = requests.get(url)
    if r.status_code != 200:
        logging.info('Request failed with status {}'.format(r.status_code))
        return -1
    logging.info('Request for {} successful'.format(url))

    # Parsing the html to extract the data
    # I kept it to what matters:
    #   * Original word/expression
    #   * Translation
    # Because who really cares if it is an intransitive verb or a noun?
    logging.info('Attempting to parse the html and extract the translations')
    soup = BeautifulSoup(r.content, 'html.parser')
    table_single_form = soup.find_all('table', {'class': 'WRD'})[0]
    try:
        data_single_form = parse_translation_table(table_single_form)
    except IndexError:
        logging.warning('The word passed doesn\'t have any translation')
        return -1

    logging.info('Translations extracted')
    # print the results in a pretty way
    print_results(word, data_single_form)


def parse_translation_table(table):
    '''
    Given the table of translations extracted with BeautifulSoup, returns
    a list of lists containing the various translations.
    '''

    data = [ ['Original Language', 'Translation'] ]

    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 3:
            cells[2].em.decompose()
            if cells[0].get_text(strip=True) == '':
                data[-1][1] += '\n{}'.format(cells[2].get_text())
            else:
                data += [[
                    cells[0].find('strong').get_text(),
                    cells[2].get_text()
                    ]]
    return data


def print_results(word, data_single_form):
    ''' Pretty print of the translation results '''

    print()
    print('**** Translations for {}:'.format(word))
    print(AsciiTable(data_single_form).table)
    print()

