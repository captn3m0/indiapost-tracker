# India Post Tracking API

Simple no-captcha required API for tracking packages on the India Post website.

-   JSON API
-   No CAPTCHA
-   Returns all events and available data for the given Item
-   Unofficial API. No liabilities

## How to use

Make a request to

    /track/:ITEM_ID

### Sample Response

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

## Changelog

-   June 2018: API switched to `ipsweb.ptcmysore.gov.in` from `indiapost.gov.in` on [suggestion from @troysk704](https://twitter.com/troysk704/status/1010165300069715968)
-   Oct-2015: API Shifted from Heroku-US to Heroku-EU region because India Post was blocking
    requests for the us-east region, it seems.

## Credits

-   This is currently maintained by [Vatsal Shah](@hornedbull).
-   Thanks to Troy SK for telling me about <http://ipsweb.ptcmysore.gov.in/ipswebtracking/>

## License

Licensed under the [MIT License](http://nemo.mit-license.org/)
