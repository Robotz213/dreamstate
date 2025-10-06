import os

from flask import Flask


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development").capitalize() + "Config"

    from app import conf

    config_class = getattr(conf, config_name, conf.DevelopmentConfig)
    app.config.from_object(config_class)

    # Importa e registra blueprints de rotas
    from app.routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    return app
