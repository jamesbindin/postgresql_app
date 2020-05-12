from database import Database
from user import User
Database.initialize(database="postgres", user="postgres", password="password", host="localhost")

my_user = User("anne@asmith.com", "Rolf", "Smith", None)
my_user.save_to_db()

user_from_db = User.load_from_db_by_email("anne@asmith.com")
print(user_from_db)
