from os import environ

# FLASK_APP = environ.get('FLASK_APP')
# FLASK_ENV = environ.get('FLASK_ENV')
# General
# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = environ.get('SECRET_KEY')
TESTING = environ.get('TESTING', False)
FLASK_DEBUG = environ.get('FLASK_DEBUG', False)

# Database
SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
DB_TYPE = environ.get('DB_TYPE')
DB_CONNECTOR = environ.get('DB_CONNECTOR')
DB_USERNAME = environ.get('DB_USERNAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST', '127.0.0.1')
DB_PORT = environ.get('DB_PORT', '3306')
DB_NAME = environ.get('DB_NAME')
SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}+{DB_CONNECTOR}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
# LOCAL_SQLALCHEMY_DATABASE_URI = (
#     'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}?charset=utf8mb4').format(
#         user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
#         database=CLOUDSQL_DATABASE)
# [DB_TYPE]+[DB_CONNECTOR]://[DB_USERNAME]:[DB_PASSWORD]@[DB_HOST]:[DB_PORT]/[DB_NAME]

# # When running on App Engine a unix socket is used to connect to the cloudsql instance.
# LIVE_SQLALCHEMY_DATABASE_URI = (
#     'mysql+pymysql://{user}:{password}@localhost/{database}'
#     '?unix_socket=/cloudsql/{connection_name}&charset=utf8mb4').format(
#         user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
#         database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

# if environ.get('GAE_INSTANCE'):
#     SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
# else:
#     SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
