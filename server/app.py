from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant  # Assuming your model is in 'models.py'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Root route
@app.route('/')
def home():
    return "Welcome to the Plants API!"

class Plants(Resource):
    def get(self):
        # Retrieve all plants from the database
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        # Add a new plant to the database
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True)  # Default to True if not provided
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

# Add Plants resource to API
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        return make_response(jsonify({"message": "Plant not found"}), 404)

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            data = request.get_json()
            if 'is_in_stock' in data:
                plant.is_in_stock = data['is_in_stock']
                db.session.commit()
                return make_response(jsonify(plant.to_dict()), 200)
            return make_response(jsonify({"message": "No 'is_in_stock' field provided"}), 400)
        return make_response(jsonify({"message": "Plant not found"}), 404)

    class PlantByID(Resource):

     @app.route('/plants/<int:id>', methods=['DELETE'])
     def delete_plant(id):
        plant = Plant.query.get(id)
        if plant:
         db.session.delete(plant)
        db.session.commit()
        return jsonify({"message": f"Plant {id} has been deleted"}), 200
        return jsonify({"message": "Plant not found"}), 404

# Add PlantByID resource to API
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
