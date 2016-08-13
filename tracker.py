import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from dateutil import parser

from captcha import Captcha
from encoder import DateTimeEncoder

CAPTCHA_URL = "http://www.indiapost.gov.in/captcha.aspx"
ROOT_URL = "http://www.indiapost.gov.in/"


class Tracker:
    HOME_URL = str()

    def __init__(self, id):
        self.id = id
        self.POST_DATA = {}
        self.HOME_URL = self.getUrl(id)
        self.session = requests.Session()
        home_response = self.session.get(self.HOME_URL)
        dom = BeautifulSoup(home_response.content, "html.parser")

        inputs = dom.find_all('input')

        for input in inputs:
            if 'value' in input.attrs:
                self.POST_DATA[input.attrs['name']] = input.attrs['value']
            else:
                self.POST_DATA[input.attrs['name']] = None

        self.captcha_url = dom.find(id="imgcap").attrs['src']

        captcha_response = self.session.get(ROOT_URL + self.captcha_url)
        captcha_file = BytesIO()
        captcha_file.write(captcha_response.content)

        code = Captcha(captcha_file).crack()

        self.POST_DATA['txtCaptcha'] = code


    def trackSpeedPost(self):
        id = self.id
        details = {}
        self.POST_DATA['Txt_ArticleTrack'] = id
        response = self.session.post(self.HOME_URL, data=self.POST_DATA)
        dom = BeautifulSoup(response.content, "html.parser")
        general_details = dom.find(id="GridView1").findAll('td')

        if len(general_details) < 7:
            return None
        details['id'] = dom.find(id='Label1').text.strip()
        details['origin'] = general_details[0].text.strip()
        details['booking_date'] = parser.parse(
            general_details[1].text.strip(), dayfirst=True)
        details['pincode'] = general_details[2].text.strip()
        details['tariff'] = general_details[3].text.strip()
        details['category'] = general_details[4].text.strip()
        details['destination'] = general_details[5].text.strip()
        details['delivery_date'] = general_details[6].text.strip()
        details['delivered'] = (details['delivery_on'] != 'Not Available')

        details['events'] = []

        events = dom.find(id='GridView2').findAll('tr')[1:]
        for tr in events:
            event = {}
            data = tr.findAll('td')
            event['date'] = parser.parse(
                data[0].text.strip() +
                ' ' +
                data[1].text.strip() +
                ' IST',
                dayfirst=True)
            event['office'] = data[2].text.strip()
            event['description'] = data[3].text.strip()

            details['events'].append(event)

        return details

    def trackRegisteredPost(self):
        id = self.id
        details = {}
        self.POST_DATA['Txt_ArticleTrack'] = id
        response = self.session.post(self.HOME_URL, data=self.POST_DATA)
        dom = BeautifulSoup(response.content, "html.parser")
        general_details = dom.find(id="GridView1").findAll('td')

        if len(general_details) < 7:
            return None
        details['id'] = dom.find(id='Lbl_Track1').text.strip()
        details['origin'] = general_details[0].text.strip()
        details['booking_date'] = parser.parse(
            general_details[1].text.strip(), dayfirst=True)
        details['destination'] = general_details[2].text.strip()
        details['tariff'] = general_details[3].text.strip()
        details['category'] = general_details[4].text.strip()
        details['delivered_at'] = general_details[5].text.strip()
        details['delivery_date'] = general_details[6].text.strip()
        details['delivered'] = (details['delivery_on'] != 'Not Available')

        details['events'] = []

        events = dom.find(id='GridView2').findAll('tr')[1:]
        for tr in events:
            event = {}
            data = tr.findAll('td')
            event['date'] = parser.parse(
                data[0].text.strip() +
                ' ' +
                data[1].text.strip() +
                ' IST',
                dayfirst=True)
            event['office'] = data[2].text.strip()
            event['description'] = data[3].text.strip()

            details['events'].append(event)

        return details

    def track(self):
        if self.id[0] == "E":
            return self.trackSpeedPost()
        elif self.id[0] == "R":
            return self.trackRegisteredPost()

    def getUrl(self, id):
        if self.id[0] == "E":
            return "http://www.indiapost.gov.in/speednettracking.aspx"
        elif self.id[0] == "R":
            return "http://www.indiapost.gov.in/rnettracking.aspx"


if __name__ == '__main__':
    tracker = Tracker("EM870359070IN")
    print(
        json.dumps(
            tracker.track(),
            cls=DateTimeEncoder,
            sort_keys=True,
            indent=4,
            separators=(
                ',',
                ': ')))
