from os import environ

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = environ.get('SECRET_KEY')
# FLASK_APP = environ.get('FLASK_APP')
# FLASK_ENV = environ.get('FLASK_ENV')

# LOCAL_SQLALCHEMY_DATABASE_URI = (
#     'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}?charset=utf8mb4').format(
#         user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
#         database=CLOUDSQL_DATABASE)

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
