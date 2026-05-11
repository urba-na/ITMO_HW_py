from flask import Flask
from werkzeug.security import generate_password_hash
from config import (
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    MAIL_SERVER,
    MAIL_PORT,
    MAIL_USE_TLS,
    MAIL_USE_SSL,
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER)
from extensions import db, login_manager, mail
from models import User
from routes import init_routes

def ensure_admin_exists():
    user = User.query.filter_by(username=DEFAULT_ADMIN_USERNAME).first()

    if user:
        user.role = 'admin'
        user.is_approved = True
        user.password = generate_password_hash(DEFAULT_ADMIN_PASSWORD)
    else:
        user = User(
            username=DEFAULT_ADMIN_USERNAME,
            email=MAIL_DEFAULT_SENDER,
            password=generate_password_hash(DEFAULT_ADMIN_PASSWORD),
            role='admin',
            is_approved=True
        )
        db.session.add(user)

    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    mail.init_app(app)

    with app.app_context():
        db.create_all()
        ensure_admin_exists()

    init_routes(app)

    @app.context_processor
    def inject_pending_users_count():
        from flask_login import current_user
        from models import User

        pending_users_count = 0

        if current_user.is_authenticated and current_user.role == 'admin':
            pending_users_count = User.query.filter_by(is_approved=False).count()

        return dict(pending_users_count=pending_users_count)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

