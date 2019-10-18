from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Vehicle_Name(Resource):
  def get(self, id):
    return {}

class Vehicle_Doors(Resource):
  def get(self, id):
    return {}

class Vehicle_Fuel(Resource):
  def get(self, id):
    return {}

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
