import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup

TRACKING_URL = "http://ipsweb.ptcmysore.gov.in/ipswebtracking/IPSWeb_item_events.aspx"


class InternationalTracker:

    def track(self, id):
        details = {
            'delivered': False,
            'id': id
        }
        response = requests.get(TRACKING_URL, params={'itemid': id})

        dom = BeautifulSoup(response.content, "html.parser")

        if not dom.find(id="200"):
            return None

        events = dom.find(id="200").findAll('tr')
        details['events'] = []

        for tr in events:
            event = {}
            klass = tr.get('class')
            data = tr.findAll('td')

            if (klass == ['tabl1'] or klass == ['tabl2']) and len(data) >= 6:
                event = {
                    'time': data[0].text.strip(),
                    'country': data[1].text.strip(),
                    'location': data[2].text.strip(),
                    'type': data[3].text.strip(),
                    'mail_category': data[4].text.strip(),
                    'next_office': data[5].text.strip(),
                }

                if 'Deliver item' in event['type']:
                    details['delivered'] = True
                    details['delivery_date'] = event['time']
                    details['destination'] = event['location']
                    details['destination_country'] = event['country']

                if 'Receive item' in event['type'] and 'origin' not in details:
                    details['origin'] = event['location']
                    details['origin_country'] = event['country']
                    details['booking_date'] = event['time']

                details['events'].append(event)

        return details


if __name__ == '__main__':
    tracker = Tracker()
    print((json.dumps(tracker.track("EE123456789IN"),  sort_keys=True, indent=4,
                      separators=(',', ': '))))
