#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Plant, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        return [plant.to_dict() for plant in Plant.query.all()]

    def post(self):
        data = request.json

        new_plant = Plant(name=data.get('name'),
                          image=data.get('image'),
                          price=data.get('price'))
        db.session.add(new_plant)
        db.session.commit()

        return new_plant.to_dict(), 201


class PlantByID(Resource):

    def get(self, id):
        return db.session.get(Plant, id).to_dict()


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
