from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
<<<<<<< HEAD
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
=======
from flask_sqlalchemy import SQLAlchemy
>>>>>>> c6fca4113377df4fb9dfcb688d6135bc4435aaec


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

<<<<<<< HEAD
        from app import db

        try:
            existing_user_query = text(
                "SELECT * FROM [user] WHERE username = :username")
            existing_user = db.session.execute(
                existing_user_query,
                {'username': normalized_username}).fetchone()
            if existing_user:
                raise ValueError("Username already used.")

            hashed_password = self.__hash_password(password)

            insert_query = text("""
                INSERT INTO [user] (username, password)
                VALUES (:username, :password)
            """)
            db.session.execute(insert_query, {
                'username': normalized_username,
                'password': hashed_password
            })
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error occurred: {str(e)}")
=======
        if User.query.filter_by(username=normalized_username).first():
            raise ValueError("Username already used.")

        hashed_password = self.__hash_password(password)
        new_user = User(username=normalized_username,
                        password=hashed_password)

        db = SQLAlchemy()
        db.session.add(new_user)
        db.session.commit()
>>>>>>> c6fca4113377df4fb9dfcb688d6135bc4435aaec

    def verify_user(self, username, password):
        normalized_username = username.strip().lower()

        from app import db

        try:
            user_query = text(
                "SELECT password FROM [user] WHERE username = :username")
            user = db.session.execute(
                user_query, {'username': normalized_username}).fetchone()

            if user and self.__verify_password(user.password, password):
                return True
            return False

        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error occurred: {str(e)}")
