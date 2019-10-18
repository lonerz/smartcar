import pytest
from server import app
from gm_api import GM_Api as GM_Api

@pytest.fixture
def client():
  app.config['TESTING'] = True

  with app.test_client() as client:
    yield client

def test_vehicle_name(client, mocker):
  mock = mocker.patch('gm_api.GM_Api.post')
  mock.return_value = {
    'service': 'getVehicleInfo',
    'status': '200',
    'data': {
      'vin': {
        'type': 'String',
        'value': '123123412412'
      },
      'color': {
        'type': 'String',
        'value': 'Metallic Silver'
      },
      'fourDoorSedan': {
        'type': 'Boolean',
        'value': 'True'
      },
      'twoDoorCoupe': {
        'type': 'Boolean',
        'value': 'False'
      },
      'driveTrain': {
        'type': 'String',
        'value': 'v8'
      }
    }
  }

  resp = client.get('/vehicles/1234')
  mock.assert_called_with('/getVehicleInfoService', {'id': '1234'})
  assert(resp.json == {'vin': '123123412412', 'color': 'Metallic Silver', 'doorCount': 4, 'driveTrain': 'v8'})

def test_vehicle_doors(client, mocker):
  mock = mocker.patch('gm_api.GM_Api.post')
  mock.return_value = {
    'service': 'getSecurityStatus',
    'status': '200',
    'data': {
      'doors': {
        'type': 'Array',
        'values': [
          {
            'location': {
              'type': 'String',
              'value': 'frontLeft'
            },
            'locked': {
              'type': 'Boolean',
              'value': 'False'
            }
          },
          {
            'location': {
              'type': 'String',
              'value': 'frontRight'
            },
            'locked': {
              'type': 'Boolean',
              'value': 'True'
            }
          },
          {
            'location': {
              'type': 'String',
              'value': 'backLeft'
            },
            'locked': {
              'type': 'Boolean',
              'value': 'False'
            }
          },
          {
            'location': {
              'type': 'String',
              'value': 'backRight'
            },
            'locked': {
              'type': 'Boolean',
              'value': 'True'
            }
          }
        ]
      }
    }
  }

  resp = client.get('/vehicles/1234/doors')
  mock.assert_called_with('/getSecurityStatusService', {'id': '1234'})
  assert(resp.json == [
    {'location': 'frontLeft', 'locked': False},
    {'location': 'frontRight', 'locked': True},
    {'location': 'backLeft', 'locked': False},
    {'location': 'backRight', 'locked': True},
  ])

def test_vehicle_fuel(client, mocker):
  mock = mocker.patch('gm_api.GM_Api.post')
  mock.return_value = {
    'service': 'getEnergy',
    'status': '200',
    'data': {
      'tankLevel': {
        'type': 'Number',
        'value': '30.2'
      },
      'batteryLevel': {
        'type': 'Null',
        'value': 'null'
      }
    }
  }

  resp = client.get('/vehicles/1234/fuel')
  mock.assert_called_with('/getEnergyService', {'id': '1234'})
  assert(resp.json == {'percent': 30.2})

def test_vehicle_battery(client, mocker):
  mock = mocker.patch('gm_api.GM_Api.post')
  mock.return_value = {
    'service': 'getEnergy',
    'status': '200',
    'data': {
      'tankLevel': {
        'type': 'Number',
        'value': '15.2'
      },
      'batteryLevel': {
        'type': 'Null',
        'value': 'null'
      }
    }
  }

  resp = client.get('/vehicles/1234/battery')
  mock.assert_called_with('/getEnergyService', {'id': '1234'})
  assert(resp.json == {'percent': None})

def test_vehicle_engine(client, mocker):
  mock = mocker.patch('gm_api.GM_Api.post')
  mock.return_value = {
    'service': 'actionEngine',
    'status': '200',
    'actionResult': {
      'status': 'EXECUTED'
    }
  }

  resp = client.post('/vehicles/1234/engine', json={'action': 'START'})
  mock.assert_called_with('/actionEngineService', {'id': '1234', 'command': 'START_VEHICLE'})
  assert(resp.json == {'status': 'success'})

  mock.return_value = {
    'service': 'actionEngine',
    'status': '200',
    'actionResult': {
      'status': 'FAILED'
    }
  }

  resp = client.post('/vehicles/1234/engine', json={'action': 'STOP'})
  mock.assert_called_with('/actionEngineService', {'id': '1234', 'command': 'STOP_VEHICLE'})
  assert(resp.json == {'status': 'error'})

def test_errors(client, mocker):
  mock = mocker.patch('gm_api.GM_Api.post')
  mock.return_value = {'error': 'Vehicle id: 1000 not found.'}

  resp = client.get('/vehicles/1000')
  mock.assert_called_with('/getVehicleInfoService', {'id': '1000'})
  assert(resp.json == {'error': 'Vehicle id: 1000 not found.'})
