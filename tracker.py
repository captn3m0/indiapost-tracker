import json
from io import BytesIO

from urllib.parse import urlparse
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from encoder import DateTimeEncoder
from captcha import solve as captcha_solve
import urllib.request
import tempfile
import os

TRACKING_URL = "https://www.indiapost.gov.in/_layouts/15/DOP.Portal.Tracking/TrackConsignment.aspx"
ARTICLE_DETAILS_ID = "ctl00_PlaceHolderMain_ucOERControl_gvTrckMailArticleDtlsOER"
FORM_ID="aspnetForm"
TRACKING_ID_FIELD="ctl00$PlaceHolderMain$ucOERControl$txtOrignlPgTranNo"
CAPTCHA_FIELD="ctl00$PlaceHolderMain$ucOERControl$txtCaptcha"

class Tracker:
    def __init__(self):
        self.saved_data = None
        self.get_headers = {
          "User-Agent": "Mozilla",
          "Referer": TRACKING_URL
        }

        self.headers = dict({
          "X-Requested-With": "XMLHttpRequest",
          'content-type': "application/x-www-form-urlencoded"
        }, **self.get_headers)

    def captcha_update(self, data):
        self.POST_DATA = data

    def get_form_data(self):
        # Make a normal GET request on TRACKING URL
        response = requests.get(TRACKING_URL, headers = self.headers)
        dom = BeautifulSoup(response.content, "html.parser")

        captcha_details = {
            "url": dom.find(alt="Enter Security code in Text field").get('src'),
            "instructions": dom.find(id="ctl00_PlaceHolderMain_ucOERControl_lblCaptcha").text.strip()
        }

        post_data = {
            "__REQUESTDIGEST": dom.find(id="__REQUESTDIGEST").get('value'),
            "__EVENTVALIDATION": dom.find(id="__EVENTVALIDATION").get('value'),
            "__VIEWSTATE": dom.find(id="__VIEWSTATE").get('value'),
            "ctl00$ScriptManager": "ctl00$PlaceHolderMain$ucOERControl$upnlTrackConsignment|ctl00$PlaceHolderMain$ucOERControl$btnSearch",
            "ctl00$PlaceHolderMain$ucOERControl$btnSearch": "Search",
            "__VIEWSTATEGENERATOR": dom.find(id="__VIEWSTATEGENERATOR").get('value'),
            "__VIEWSTATEENCRYPTED": ""
        }

        return (post_data, captcha_details)

    def solve_captcha(self, details):

        # Prep
        url = urljoin(TRACKING_URL, details['url'])
        # print(url)
        if "Math" in url:
            extension = ".png"
        else:
            extension = ".gif"

        # Download
        captcha_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
        res = requests.get(url, headers=self.get_headers)
        captcha_file.write(res.content)

        # Close from here, so remaining pipeline can open it
        captcha_file.close()

        # Solve
        answer = captcha_solve(captcha_file.name, details["instructions"])
        os.remove(captcha_file.name)

        return answer

    def parse_html(self, content):
        details = {}
        dom = BeautifulSoup(content, "html.parser")

        try:
            general_details = dom.find(id=ARTICLE_DETAILS_ID).findAll('td')

            if (len(general_details) > 0):

                details = {'id': id,
                           'origin': general_details[0].text.strip(),
                           'booking_date': parser.parse(general_details[1].text.strip()),
                           'pincode': general_details[2].text.strip(),
                           'tariff': general_details[3].text.strip(),
                           'category': general_details[4].text.strip(),
                           'destination': general_details[5].text.strip(),
                           }
            if len(general_details) > 6:
                general_details['delivery_date'] = general_details[6].text.strip()
                details['delivered'] = details['delivery_date'] != 'Not Available'

            details['events'] = []

            events = dom.find(class_='responsivetable MailArticleEvntOER').findAll('tr')[1:]
            for tr in events:
                event = {}
                data = tr.findAll('td')
                event['date'] = parser.parse(data[0].text.strip() + ' ' + data[1].text.strip() + ' IST')
                event['office'] = data[2].text.strip()
                event['description'] = data[3].text.strip()
                details['events'].append(event)

            return details
        except Exception as e:
            # raise e
            return None

    def is_saved(self):
        return self.saved_data != None

    def track(self, id):

        if self.saved_data:
            data = self.saved_data
        else:
            data, captcha_details = self.get_form_data()

            # with open('/tmp/data.json', 'w') as f:
            #     f.write(json.dumps(data))

            # with open('/tmp/captcha.json', 'w') as f:
            #     f.write(json.dumps(captcha_details))

            data[CAPTCHA_FIELD] = self.solve_captcha(captcha_details)
            data[TRACKING_ID_FIELD] = id

            # with open('/tmp/data.json', 'w') as f:
            #     f.write(json.dumps(data))

        response = requests.post(TRACKING_URL, data=data, headers=self.headers)

        # with open('/tmp/debug.html', 'w+b') as f:
        #     f.write(response.content)

        details = self.parse_html(response.content)

        # If we broke the captcha, remember these details for future
        if details != None:
            self.saved_data = data
        # If we didn't, ensure that this data isn't saved any more
        # TODO: Only do this for failed captchas, and not
        # invalid tracking IDs
        elif self.saved_data == data:
            self.saved_data = None

        return details


