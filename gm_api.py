import requests

class GM_Api:
  URL = 'http://gmapi.azurewebsites.net{}'

  def set_body(body):
    body['responseType'] = 'JSON'
    return body

  def post(route, body):
    resp = requests.post(
      GM_Api.URL.format(route),
      json=GM_Api.set_body(body)
    )
    json = resp.json()

    # deal with error handling later

    return json
