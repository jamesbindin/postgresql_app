from psycopg2 import pool

class Database:
    """Uses psycopy2 to make a pool of connection to the database, its methods return and dispose of connections"""
    __connection_pool = None

    @classmethod
    def initialize(cls, **kwargs):
        """Opens a connection pool and stores it as a class variable"""
        cls.__connection_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, **kwargs)

    @classmethod
    def get_connection(cls):
        """Returns a connection to the database from the connection pool"""
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        """Disposes of connection, requires an active connection as a parameter"""
        Database.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        Database.__connection_pool.closeall()


class CursorFromConnectionFromPool:
    """Class that uses the connections from the Database class to returns cursors and allowing client class to
     use the 'with' keyword to dispose of them."""
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Allows client to use an instance of the class and the 'with' keyword to recieve a cursor."""
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_val, exception_traceback):
        """disposes of cursor, commits changes to database, closes connection when end of 'with' has been reached."""
        if exception_val is not None:
            print("EXCEPTION RAISED")
            print("TYPE: {}, VALUE: {}, TRACEBACK: {}".format(exception_type, exception_val, exception_traceback))
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)
