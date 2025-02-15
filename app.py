"""
This is the Root file for the Flask app.

Todo:
    - move routes to separate files
"""

from datetime import date
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import old_get_db_connection, SQLALCHEMY_DATABASE_URI
from models import db, Geo, Observation


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/observation', methods=['POST'])
def add_observation():
    try:
        data = request.get_json()

        geo_id = data.get('geo_id')
        date_value = data.get('date')
        analysis = data.get('analysis')
        asset_url = data.get('asset_url')
        external_url = data.get('external_url')

        if not date_value or not analysis or not asset_url or not external_url:
            return jsonify({"error": "Missing required fields"}), 400

        date_obj = date.fromisoformat(date_value)

        new_observation = Observation(
            geo_id=geo_id,
            date=date_obj,
            analysis=analysis,
            asset_url=asset_url,
            external_url=external_url
        )

        db.session.add(new_observation)
        db.session.commit()

        return jsonify({"message": "Observation added successfully", "id": new_observation.id}), 201

    except Exception as e:
        db.session.rollback()
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
