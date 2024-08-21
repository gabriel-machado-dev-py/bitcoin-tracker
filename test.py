from requests import Session
from requests.exceptions import ConnectionError, Timeout, RequestException
import json
from pprint import pprint



url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
parameters = {
  'id':'1'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'e65d6a30-ccce-49ac-82d2-a2532d2da75c'
}

session = Session()
session.headers.update(headers)

try:

  response = session.get(url, params=parameters)
  response.raise_for_status()  # Raise an HTTPError for bad responses
  data = json.loads(response.text)

  pprint(data['data']['1']['quote']['USD']['price'])

except (ConnectionError, Timeout, RequestException) as e:
  print(e)
