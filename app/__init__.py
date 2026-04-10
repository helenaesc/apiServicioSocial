import os
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
from .routes.admin_events import admin_events_bp
from .routes.admin_event_projects import admin_event_projects_bp
from .routes.student_requests import student_requests_bp
from .routes.student_pass import student_pass_bp
from .routes.staff_checkin import staff_checkin_bp
from .routes.student_registration import student_registration_bp
from .routes.admin_incidents import admin_incidents_bp
from .routes.admin_dashboard import admin_dashboard_bp
from .routes.admin_master_projects import admin_master_projects_bp
from .routes.admin_catalogs import admin_catalogs_bp
from .routes.admin_project_tokens import admin_project_tokens_bp
from .routes.admin_project_import_export import admin_project_import_export_bp
from .routes.admin_registrations import admin_registrations_bp
from .routes.admin_session_auth import admin_session_auth_bp
from .routes.admin_users_management import admin_users_management_bp
from .routes.admin_registration_evidence import admin_registration_evidence_bp
from .routes.admin_event_export import admin_event_export_bp

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False  


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
    app.register_blueprint(admin_events_bp)
    app.register_blueprint(admin_event_projects_bp)
    app.register_blueprint(student_requests_bp)
    app.register_blueprint(student_pass_bp)
    app.register_blueprint(staff_checkin_bp)
    app.register_blueprint(student_registration_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_master_projects_bp)
    app.register_blueprint(admin_catalogs_bp)
    app.register_blueprint(admin_incidents_bp)
    app.register_blueprint(admin_project_tokens_bp)
    app.register_blueprint(admin_project_import_export_bp)
    app.register_blueprint(admin_registrations_bp)
    app.register_blueprint(admin_session_auth_bp)
    app.register_blueprint(admin_users_management_bp)
    app.register_blueprint(admin_registration_evidence_bp)
    app.register_blueprint(admin_event_export_bp)


    return app