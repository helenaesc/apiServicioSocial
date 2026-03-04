from flask import Flask
from .routes.views import views_bp
from .routes.catalogs import catalogs_bp
from .routes.projects import projects_bp
from .routes.inscripciones import inscripciones_bp

def create_app():
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    app.register_blueprint(views_bp)
    app.register_blueprint(catalogs_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(inscripciones_bp)

    return app