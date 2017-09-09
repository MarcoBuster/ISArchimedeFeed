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

import sqlite3

import botogram

import config
import parser

bot = botogram.create(config.TOKEN)
conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS urls(url TEXT);')


def check_and_send():
    results = parser.get_all()
    for result in results:
        c.execute('SELECT EXISTS(SELECT 1 FROM urls WHERE url=? LIMIT 1);', (result['url'],))
        exists = c.fetchone()[0]
        if not exists:
            document = parser.get_more_info(result['url'])
            if not document:
                continue

            text = (
                "{emoji} <b>{title}</b>"
                "{content}"
                "\n{attachements}"
                .format(
                    emoji='📄' if result['type'] == 'notice' else '📑',
                    title=document['title'],
                    content='\n' + document['content'] if document['content'] else '',
                    attachements=('\n📎 <b>Allegati</b>' if document['attachements'] else '') + ''.join(
                        "\n➖ <a href=\"{url}\">{name}</a>".format(url=x['url'], name=x['name'])
                        for x in document['attachements']
                    ) if document['attachements'] else ''
                )
            )
            for chat_id in config.CHAT_IDS:
                bot.chat(chat_id).send(text, syntax="HTML")

            c.execute('INSERT OR IGNORE INTO urls VALUES(?);', (result['url'],))
            conn.commit()


if __name__ == "__main__":
    check_and_send()
