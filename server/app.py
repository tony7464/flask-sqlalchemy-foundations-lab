# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    """Return one earthquake, or a 404 JSON message when the id is missing."""
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if not earthquake:
        return make_response({"message": f"Earthquake {id} not found."}, 404)

    return make_response({
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year,
    }, 200)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    """Return every earthquake at or above the given magnitude."""
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).order_by(Earthquake.id).all()

    return make_response({
        "count": len(quakes),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year,
            }
            for quake in quakes
        ],
    }, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
