from app import app
from app.models import db
from run_dev import create_admin


db.init_app(app)

with app.app_context():
    db.create_all()
    create_admin()
