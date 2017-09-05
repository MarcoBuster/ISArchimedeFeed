# Copyright (c) 2017 Marco Aceti <mail@marcoaceti.it>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
from bs4 import BeautifulSoup

import config


def get_notices():
    r = requests.get(config.BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all('li', {"class": "widget widget_pasw2015_posts"})[0].find_all('li')
    notices = []
    for notice in results:
        notices.append({
                "title": notice.find('a').text.lstrip(),
                "date": notice.find('span', {'class': 'hdate'}).text.lstrip(),
                "url": notice.find('a').get('href'),
                "type": "notice",
             })

    return notices


def get_circulars():
    r = requests.get("http://www.isarchimede.gov.it")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all('li', {"class": "widget widget_pasw2015_circolari"})[0].find_all('li')
    circulars = []
    for circular in results:
        circulars.append({
                "title": circular.find('a').text.lstrip(),
                "date": circular.find('span', {'class': 'hdate'}).text.lstrip(),
                "url": circular.find('a').get('href'),
                "type": "circular",
            })

    return circulars


def get_more_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find('h2', {'class': 'posttitle'}).text
    content = soup.find('div', {'class': 'postentry'}).p.text
    author = soup.find('span', {'class': 'postauthor'}).text

    if author in content:
        content = ''

    if soup.find('div', {'class': 'members-access-error'}):
        return

    results = soup.find_all('li', {'class': 'post-attachment'})
    attachments = []
    for attachment in results:
        attachments.append({'url': attachment.a.get('href'), 'name': attachment.a.text, 'size': attachment.small.text})

    return {
        'title': title,
        'content': content,
        'author': author,
        'attachements': attachments
    }


def get_all():
    return get_notices() + get_circulars()
