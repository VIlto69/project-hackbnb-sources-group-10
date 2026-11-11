from os import path, getenv

basedir = path.abspath(path.dirname(__file__))

# [D10] Origines CORS définies par l'environnement. En production le front et l'API
# sont servis sur la même origine (Apache /api/), donc aucune origine n'est nécessaire.
CORS_ORIGINS = [o for o in getenv("CORS_ORIGINS", "").split(",") if o]

SQLALCHEMY_DATABASE_URI = "sqlite:///./database.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False
