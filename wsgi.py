from config import Config
from application import create_app

app = create_app(Config)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(host='127.0.0.1', port=8080, debug=True)
