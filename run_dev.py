from app import app, admin_username, admin_password
from app.models import db, Admin


def create_admin():
    admin_user = Admin.query.filter_by(username=admin_username).first()
    if admin_user:
        print("Admin user already exists.")
    else:
        admin_user = Admin(username=admin_username, password=admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")


if __name__ == "__main__":
    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)
