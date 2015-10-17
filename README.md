# India Post Tracking API

Simple no-captcha required API for tracking packages on the India Post website.

 - JSON API
 - No CAPTCHA
 - ISO formatted timestamps
 - Returns all events and available data for the given Item
 - Unofficial API. No liabilities
 - Requests are currently logged because [Heroku does not offer a way to disable logging](http://stackoverflow.com/questions/22582466/disable-heroku-router-logs). This data will never be sold or given to a third-party.

## How to use

Make a request to

    /track/:ITEM_ID

[Here](http://hurl.eu/views/6e49285668da0a89c765d89197fbbca6c37db896) is a sample response.

The API root url is <https://india-post-tracker-api.captnemo.in/>.

## Changelog

- Oct-2015: API Shifted from Heroku-US to Heroku-EU region because India Post was blocking
  requests for the us-east region, it seems.

## License

Licensed under the [MIT License](http://nemo.mit-license.org/)
