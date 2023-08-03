import pytest
from app import app
from app.models import db, Admin, Dispenser, Transaction
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="session")
def test_setup():
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_data.db"
    app.config["JWT_SECRET_KEY"] = "test_secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    db.init_app(app)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            test_user = Admin(username="test_user", password="test_password")
            db.session.add(test_user)
            db.session.commit()
            test_token = create_access_token(identity=test_user.id)

            yield client, db, test_token

            db.session.remove()
            db.drop_all()


@pytest.fixture(scope="function")
def test_teardown(test_setup):
    _, db, _ = test_setup
    yield
    db.session.query(Dispenser).delete()
    db.session.query(Transaction).delete()
    db.session.commit()
