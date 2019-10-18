from flask import Flask, request
from flask_restful import Resource, Api
from gm_api import GM_Api

app = Flask(__name__)
api = Api(app)

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
    doors = data.get('doors').get('values')
    json = []

    for door in doors:
      json.append({
        'location': door.get('location').get('value'),
        'locked': door.get('locked').get('value') == 'True',
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
  def get(self, id):
    return {}

class Vehicle_Engine(Resource):
  def post(self, id):
    return {}

api.add_resource(Vehicle_Name, '/vehicles/<id>')
api.add_resource(Vehicle_Doors, '/vehicles/<id>/doors')
api.add_resource(Vehicle_Fuel, '/vehicles/<id>/fuel')
api.add_resource(Vehicle_Battery, '/vehicles/<id>/battery')
api.add_resource(Vehicle_Engine, '/vehicles/<id>/engine')

if __name__ == '__main__':
  app.run()
