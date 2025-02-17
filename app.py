"""
This is the Root file for the Flask app.

Todo:
    - move routes to separate files
"""

from datetime import date
import requests
from flask import Flask, jsonify, request
from config import old_get_db_connection, SQLALCHEMY_DATABASE_URI, ROBOFLOW_APIKEY
from models import db, Geo, Observation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Singleton SQL ALchemy 'db' instance is imported from models.py
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/observation', methods=['POST'])
def add_observation():
    try:
        data = request.get_json()

        geo_id = data.get('geo_id')
        date_value = data.get('date')
        asset_url = data.get('asset_url')
        external_url = data.get('external_url')



        if not date_value or not asset_url or not geo_id:
            return jsonify({"error": "Missing required fields"}), 400

        date_obj = date.fromisoformat(date_value)


        url = "https://detect.roboflow.com/aircraft-reco-1/2"
        params = {
            "api_key": ROBOFLOW_APIKEY,
            "confidence": 40,
            "overlap": 30,
            "format": "json",
            "image": "https://aircraft-reco.s3.us-east-1.amazonaws.com/geoid-06_2022-11-02.png"
        }

        headers = {
        "accept": "*/*"
        }

        response = requests.post(url, params=params, headers=headers, timeout = 10)

        print(response.json())

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch analysis"}), 500

        new_observation = Observation(
            geo_id=geo_id,
            date=date_obj,
            analysis=response.json(),
            asset_url=asset_url,
            external_url=external_url
        )

        db.session.add(new_observation)
        db.session.commit()

        return jsonify({"message": "Observation added successfully", "id": new_observation.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/observations/<int:geo_id>', methods=['GET'])
def get_observations_by_geo(geo_id):
    try:
        observations = Observation.query.filter_by(geo_id=geo_id).all()

        if not observations:
            return jsonify({"message": "No observations found for this geo_id"}), 404

        result = [
            {
                "id": obs.id,
                "geo_id": obs.geo_id,
                "date": obs.date.isoformat(),
                "analysis": obs.analysis,
                "asset_url": obs.asset_url,
                "external_url": obs.external_url
            }
            for obs in observations
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/geos")
def get_geos():
    """
    FOR TESTING PURPOSE ONLY
    This function is only here to test the Geo database
    """
    geos = Geo.query.all()
    return jsonify([geo.to_dict() for geo in geos])


@app.route('/geos_old')
def old_read_database():
    """
    DEPRECATED: we should use SQL Alchemy instead.
    This function is just here for training purpose and will be removed in future versions.
    """
    conn = old_get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT id, name, created_at FROM geo;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    user_list = [{"id": row[0], "name": row[1], "created_at": row[2]} for row in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)
