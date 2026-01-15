from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Earthquake

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)

# Ensure tables exist
with app.app_context():
    db.create_all()

# Route to get all earthquakes
@app.route("/earthquakes")
def earthquakes():
    try:
        earthquakes = Earthquake.query.all()
        return jsonify({
            "count": len(earthquakes),
            "quakes": [e.to_dict() for e in earthquakes]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get earthquakes by magnitude
@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):
    try:
        earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
        return jsonify({
            "count": len(earthquakes),
            "quakes": [e.to_dict() for e in earthquakes]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get earthquake by ID
@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    try:
        earthquake = Earthquake.query.get(id)
        if earthquake:
            return jsonify(earthquake.to_dict()), 200
        else:
            return jsonify({"message": f"Earthquake {id} not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
