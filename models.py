import sqlite3
import threading

class Schema:
    _thread_local = threading.local()

    def __init__(self):
        self.conn = self.get_connection()
        self.create_location_table()
        self.create_beer_table()
        self.create_inventory_table()

    def create_location_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Location" (
            Name TEXT PRIMARY KEY
        );
        """
        self.conn.execute(query)

    def create_beer_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Beer" (
            Name TEXT NOT NULL,
            Brewery TEXT NOT NULL,
            PRIMARY KEY (Name, Brewery)
        );
        """
        self.conn.execute(query)

    def create_inventory_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Inventory" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BeerName TEXT,
            Brewery TEXT,
            LocationName TEXT,
            Quantity INTEGER,
            Size TEXT,
            FOREIGN KEY (BeerName, Brewery) REFERENCES Beer(Name, Brewery),
            FOREIGN KEY (LocationName) REFERENCES Location(Name)
        );
        """
        self.conn.execute(query)

    def get_connection(self):
        if not hasattr(self._thread_local, 'conn'):
            self._thread_local.conn = sqlite3.connect('beer_inventory.db', check_same_thread=False)
            self._thread_local.conn.row_factory = sqlite3.Row
        return self._thread_local.conn

    def close_connection(self):
        if hasattr(self._thread_local, 'conn'):
            self._thread_local.conn.close()
            del self._thread_local.conn