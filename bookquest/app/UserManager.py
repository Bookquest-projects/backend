import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


class UserManager:

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.ph = PasswordHasher()

    def __hash_password(self, password, salt=None):
        if not salt:
            salt = os.urandom(16)
        return self.ph.hash(password, salt.hex())

    def __verify_password(self, hashed_password, password, salt):
        try:
            return self.ph.verify(hashed_password, password + salt.hex())
        except (VerifyMismatchError, VerificationError):
            return False

    def __is_username_taken(self, username):
        query = "SELECT COUNT(*) FROM users WHERE username = %s"
        result = self.db_manager.execute_select(query, (username,))
        return result[0][0] > 0

    def create_user(self, username, password):
        if self.__is_username_taken(username):
            raise ValueError("Username already used.")

        salt = os.urandom(16)
        hashed_password = self.__hash_password(password, salt)
        query = ("INSERT INTO users (username, password, salt) "
                 "VALUES (%s, %s, %s)")
        self.db_manager.execute_insert(query, (
            username, hashed_password, salt.hex()))

    def verify_user(self, username, password):
        query = "SELECT password, salt FROM users WHERE username = %s"
        result = self.db_manager.execute_select(query, (username,))
        if result:
            hashed_password, salt = result[0]
            return self.__verify_password(hashed_password, password,
                                          bytes.fromhex(salt))
        return False
