"""
Application Factory – SOLID: Single Responsibility & Dependency Inversion
Flask uygulamasını oluşturur, extension'ları ve blueprint'leri kaydeder.
"""

from flask import Flask
from datetime import timedelta
import os

from config import Config


def create_app(config_class=Config):
    # --- Konfigürasyon doğrulama ---
    config_class.validate()

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
    )

    # --- Konfigürasyon (tek kaynak: Config) ---
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']
    app.permanent_session_lifetime = timedelta(hours=app.config.get('PERMANENT_SESSION_LIFETIME_HOURS', 4))

    # --- Extension'ları başlat ---
    from app.extensions import mail
    mail.init_app(app)

    # --- DB havuzunu başlat ---
    from db_manager import init_pool, close_db
    with app.app_context():
        init_pool()
    app.teardown_appcontext(close_db)

    # --- Blueprint'leri kaydet ---
    from app.blueprints.auth import auth_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.student import student_bp
    from app.blueprints.hoca import hoca_bp
    from app.blueprints.kontrolcu import kontrolcu_bp
    from app.blueprints.api import api_bp
    from app.blueprints.export import export_bp
    from app.blueprints.duyuru import duyuru_bp
    from app.blueprints.mesaj import mesaj_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(hoca_bp, url_prefix='/hoca')
    app.register_blueprint(kontrolcu_bp, url_prefix='/kontrolcu')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(export_bp)
    app.register_blueprint(duyuru_bp)
    app.register_blueprint(mesaj_bp, url_prefix='/mesaj')

    # --- Güvenlik header'ları ---
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    # --- Error handler'lar ---
    from flask import render_template, redirect, request, url_for, flash

    @app.errorhandler(404)
    def not_found(e):
        return render_template('shared/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('shared/500.html'), 500

    @app.errorhandler(413)
    def too_large(e):
        flash('Dosya boyutu 5 MB sınırını aşıyor!')
        return redirect(request.referrer or url_for('auth.login'))

    return app
