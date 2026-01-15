# server/testing/conftest.py
import pytest
from app import app, db, Earthquake

@pytest.fixture(scope="module")
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # in-memory DB for testing

    with app.test_client() as testing_client:
        with app.app_context():
            # Create tables
            db.create_all()

            # Seed data
            earthquakes = [
                Earthquake(id=1, magnitude=9.5, location="Chile", year=1960),
                Earthquake(id=2, magnitude=9.2, location="Alaska", year=1964),
                Earthquake(id=3, magnitude=9.1, location="Sumatra", year=2004),
                Earthquake(id=4, magnitude=9.0, location="Japan", year=2011),
            ]
            db.session.bulk_save_objects(earthquakes)
            db.session.commit()

        yield testing_client

        # Teardown
        with app.app_context():
            db.drop_all()
