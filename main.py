import config
import app_start


app = app_start.create_app(config, debug=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
