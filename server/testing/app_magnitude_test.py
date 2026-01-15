import json
import pytest
from app import app, db, Earthquake

# Fixture: fresh in-memory DB with seeded data
@pytest.fixture(scope="module")
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            earthquakes = [
                Earthquake(id=1, magnitude=9.5, location="Chile", year=1960),
                Earthquake(id=2, magnitude=9.2, location="Alaska", year=1964),
                Earthquake(id=3, magnitude=9.1, location="Sumatra", year=2004),
                Earthquake(id=4, magnitude=9.0, location="Japan", year=2011),
            ]
            db.session.bulk_save_objects(earthquakes)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


class TestApp:
    """Flask tests for /earthquakes/magnitude route"""

    def test_earthquake_magnitude_route(self, test_client):
        """Resource available at /earthquakes/magnitude/<magnitude>"""
        response = test_client.get('/earthquakes/magnitude/8.0')
        assert response.status_code == 200

    def test_earthquakes_magnitude_match_response(self, test_client):
        """Displays JSON with keys count, quakes for magnitude 9.0"""
        response = test_client.get('/earthquakes/magnitude/9.0')
        response_json = response.get_json()
        assert response_json["count"] == 4  # all quakes >= 9.0
        quakes = response_json["quakes"]
        assert all(q["magnitude"] >= 9.0 for q in quakes)

    def test_earthquakes_magnitude_no_match_response(self, test_client):
        """Displays JSON with count=0 if no quakes match"""
        response = test_client.get('/earthquakes/magnitude/10.0')
        response_json = response.get_json()
        assert response_json["count"] == 0
        assert response_json["quakes"] == []
