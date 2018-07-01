# India Post Tracking API

[![](https://images.microbadger.com/badges/version/captn3m0/indiapost-tracker:latest.svg)](https://microbadger.com/images/captn3m0/indiapost-tracker:latest) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](http://www.wtfpl.net/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Simple no-captcha required API for tracking packages on the India Post website.

-   JSON API
-   No CAPTCHA
-   Returns all events and available data for the given Item
-   Unofficial API. No liabilities

## How to use

Make a request to

    /track/:ITEM_ID

If you know that a package is international, you can force a different "international-only" response
by using `/track/:ITEM_ID?international=true`. This gives you a few extra details about the country

### Sample Response (/track/:ITEM_ID)

```json
{
    "booking_date": "2018-06-15T00:00:00",
    "category": "SPA",
    "delivered": true,
    "delivery_date": "19/06/2018",
    "destination": "Faridabad Sector 7 S.O",
    "events": [
        {
            "date": "2018-06-19T16:42:55+05:30",
            "description": "Item delivered",
            "office": "Faridabad Sector 7 S.O"
        },
        {
            "date": "2018-06-16T08:42:18+05:30",
            "description": "Bag Despatched to ICH FARIDABAD",
            "office": "DELHI RMS"
        },
        {
            "date": "2018-06-16T07:05:40+05:30",
            "description": "Bag Received",
            "office": "DELHI RMS"
        },
        {
            "date": "2018-06-16T03:24:33+05:30",
            "description": "Bag Despatched to DELHI RMS",
            "office": "BNPL SP Hub NEW DELHI"
        },
        {
            "date": "2018-06-16T02:06:10+05:30",
            "description": "Item Bagged for ICH FARIDABAD",
            "office": "BNPL SP Hub NEW DELHI"
        },
        {
            "date": "2018-06-15T20:41:03+05:30",
            "description": "Item Booked",
            "office": "BNPL SP Hub NEW DELHI"
        }
    ],
    "id": "PP116215523IN",
    "origin": "BNPL SP Hub NEW DELHI",
    "pincode": "121006",
    "tariff": "35.00"
}
```

## Sample API Response (/track:ITEM_ID?international=true)

```json
{
    "booking_date": "9/27/2014 4:22:00 PM",
    "delivered": true,
    "delivery_date": "9/29/2014 7:57:00 AM",
    "destination": "2150",
    "destination_country": "Australia",
    "events": [
        {
            "country": "Australia",
            "location": "SYDNEY EMS",
            "mail_category": "A",
            "next_office": "ISC NEW YORK NY (USPS)",
            "time": "9/27/2014 4:22:00 PM",
            "type": "Receive item at office of exchange (Inb)"
        },
        {
            "country": "Australia",
            "location": "AUMXBT",
            "mail_category": "A",
            "next_office": "-",
            "time": "9/29/2014 7:57:00 AM",
            "type": "Receive item at delivery office (Inb)"
        },
        {
            "country": "Australia",
            "location": "2150",
            "mail_category": "A",
            "next_office": "-",
            "time": "9/29/2014 7:57:00 AM",
            "type": "Deliver item (Inb)"
        }
    ],
    "id": "ED123456789IN",
    "origin": "SYDNEY EMS",
    "origin_country": "Australia"
}
```

The API root url is <https://india-post-tracker-api.captnemo.in/>.

## Docker

You can run this as a docker container as well:

`docker run --detach --publish 3000:3000 captn3m0/indiapost-tracker` and access the service locally using http://localhost:3000

## Changelog

-   June 2018: International support added using `ipsweb.ptcmysore.gov.in` [suggestion from @troysk704](https://twitter.com/troysk704/status/1010165300069715968)
-   Oct-2015: API Shifted from Heroku-US to Heroku-EU region because India Post was blocking
    requests for the us-east region, it seems.

## Credits

-   This is currently maintained by [Vatsal Shah](@hornedbull).
-   Thanks to Troy SK for telling me about <http://ipsweb.ptcmysore.gov.in/ipswebtracking/>

## License

Licensed under the [MIT License](http://nemo.mit-license.org/)
