from flask import Flask
from .routes.views import views_bp
from .routes.catalogs import catalogs_bp
from .routes.projects import projects_bp
from .routes.inscripciones import inscripciones_bp
from .routes.admin_tokens import admin_tokens_bp
from .routes.admin_projects import admin_projects_bp
from .routes.admin_auth import admin_auth_bp
from .routes.admin_access_codes import admin_access_bp
from .routes.admin_settings import admin_settings_bp
from .routes.player_auth import player_auth_bp
from .routes.player_register import player_register_bp

def create_app():
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    app.register_blueprint(views_bp)
    app.register_blueprint(catalogs_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(inscripciones_bp)
    app.register_blueprint(admin_tokens_bp)
    app.register_blueprint(admin_projects_bp)
    app.register_blueprint(admin_auth_bp)
    app.register_blueprint(admin_access_bp)
    app.register_blueprint(admin_settings_bp)
    app.register_blueprint(player_auth_bp)
    app.register_blueprint(player_register_bp)

    return app