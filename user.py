from database import CursorFromConnectionFromPool


class User:
    """Class that creates user record on the database. id should be None (default value) the database auto increments"""
    def __init__(self, email, first_name, last_name, id=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

    def save_to_db(self):
        """Saves user on the database, """
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO users (email, first_name, last_name) VALUES (%s, %s, %s)",
                           (self.email, self.first_name, self.last_name))

    @classmethod
    def load_from_db_by_email(cls, email):
        """Loads user record from db using email as a reference"""
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            return cls(user_data[1], user_data[2], user_data[3], user_data[0])

    def __str__(self):
        return "User Email: {}".format(self.email)