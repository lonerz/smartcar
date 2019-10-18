from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from gm_api import GM_Api

app = Flask(__name__)
api = Api(app)

# add request parser for post requests
parser = reqparse.RequestParser()
parser.add_argument('action', required=True, help='Need an action')

class Vehicle_Name(Resource):
  URL = '/getVehicleInfoService'

  '''
  {
    "vin": "1213231",
    "color": "Metallic Silver",
    "doorCount": 4,
    "driveTrain": "v8"
  }
  '''

  def body(id):
    return {'id': id}

  def parse_response(data):
    json = {}
    json['vin'] = data.get('vin').get('value')
    json['color'] = data.get('color').get('value')
    json['doorCount'] = 4 if data.get('fourDoorSedan').get('value') == 'True' else 2
    json['driveTrain'] = data.get('driveTrain').get('value')
    return json

  def get(self, id):
    payload = GM_Api.post(self.URL, Vehicle_Name.body(id))
    data = payload.get('data')
    return Vehicle_Name.parse_response(data)

class Vehicle_Doors(Resource):
  URL = '/getSecurityStatusService'

  '''
  [
    {
      "location": "frontLeft",
      "locked": true
    },
    {
      "location": "frontRight",
      "locked": true
    },
    {
      "location": "backLeft",
      "locked": true
    },
    {
      "location": "backRight",
      "locked": false
    }
  ]
  '''

  def body(id):
    return {'id': id}

  def parse_response(data):
    values = data.get('doors').get('values')
    doors = {}

    for door in values:
      doors[door.get('location').get('value')] = door.get('locked').get('value') == 'True'

    json = []
    for location in ['frontLeft', 'frontRight', 'backLeft', 'backRight']:
      json.append({
        'location': location,
        'locked': doors[location],
      })

    return json

  def get(self, id):
    payload = GM_Api.post(self.URL, Vehicle_Doors.body(id))
    data = payload.get('data')
    return Vehicle_Doors.parse_response(data)

class Vehicle_Fuel(Resource):
  URL = '/getEnergyService'

  '''
  {
    "percent": 30.2
  }
  '''

  def body(id):
    return {'id': id}

  def parse_response(data):
    json = {}
    json['percent'] = float(data.get('tankLevel').get('value'))
    return json

  def get(self, id):
    payload = GM_Api.post(self.URL, Vehicle_Fuel.body(id))
    data = payload.get('data')
    return Vehicle_Fuel.parse_response(data)

class Vehicle_Battery(Resource):
  URL = '/getEnergyService'

  '''
  {
    "percent": 50.3
  }
  '''

  def body(id):
    return {'id': id}

  def parse_response(data):
    json = {}
    json['percent'] = float(data.get('batteryLevel').get('value'))
    return json

  def get(self, id):
    payload = GM_Api.post(self.URL, Vehicle_Battery.body(id))
    data = payload.get('data')
    return Vehicle_Battery.parse_response(data)

class Vehicle_Engine(Resource):
  URL = '/actionEngineService'

  '''
  {
    "status": "success|error"
  }
  '''

  def body(id, action):
    return ({
      'id': id,
      'command': 'START_VEHICLE' if action == 'START' else 'STOP_VEHICLE',
    })

  def parse_response(data):
    json = {}
    json['status'] = 'success' if data.get('status') == 'EXECUTED' else 'error'
    return json

  def post(self, id):
    args = parser.parse_args()
    payload = GM_Api.post(self.URL, Vehicle_Engine.body(id, args.get('action')))
    data = payload.get('actionResult')
    return Vehicle_Engine.parse_response(data)

api.add_resource(Vehicle_Name, '/vehicles/<id>')
api.add_resource(Vehicle_Doors, '/vehicles/<id>/doors')
api.add_resource(Vehicle_Fuel, '/vehicles/<id>/fuel')
api.add_resource(Vehicle_Battery, '/vehicles/<id>/battery')
api.add_resource(Vehicle_Engine, '/vehicles/<id>/engine')

if __name__ == '__main__':
  app.run()
