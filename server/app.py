from flask import Flask, jsonify
from models import db, Earthquake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/earthquakes")
def earthquakes():
    earthquakes = Earthquake.query.all()

    return jsonify({
        "count": len(earthquakes),
        "quakes": [e.to_dict() for e in earthquakes]
    }), 200

@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return jsonify({
        "count": len(earthquakes),
        "quakes": [e.to_dict() for e in earthquakes]
    }), 200

@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        return jsonify(earthquake.to_dict()), 200
    else:
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404
