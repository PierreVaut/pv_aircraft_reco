"""
This is the Root file for the Flask app.

Todo:
    - move routes to separate files
"""

from flask import Flask, jsonify
from config import old_get_db_connection, SQLALCHEMY_DATABASE_URI
from models import db, Geo

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def get_geos():
    """geo is short geographical point"""
    geos = Geo.query.all()
    return jsonify([geo.to_dict() for geo in geos])


@app.route('/old')
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
