"""Scrape the website and build the database."""

import sqlite3
import atexit
import urllib.parse as urlparse
import datetime

import requests
from bs4 import BeautifulSoup


# connect to database
db = sqlite3.connect('../strongbad_emails.db')


def close_out():
    """Auto commit and close the connection on program exit."""
    db.commit()
    db.close()
    print('Closed DB.')


atexit.register(close_out)

# clear out database and set up tables fresh.
with open('init-data-model.sql', 'r') as f:
    db.executescript(f.read())


def get(*args, **kwargs):
    """Make GET requests more convenient.

    - Do retries on bad HTTP responses
    - Timeouts between requests
    """
    for attempt in range(1, 10):
        res = requests.get(*args, **kwargs)
        if res.status_code == 200:
            break
        elif attempt == 10:
            res.raise_for_status()
        else:
            time.sleep(2)
    return res


res = get('http://www.hrwiki.org/wiki/Strong_Bad_Email')
soup = BeautifulSoup(res.content, 'lxml')

# get all tables of emails
tables = soup.find_all('table', {'class': 'emaillinks'})
tables += soup.find_all('table', {'class': 'emailgreenlinks'})

# iterate on tables
for table in tables:

    # get URLs from each table
    urls = [i for i in table.find_all('a') if i['href'].startswith('/wiki/')]

    # iterate on email URLs
    for url in urls:

        print(f'''RUNNING: {url['href']}''')

        # compose the email url
        hrwiki_url = urlparse.urljoin('http://www.hrwiki.org', url['href'])

        # get the email soup
        soup = BeautifulSoup(get(hrwiki_url).content, 'lxml')

        # get email properties
        email_id = [
            int(i.find('td').text.strip()[18:])
            for i in soup.find_all('table')
            if i.find('td').text.strip().startswith('Strong Bad Email #')
        ][0]

        homestarrunner_url = (
            f'http://homestarrunner.com/sbemail{email_id}.html'
        )

        email_title = soup.find('h1', {'id': 'firstHeading'}).text.strip()

        email_message = (
            soup.find('blockquote', {'class': 'email'})
            .text.strip()
        )

        if email_message.lower().startswith('subject: '):
            email_message = '\n'.join(email_message.split('\n')[1:])

        sql = '''
            INSERT INTO email
            (
                'id',
                'title',
                'message',
                'homestarrunner_url',
                'hrwiki_url'
            )
            VALUES (?, ?, ?, ?, ?)
        '''

        params = [
            email_id,
            email_title,
            email_message,
            homestarrunner_url,
            hrwiki_url
        ]
        db.execute(sql, params)
