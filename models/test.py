from flask_sqlalchemy import SQLAlchemy
class Product(db.Model):
        __tablename__='linebot_test3'
        pid = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(30), unique=False, nullable=False)
        description = db.Column(db.String(255), nullable=False)
        insert_time = db.Column(db.DateTime, default=datetime.now)
        update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

        def __init__(self, name, description):
                self.name = name
                self.description = description
def test3():
    db.create_all()
