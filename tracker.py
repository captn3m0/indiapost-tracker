import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from dateutil import parser
from encoder import DateTimeEncoder

TRACKING_URL = "https://www.indiapost.gov.in/_layouts/15/DOP.Portal.Tracking/TrackConsignment.aspx"
ARTICLE_DETAILS_ID = "ctl00_PlaceHolderMain_ucOERControl_gvTrckMailArticleDtlsOER"


class Tracker:
    def __init__(self):
        self.POST_DATA = "ctl00%24ScriptManager=ctl00%24PlaceHolderMain%24ucOERControl%24upnlTrackConsignment%7Cctl00%24PlaceHolderMain%24ucOERControl%24btnSearch&__REQUESTDIGEST=0x0C129F9F4E6505B556DF4189ECC53D3265A1D02A736D8A4216234289B8A65B544389510F1103DBA949B4CD1C7B00E8A90237FEBC85B9798253B4AD9C4D14FE2B%2C12%20May%202019%2018%3A18%3A10%20-0000&__VIEWSTATE=LTMTJEN2p%2FY5gVLohrpnPr058t4%2FMKLhRoLhZ76mPox9pt7lStcu988vCK5dFlIiPTC3Y%2FkKEeLgNDNla4UYRN253ZJcdkvaihxvcSAwXn0%2Bogrzv4qknEm%2BfCY9Cqd1jvR5pP7A8kuzI4Ek7830VpXO%2FhAxEo4nlgqVyGKMErfBVTxHhdcMJGDl0yD7xVQa9CR8BHM9vmtBKWNDwRJJIjRv8j56yw%2FG4gOi16vtLSFJZyb2FmdriD3ZLeI8Psr3XTRRw2aoSHos6UUXg4DZuugVUngQg4Q6CAfr8BSXrpv0mT%2B%2B2srmu4A6oEUFnapIz17nyLRTYPP8G%2F%2BPB4L0XUCl996dF%2B2GKsWkQP6grfNJfzMtuhviNl2kdXlEuFFDPyeOL3AYaDc%2FXM5WRAf9Tq2yLHYlqNLRN6EHtR8j4F%2BWkH07pfXLQvYvby3fQJJrGZkdwQLAKrfPTkot5TYs2UiSYMwaPyvVhswevBK7Qsik58GCe3b0yHaqx7D1mzJYeT8lP58H4A8Ug12EQkjDja12GYu3gtO4bOLUy4s9AL1BWRYwFxdKSzRoVGtVcvNfXTxSQF80rtviQfUzvULR9edN9UzebiGvJgQz2%2Bz7KH4dXdKmhM3R9%2Bqwm%2BDHMB2e89Uo8HcZBU0dTVPwtY9JQXwMGPGA2HOV01VLxLUZkNWa2qr%2FFrmfi6NnfnrAJXsR1sdGTLVaCdCK0yNcL3gDjtBQjHHlsnCvUKUZJet4DExkkR1lVeZlqKX35t5UIwA4Qbm45rQRSPIf9MbGa27kmrJ%2FjiZ4OSoBvM0aT2jjrRJXyHaWzrw%2FS%2FTxy%2FldqnZFLKKhU5udmFEfSETfS6B3FGLhrXNMug4svnIfeAXeB69s9SPR4z2RTe8z23alMHJS5TUkmJokS5MYgWgkFsg3ZE1lONsLsXCMTdNnH3G3FRMtowUCPVcpYUTJJRqusz1r0Rjl6yEyrBFgugt%2BHGBWkBxDHmbfdXJEQEIfmCvgK5wqtwK4%2BWNv0ethmQPZfvw9EDqC%2BbrJ5K%2B8o5vVNuP5DQFS0edMPhYCpUp%2BjgUz2rGV9RgEP6Yi2hT6jNnLxuYT3QfV9J%2B%2Bn5Gr8jPdJiBSGWNXRNJT6x4Aoxq2DNpEC47nT0Zm3d8meWjkQAzMy0NBGu5WMgRG3Eau8s55YK1fV5vxWbJVvOMADm5eFlPfNHl31hGHyfdgMKHfRgAimcj%2Bp3VIOah5hMf%2F9vqTbJzgSqlQFwx5t6D7O8zC09B0fDpjLDY32bNepoA1MErD2qDrENO5qWNqm8kyUJsm7ruQ0ZiSEDka5cGTF8e%2FFbD0brypbpDy5VETwWoxX7f9hLgnvcO9mgRAlJ%2FvolRlqDZFv378WUGd1rVMBJdOzyaUH5LDhrG6u1j90xQzbRYuQB0xK8YhWyFK9ex2UQLEQiesUufpYXgwZ3z%2BEfJ6S6Igb%2BXZAaGV%2BbHPaOeZef1oBIkmUW20%2FQIyRMYecQxCNklB4czVrQemjnVDBjaEqWqkC7ao0yAONx21sggoJgNmlafZRHOT%2FlLMjC%2BfpZMj5HkLnMH3as1A4e8zKAgf5u0BbqQ8lsCBaB8pe%2Fmb3l%2FvdfSjDtlUNImDfAXJQewB5xHzBxRA9a2XRP67%2FbN4tQ5QyJRzctgD8kdIGBJoXHnZ6DDvOvqb9XE78JnO5Fth8eflr9k0NB9L1lfHtsemIgm%2BsVFX9RaNBO4NmzT16PYws085ykhn9u3Hfntqv5Hh2ReGPuZ2Ypa5UmLKLC0GXXxeUwXytIYd14M990rlmFER%2FyXGXYbO7SlLnQFOV%2FfLsNNk0HTkroHFwo5T2v8kKSZbVCtsOm7l45nCkgZB8jDDVL%2BQ1X19rnf5FxPfTG6c8xZTKLH6027Ikh1Yw8IHG4igbRuaAIOZ0v2b80h1%2FST2Tda9qMY8QtTNRJfKFe3%2F7Dhw6iz6b%2FIZ2Q%2FKoVBUK8aSQz2UrbjNHaYGdMkhCkyoP7WNh6WVe94%2BwpMuL3KaN0xjhIDSPTbnpMDhJUI%2B5Ci%2BRcG8lz8TWy5qZyKe%2Fh6QcYMf7xZ0uuFtnNbuSPbd90ZdkMivMX3HqJhLQTmbVWkB2dLiuEqp0JUHVuF6OAOhuzlULP0vpfcfyeFmcDUfqLhsB3ff8ew8taMSlI4Wf4RY5DoFmVPp69xUy2Q6abEmd2kZN6Pyt%2FCgi3%2FbkQx7Niw65zVzjow9bH1rauJN%2BMPvLGXIoVqgPboYF%2BihUkhjmP9mld6V5dNCVVQWiJ9vAB3c6PF2MLdk3rhixhcY91q31k76S%2F40BKt%2B1TF3p2o6IOpdo4xeC1CK3q3vxbfWXyEVr5pOdaZLFMF2xElCgmKxVWaUFXxFhw35G%2F%2FJ6KzXW0MFubDhYU%2BD9OP8ZndMI%2FX6%2BCMT997Uyhs7ZCuVHCy5o41S3%2Bh3ay%2FICNUf0b1ZGtt%2BX32rqlEv9D9otOu2eK3zXxfEwnPBulJdQgXAYwVepqdYW6HaXGujS6GEdaPKcFr28bWKfUEh0sA8dOwFFiboBiHSXuhdg0jKHgEV6Me1uH%2BH3EBr1h1ptvjE70hpt6dCkFx01F8afUhK4iRh50MgL%2BUlc9z11%2FTry5OKkXvkCNQegmKVkKmNZZBCjyon6dKu7RsmhbpSmTf%2FmlwUjOBAzf07On0C5wKZVZh21yZhqk%2BjjSyESVNOnWNP0SRbwTYmEbFNvLDHFUlXubmumlLOheEApDS8OdEplr4Mg82n5NiZQP1DSt9SoftbvIfppx9qZhsHNxYDNYfJPmyKugGnIqtGsfGy1KEqkAa%2BzU00OIi2qo9if9FDDZHz4nn2%2FPhutW2C3eIbijjiZHvoVbBGF%2BEbwrlsONYxIs4ZFiiSBmhvetDYkaJe87CL9nc%2F5F2s9aNSnfUARRi8ixTFD%2BHBWA%3D%3D&__VIEWSTATEGENERATOR=BA91C67B&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=5eefHwdGHeMKpu%2F7Z%2FrkAtbcnu5%2BhSbpYqPHlIedBwKXHebDAIAO2pniexdp84O8GkmOvWEPI6SBudzZJKGoIonceDkw4WsSEjJL5IBre67wMS4fUF7MYF94GsyUPAJ5yBQBiUapbyC43XHFdNjxt2h4azGeCpaupsLfdgtaTnGyNVZQHfMY5K7KurfnCVUNuwIEIjnxOJEWXwN%2B8ZFlXhHoHQqezt%2FL92IrCURwjPk59ermz%2BWJ8w3hsTkq7e8V%2FGtjVCKsnkt52cNS7k%2FLAg%3D%3D&ctl00%24PlaceHolderMain%24ucOERControl%24txtOrignlPgTranNo=EO430454377IN&ctl00%24PlaceHolderMain%24ucOERControl%24txtCaptcha=7f1658&ctl00%24PlaceHolderMain%24ucOERControl%24btnSearch=Search"

    def track(self, id):
        details = {}
        self.POST_DATA = self.POST_DATA.replace("EO430454377IN", id)
        headers = {
          "User-Agent": "Mozilla",
          "Referer": "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx",
          "X-Requested-With": "XMLHttpRequest",
          'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.post(TRACKING_URL, data=self.POST_DATA, headers = headers)
        dom = BeautifulSoup(response.content, "html.parser")

        try:
            general_details = dom.find(id=ARTICLE_DETAILS_ID).findAll('td')
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
            return None
