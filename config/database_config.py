from application.models import db


def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///split_service.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


def create_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
