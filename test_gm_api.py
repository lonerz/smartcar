import pytest
import requests
from gm_api import GM_Api as GM_Api

def test_post(mocker):
  mock = mocker.patch('requests.post')
  def json():
    return 'this is a mock'
  mock.return_value.json = json

  resp = GM_Api.post('/getVehicleInfoService', {'id': '1234'})
  mock.assert_called_with('http://gmapi.azurewebsites.net/getVehicleInfoService', json={'id': '1234', 'responseType': 'JSON'})
  assert(resp == 'this is a mock')
