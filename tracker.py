import json
from io import BytesIO

from international import InternationalTracker
import requests
from bs4 import BeautifulSoup
from dateutil import parser

from captcha import Captcha
from encoder import DateTimeEncoder

HOME_URL = "http://www.indiapost.gov.in/speednettracking.aspx"
CAPTCHA_URL = "http://www.indiapost.gov.in/captcha.aspx"
ROOT_URL = "http://www.indiapost.gov.in/"


class Tracker:
    # def __init__(self):
        # self.POST_DATA = {}

        # self.session = requests.Session()
        # home_response = self.session.get(HOME_URL)

        # dom = BeautifulSoup(home_response.content, "html.parser")

        # inputs = dom.find_all('input')

        # for input in inputs:
        #     if 'value' in input.attrs:
        #         self.POST_DATA[input.attrs['name']] = input.attrs['value']
        #     else:
        #         self.POST_DATA[input.attrs['name']] = None

        # self.captcha_url = dom.find(id="imgcap").attrs['src']

        # captcha_response = self.session.get(ROOT_URL + self.captcha_url)
        # captcha_file = BytesIO()
        # captcha_file.write(captcha_response.content)

        # code = Captcha(captcha_file).crack()

        # self.POST_DATA['txtCaptcha'] = code

    def track(self, id, international):
        if international:
            return InternationalTracker().track(id)
        details = {}
        self.POST_DATA['Txt_ArticleTrack'] = id
        response = self.session.post(HOME_URL, data=self.POST_DATA)
        dom = BeautifulSoup(response.content, "html.parser")

        general_details = dom.find(id="GridView1").findAll('td')

        if len(general_details) < 7:
            return None

        details['id'] = dom.find(id='Label1').text.strip()
        details['origin'] = general_details[0].text.strip()
        details['booking_date'] = parser.parse(general_details[1].text.strip())
        details['pincode'] = general_details[2].text.strip()
        details['tariff'] = general_details[3].text.strip()
        details['category'] = general_details[4].text.strip()
        details['destination'] = general_details[5].text.strip()
        details['delivery_date'] = general_details[6].text.strip()
        details['delivered'] = (details['delivery_date'] != 'Not Available')

        details['events'] = []

        events = dom.find(id='GridView2').findAll('tr')[1:]
        for tr in events:
            event = {}
            data = tr.findAll('td')
            event['date'] = parser.parse(data[0].text.strip() + ' ' + data[1].text.strip() + ' IST')
            event['office'] = data[2].text.strip()
            event['description'] = data[3].text.strip()

            details['events'].append(event)

        return details


if __name__ == '__main__':
    tracker = Tracker()
    print((json.dumps(tracker.track("EM870359070IN"), cls=DateTimeEncoder, sort_keys=True, indent=4,
                      separators=(',', ': '))))
