import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from dateutil import parser
from encoder import DateTimeEncoder

TRACKING_URL = "https://www.indiapost.gov.in/_layouts/15/DOP.Portal.Tracking/TrackConsignment.aspx"
ARTICLE_DETAILS_ID = "ctl00_PlaceHolderMain_ucOERControl_gvTrckMailArticleDtls"


class Tracker:
    def __init__(self):
        self.POST_DATA = {
            "__VIEWSTATE": "pW37hBUqyhnv3HPmhysIDIm29rE9VueSxrSMY5xkDSpE5XGO+gcNyQFHNOzQoCBPqmQgBsnbPe1xZhmkcBFVxkOtLSZF6HAlDW/NEQvycp0nUMfzkNQBev4rh90b1FF8rRYppfhtz1f6m8AoVxAVUA1bVaL8+Vpu7MKbAEHJ+wFkpv77I5CqKSnxGSDAyidk3e0he2rdcSNljT/tljA/eFoqivOUCYz7Ayvb2KXXHV40IG/37AHZQDI1k9y/qZ6DEDY+LT/iK/hVayvw5h7LxFqwNKHGlvGuMmlreuPBpEXhFiBIXdeuVrVejdILcQsk7pUVOiyPOC4fb4PlMkWLd+nZl2v89BDpaD0RrGt8kdy9w64q2mlxCtVq3gVdN1942Dkc90lzQ8ou2cK4gk0nJ2ApPikWA6yPta6JnQdkGQsO+5u5EsNOcIB2BWR8bKgtNQRHt4VCSNg8Vit3FzlVC3+PB2aJo0KEVmGYnFHV/Na3XVkFgSWhgiS/WvvCIS7r5RRw+0ps8ri9zh5qZcQyY0g70hIrSqxV+6MF7YjL80tYDKXv9tkrOLgkDiWdGhIk6GQSFvZdjJUfezVmc3R1gLJGnXaf//595FSYbBA2GUvoFSsecgBZ8IY0KD6aQ2j0tm7gPryJsdxf7443r9s/el4WynG7hSKyY0FLq/h5HRK/+rvIKPbmAadt8xnlhU0a+H4HTopx068Vxu8Mp8YdGQVB+OI8ZKNS9MlaLKmUj310pWyNzLXhfqbtGXFVePb6QF2ymMTGT3uW8UyYd1NlUVOu9bfposaD0pDVmj7RY4PtzCONZiOiQnAHCtbdRvjAYiavTGzac4TI5cXGLgKQaJuP6idZzyGkDBWZrT9ycKkb9+Qfc5ItveCjyhRsS0Wn8ART3ujpVHECSYIx/3/0U/PAgcavY6HntoJkhRdSJc6+sC0qgHvEhpqjep6MrqYbHKZ4FZuknHThrxhA9vaEYmQDBl2CJ4Z2n0QLrq6z6F5nSkyh0G1Ms6hnLvaoagXtFH5LzuTHy6Fn1la7kCZ1TpQsAFXKLPD+3TcEG7xPG7QQ4vAum6WqnubT9PeM3xXrmNEgziw2GJgOfJo+6QUxlEe1LzutLorNHGLC9lxwcC2AiyxojlU1y3h0KuNSE9Ti+t7JZR4edAACNqqWh/QCjypt4e1Fe/gMMBvcAP5iIYSyeHu1JrYt5bdSduTAG0Bq+jeo6U43ylMgTVLranV2fph2myR3mPovuI8yUiy4tWul8YMpT8kmwMWnmIHdDds8cMHChpNHbisY6zD5VnIKKYCe53d1km+HYa4QDW+Zbf0iokArIFAeaSWMmywMPaOD3jcRdCq5BM22wm50l6ZC0yLm+g96QncAHI9iIlPNWoT7Lj4dOR57eR6dvM9lLe4sTr8nXP81JghbpvC7OcA98VCZnkdgmRQ3FNM3zS8XRhvQ7hjUClINDao+8gZsAnVJ3Y1BphOQDROWdRPthTDWMDU8llCzouKHN3bATdzqcUfCff3GvKy8G8C4ulSvcwH5z+7XldVLBoZcCSkxLJn7qllbK7nXvgepyr2bgwnau+M44qrq+X2VoJmlZ58Y4HeKNBfavJDP0pjFxfvc9co7j6ub0k74yiv0MoeMOL7NlBgV8LUdVjLP2aYcOCPZ4PIIeibhu8rUIPDYX7ShEB+uYr0QFGilrZ9iYtwKqKxOMrsCkeqtYU81noZja23seFDThmaDJ5sNz3S4xLNx2L115RoDsEfwqWXYFt5fE0drR7cXkE5Pa1/1P5U/8kBOh/k6SZjBJ8os3zp57SeriNgUDv9mrbf6aGWCHBgc4uNGzHBjv6g+KEYK96Sx2Z1eX0ZP",
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": "QoGNrZX5GdTk7GfKERTyHOYHEuS0eeDtGieHuZYO/hs5mM8KacgsDou6eDmCWS5TkZqlaoTsf3LgSs1AXVkTzSJxNKqGUkb8EjXNhpHwhB1+34V3/psFqFnSyVqODOs45xCDsjt5BPwcpCM/IYGzY0UvVViJAlrU4kcxwI21IZy6Z3DMjtIl+78zbrrNPdY6y+ebhanMCSqYxVxjEp+Jr87+hg2d5QqHnrLm9NlkmL8=",
            "ctl00$PlaceHolderMain$ucOERControl$txtOrignlPgTranNo": "PP116215523IN",
            "ctl00$PlaceHolderMain$ucOERControl$txtCaptcha": "d9067d",
            "ctl00$PlaceHolderMain$ucOERControl$btnSearch": "Search"
        }

    def track(self, id):
        details = {}
        self.POST_DATA["ctl00$PlaceHolderMain$ucOERControl$txtOrignlPgTranNo"] = id
        response = requests.post(TRACKING_URL, data=self.POST_DATA)
        dom = BeautifulSoup(response.content, "html.parser")

        try:
            general_details = dom.find(id=ARTICLE_DETAILS_ID).findAll('td')
        except Exception as e:
            return None

        if len(general_details) < 7:
            return None

        details = {'id': id,
                   'origin': general_details[0].text.strip(),
                   'booking_date': parser.parse(general_details[1].text.strip()),
                   'pincode': general_details[2].text.strip(),
                   'tariff': general_details[3].text.strip(),
                   'category': general_details[4].text.strip(),
                   'destination': general_details[5].text.strip(),
                   'delivery_date': general_details[6].text.strip(),
                   'delivered': (details['delivery_date'] != 'Not Available'),
                   }

        details['events'] = []

        events = dom.find(class_='responsivetable MailArticleEvnt').findAll('tr')[1:]
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
    print((json.dumps(tracker.track("PP116215523IN"), cls=DateTimeEncoder, sort_keys=True, indent=4,
                      separators=(',', ': '))))
