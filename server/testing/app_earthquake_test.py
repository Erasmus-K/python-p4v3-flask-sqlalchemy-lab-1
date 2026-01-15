import json
import pytest
from app import app, db, Earthquake

# Fixture to create a test client with seeded data
@pytest.fixture(scope="module")
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # in-memory DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Seed data exactly as the tests expect
            earthquakes = [
                Earthquake(id=1, magnitude=9.5, location="Chile", year=1960),
                Earthquake(id=2, magnitude=9.2, location="Alaska", year=1964),
                Earthquake(id=3, magnitude=9.1, location="Sumatra", year=2004),
                Earthquake(id=4, magnitude=9.0, location="Japan", year=2011),
            ]
            db.session.bulk_save_objects(earthquakes)
            db.session.commit()

        yield client

        # Teardown: drop all tables after tests
        with app.app_context():
            db.drop_all()


class TestApp:
    """Flask application tests for /earthquakes routes"""

    def test_earthquake_found_route(self, test_client):
        """Resource available at /earthquakes/<id>"""
        response = test_client.get('/earthquakes/1')
        assert response.status_code == 200

    def test_earthquake_not_found_route(self, test_client):
        """Resource not found returns 404"""
        response = test_client.get('/earthquakes/999')
        assert response.status_code == 404

    def test_earthquakes_found_response(self, test_client):
        """Displays JSON in /earthquakes/<id> route with keys id, magnitude, location, year"""
        response = test_client.get('/earthquakes/2')
        response_json = response.get_json()

        assert response_json["id"] == 2
        assert response_json["magnitude"] == 9.2
        assert response_json["location"] == "Alaska"
        assert response_json["year"] == 1964
        assert response.status_code == 200

    def test_earthquakes_not_found_response(self, test_client):
        """Displays message if earthquake id not found"""
        response = test_client.get('/earthquakes/9999')
        response_json = response.get_json()

        assert response_json["message"] == "Earthquake 9999 not found."
        assert response.status_code == 404
