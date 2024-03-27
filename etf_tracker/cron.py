from django_cron import CronJobBase, Schedule
from bs4 import BeautifulSoup
import requests
import dateparser


class CronJob(CronJobBase):
    RUN_EVERY_MINS = 0.1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'clean'    # a unique code

    def do(self):
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        html = requests.get('https://www.bitcoinstrategyplatform.com/etfs', headers=headers).text

        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table')

        headers = table.findAll('th')
        rows = table.findAll('td')
      
        # for row in headers[-8:]:
        #     print(dateparser.parse(row.contents[0]))
        #     print("\n")

        # for row in rows:
        #     print(row)
        #     print("\n")

        print(table)