import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# database file will be created inside the backend folder
DATABASE = os.path.join(BASE_DIR, "database.db")

# change these keys before submitting / deploying
SECRET_KEY = "medassist-secret-key"
JWT_SECRET_KEY = "medassist-jwt-secret-key-change-this-before-submitting"

# token is valid for 1 hour
JWT_EXPIRY = timedelta(hours=1)
