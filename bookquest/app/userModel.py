from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
