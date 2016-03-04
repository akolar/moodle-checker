#!/bin/env python

import os
import argparse
import time

import requests
from bs4 import BeautifulSoup
from najdisi_sms import SMSSender


def login(session, domain):
    url = 'https://{}/login/index.php'.format(domain)

    if 'MOODLE_CREDENTIALS' in os.environ:
        username, password = os.environ['MOODLE_CREDENTIALS'].split(':', maxsplit=1)
    else:
        username, password = 'guest', 'guest'

    response = session.post(url, allow_redirects=True,
                            data={'username': username, 'password': password})

    if response.url == url:
        raise ValueError('Wrong username or password')


def notify(phone_number):
    if phone_number and ('NAJDISI_CREDENTIALS' in os.environ):
        username, password = os.environ['NAJDISI_CREDENTIALS'].split(':', maxsplit=1)
        sms = SMSSender(username, password)
        sms.send(
            phone_number,
            'Results are up :)'
        )

    print('\n Results are up :)')


parser = argparse.ArgumentParser(description='tool for checking whether the '
                                 'contents of a Moodle classroom has changed.')
parser.add_argument('domain',
                    help='domain of the moodle classroom (e.g. ucilnica.fmf.uni-lj.si)')
parser.add_argument('id', type=int,
                    help='id of the class')
parser.add_argument('--timeout', type=int, default=180,
                    help='seconds between sequential refreshes [default: 180]')
parser.add_argument('--phonenumber',
                    help='phone number for receiving notifications')
args = parser.parse_args()

url = 'https://{}/course/view.php?id={}'.format(args.domain, args.id)
print('Working on: {}'.format(url))
print('SMS notifications: {}'.format(args.phonenumber and
                                     ('NAJDISI_CREDENTIALS' in os.environ)))

session = requests.Session()
login(session, args.domain)
old_content = None
old_messages = None

while True:
    response = session.get(url)
    try:
        bs = BeautifulSoup(response.text, 'html.parser')
        content = bs.find(class_='course-content').get_text()
        messages = bs.find(class_='block_news_items block').get_text()
    except:
        if response.url.find('enrol') != -1:
            raise RuntimeError('Guests cannot view this course')
        login()
        continue

    if old_content and ((old_content != content) or (old_messages != messages)):
        notify(args.phonenumber)
        break
    else:
        old_content = content
        old_messages = messages
        print('[{}] Refreshed webpage; nothing new'.format(time.strftime("%H:%M:%S")))
        time.sleep(args.timeout)
