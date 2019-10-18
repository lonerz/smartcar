import pytest
import requests
from gm_api import GM_Api as GM_Api

def test_post_success(mocker):
  mock = mocker.patch('requests.post')
  def success_json():
    return {'status': '200', 'data': 'this is a mock'}
  mock.return_value.json = success_json

  resp = GM_Api.post('/getVehicleInfoService', {'id': '1234'})
  mock.assert_called_with('http://gmapi.azurewebsites.net/getVehicleInfoService', json={'id': '1234', 'responseType': 'JSON'})
  assert(resp == {'status': '200', 'data': 'this is a mock'})

def test_post_fail(mocker):
  mock = mocker.patch('requests.post')
  def fail_json():
    return {'status': '404', 'reason': 'Vehicle id: 1000 not found.'}
  mock.return_value.json = fail_json 

  resp = GM_Api.post('/getVehicleInfoService', {'id': '1000'})
  mock.assert_called_with('http://gmapi.azurewebsites.net/getVehicleInfoService', json={'id': '1000', 'responseType': 'JSON'})
  assert(resp == {'error': 'Vehicle id: 1000 not found.'})
