from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class UserManager:

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.ph = PasswordHasher()

    def __hash_password(self, password):
        return self.ph.hash(password)

    # Si on doit vérifier un password quand un user se connecte
    def __verify_password(self, hashed_password, password):
        try:
            return self.ph.verify(hashed_password, password)
        except VerifyMismatchError:
            return False

    def __is_email_taken(self, email):
        # Configurer la data source ?
        query = "SELECT COUNT(*) FROM users WHERE email = %s"
        result = self.db_manager.execute_select(query, (email,))
        return result[0][0] > 0

    def create_user(self, username, email, password):
        if self.__is_email_taken(email):
            raise ValueError("Email already used.")

        hashed_password = self.__hash_password(password)
        # Configurer la data source ?
        query = ("INSERT INTO users (username,"
                 "email,"
                 "password) VALUES (%s, %s, %s)")
        self.db_manager.execute_insert(query,
                                       (username, email, hashed_password))
