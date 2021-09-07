import os
import unittest
import json

from flaskr import create_app
from models import setup_db, Plant


class PlantTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "plantsdb_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "postgres", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_plant = {"name": "test plant",
                          "scientific_name": "tes plante", "is_poisonous": False, "primary_color": "blue"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_plants(self):
        res = self.client().get("/plants")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_plants"])
        self.assertTrue(len(data["plants"]))

    def test_get_plant_search_with_results(self):
        res = self.client().post("/plants?search=Hydrangea")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_plants"])
        self.assertEqual(len(data["plants"]), 1)

    def test_get_book_search_without_results(self):
        res = self.client().post("/books?search=non_existant_plant")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_books"], 0)
        self.assertEqual(len(data["books"]), 0)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/plants?page=1000", json={"rating": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_update_plant_rating(self):
        res = self.client().patch("/plants/5", json={"rating": 1})
        data = json.loads(res.data)
        plant = Plant.query.filter(Plant.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(plant.format()["rating"], 1)

    def test_400_for_failed_update(self):
        res = self.client().patch("/plants/5")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_create_new_plant(self):
        res = self.client().post("/plants", json=self.new_plant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["plants"]))

    def test_405_if_plant_creation_not_allowed(self):
        res = self.client().post("/plants/45", json=self.new_plant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # Delete a different plant in each attempt
    def test_delete_plant(self):
        res = self.client().delete("/plants/2")
        data = json.loads(res.data)

        plant = Plant.query.filter(Plant.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 2)
        self.assertTrue(data["total_plants"])
        self.assertTrue(len(data["plants"]))
        self.assertEqual(plant, None)

    def test_422_if_plant_does_not_exist(self):
        res = self.client().delete("/plants/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
