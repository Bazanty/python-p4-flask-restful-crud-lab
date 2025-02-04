import json
import unittest
from app import app, db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert(response.status_code == 200)

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        data = json.loads(response.data.decode())

        assert(type(data) == dict)
        assert(data["id"])
        assert(data["name"])

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        with app.app_context():
            plant_1 = Plant.query.filter_by(id=1).first()
            plant_1.is_in_stock = True
            db.session.add(plant_1)
            db.session.commit()

        response = app.test_client().patch(
            '/plants/1',
            json={
                "is_in_stock": False,
            }
        )
        data = json.loads(response.data.decode())

        assert(type(data) == dict)
        assert(data["id"])
        assert(data["is_in_stock"] == False)

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''returns JSON representing the deletion of a Plant object at "/plants/<int:id>".'''
    with app.app_context():
        # Add a new plant to test deletion
        lo = Plant(
            name="Live Oak",
            image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
            price=250.00,
            is_in_stock=False,
        )
        db.session.add(lo)
        db.session.commit()

        # Ensure the plant exists before deletion
        plant = Plant.query.get(lo.id)
        assert plant is not None

        # Send DELETE request to delete the plant
        response = app.test_client().delete(f'/plants/{lo.id}')
        data = json.loads(response.data.decode())  # Parse the JSON response

        # Check if the response contains the correct deletion message with the plant ID
        assert f"Plant {lo.id} has been deleted" == data["message"]

        # Ensure the plant is deleted from the database
        deleted_plant = Plant.query.get(lo.id)
        assert deleted_plant is None


if __name__ == '__main__':
    unittest.main()
