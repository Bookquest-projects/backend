from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from flask_sqlalchemy import SQLAlchemy


class UserManager:

    def __init__(self):
        self.ph = PasswordHasher()

    def __hash_password(self, password):
        return self.ph.hash(password)

    def __verify_password(self, hashed_password, password):
        try:
            return self.ph.verify(hashed_password, password)
        except (VerifyMismatchError, VerificationError):
            return False

    def create_user(self, username, password):
        normalized_username = username.strip().lower()

        if User.query.filter_by(username=normalized_username).first():
            raise ValueError("Username already used.")

        hashed_password = self.__hash_password(password)
        new_user = User(username=normalized_username,
                        password=hashed_password)

        db = SQLAlchemy()
        db.session.add(new_user)
        db.session.commit()

    def verify_user(self, username, password):
        normalized_username = username.strip().lower()
        user = User.query.filter_by(username=normalized_username).first()
        if user and self.__verify_password(user.password, password):
            return True
        return False
