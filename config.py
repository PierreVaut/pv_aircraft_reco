"""
This is the configuration file for the Flask app.

Todo:
    - Silence the "missing docstring" warning for the root files
"""

import os
import warnings
import psycopg2
from dotenv import load_dotenv

load_dotenv()

RDS_HOST = os.getenv("RDS_HOST")
RDS_NAME = os.getenv("RDS_NAME")
RDS_USER = os.getenv("RDS_USER")
RDS_PW = os.getenv("RDS_PW")
RDS_PORT=5432

ROBOFLOW_APIKEY = os.getenv("ROBOFLOW_APIKEY")

SQLALCHEMY_DATABASE_URI = f"postgresql://{RDS_USER}:{RDS_PW}@{RDS_HOST}:{RDS_PORT}/{RDS_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

def old_get_db_connection():
    """
    DEPRECATED: we should use SQL Alchemy instead.
    This function is just here for training/debugging purpose.
    It will be removed in future versions.
    """
    warnings.warn(
        "This function is deprecated. Use SQL Alchemy instead.",
        DeprecationWarning,
        stacklevel=2)

    try:
        conn = psycopg2.connect(
            host=RDS_HOST,
            database=RDS_NAME,
            user=RDS_USER,
            password=RDS_PW,
            port=RDS_PORT
        )
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None