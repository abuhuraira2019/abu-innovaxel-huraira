from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from .views import shorten_url
    app.register_blueprint(shorten_url)

    return app

