import os

from flask import Flask


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development").capitalize() + "Config"

    from flask import conf

    config_class = getattr(conf, config_name, conf.DevelopmentConfig)
    app.config.from_object(config_class)

    from flask.routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    return app


# Para rodar com gevent:
# from gevent.pywsgi import WSGIServer
# app = create_app()
# if __name__ == "__main__":
#     http_server = WSGIServer(("0.0.0.0", 5000), app)
#     http_server.serve_forever()
