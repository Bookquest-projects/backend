from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


class UserManager:

    def __init__(self):
        self.ph = PasswordHasher()

    def __hash_password(self, password):
        return self.ph.hash(password)

    def __verify_password(self, password, hashed_password):
        try:
            return self.ph.verify(hashed_password, password)
        except (VerifyMismatchError, VerificationError):
            return False

    def __is_username_taken(self, username):
        from __init__ import session, User
        user = session.query(User).filter_by(username=username).first()
        return user is not None

    def create_user(self, username, password):
        if self.__is_username_taken(username):
            raise ValueError("Username already used.")

        hashed_password = self.__hash_password(password)

        from __init__ import User
        user = User(username=username, password=hashed_password)

        from __init__ import session
        session.add(user)
        session.commit()
        return True

    def verify_user(self, username, password):
        from __init__ import session, User
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            return False

        return self.__verify_password(password, user.password)
