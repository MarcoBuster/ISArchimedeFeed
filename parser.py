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


def get_circulars():
    r = requests.get(config.BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find('div', {"class": "postentry"}).find('div').find_all('div')
    circulars = []
    for result in results:
        if result.find('a'):
            circulars.append(result.find('a').get('href'))
    
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

