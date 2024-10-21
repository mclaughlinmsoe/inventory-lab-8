from models import Schema

class BeerService:
    def __init__(self):
        self.schema = Schema()

    def add_location(self, data):
        conn = self.schema.get_connection()
        query = "INSERT INTO Location (Name) VALUES (?)"
        conn.execute(query, (data['name'],))
        conn.commit()
        return {"message": "Location added successfully"}

    def remove_location(self, location_name):
        conn = self.schema.get_connection()
        query = "DELETE FROM Location WHERE Name = ?"
        conn.execute(query, (location_name,))
        conn.commit()
        return {"message": "Location removed successfully"}

    def get_locations(self):
        conn = self.schema.get_connection()
        query = "SELECT * FROM Location"
        result = conn.execute(query).fetchall()
        return [dict(row) for row in result]

    def add_beer(self, data):
        conn = self.schema.get_connection()
        query = "INSERT INTO Beer (Name, Brewery) VALUES (?, ?)"
        conn.execute(query, (data['name'], data['brewery']))
        conn.commit()
        return {"message": "Beer added successfully"}

    def add_inventory(self, data):
        conn = self.schema.get_connection()
        query = """
        SELECT id, Quantity FROM Inventory
        WHERE BeerName = ? AND Brewery = ? AND LocationName = ? AND Size = ?
        """
        inventory = conn.execute(query, (data['beer_name'], data['brewery'], data['location_name'], data['size'])).fetchone()

        if inventory:
            new_quantity = inventory['Quantity'] + int(data['quantity'])
            update_query = "UPDATE Inventory SET Quantity = ? WHERE id = ?"
            conn.execute(update_query, (new_quantity, inventory['id']))
        else:
            insert_query = """
            INSERT INTO Inventory (BeerName, Brewery, LocationName, Quantity, Size)
            VALUES (?, ?, ?, ?, ?)
            """
            conn.execute(insert_query, (data['beer_name'], data['brewery'], data['location_name'], int(data['quantity']), data['size']))
        
        conn.commit()
        return {"message": "Inventory updated successfully"}

    def get_locations_for_beer(self, beer_name, brewery):
        conn = self.schema.get_connection()
        query = """
        SELECT Location.* FROM Location
        JOIN Inventory ON Location.Name = Inventory.LocationName
        WHERE Inventory.BeerName = ? AND Inventory.Brewery = ?
        """
        result = conn.execute(query, (beer_name, brewery)).fetchall()
        return [dict(row) for row in result]

    def get_sizes_for_beer(self, beer_name, brewery):
        conn = self.schema.get_connection()
        query = """
        SELECT DISTINCT Size FROM Inventory
        WHERE BeerName = ? AND Brewery = ?
        """
        result = conn.execute(query, (beer_name, brewery)).fetchall()
        return [dict(row) for row in result]

    def get_beers_for_location(self, location_name):
        conn = self.schema.get_connection()
        query = """
        SELECT Beer.Name, Beer.Brewery, Inventory.Quantity, Inventory.Size
        FROM Beer
        JOIN Inventory ON Beer.Name = Inventory.BeerName AND Beer.Brewery = Inventory.Brewery
        WHERE Inventory.LocationName = ?
        """
        result = conn.execute(query, (location_name,)).fetchall()
        return [dict(row) for row in result]

    def get_beer_list(self):
        conn = self.schema.get_connection()
        query = "SELECT * FROM Beer"
        result = conn.execute(query).fetchall()
        return [dict(row) for row in result]

    def get_inventory_for_beer(self, beer_name, brewery):
        conn = self.schema.get_connection()
        query = """
        SELECT Inventory.LocationName, Inventory.Quantity, Inventory.Size
        FROM Inventory
        WHERE Inventory.BeerName = ? AND Inventory.Brewery = ?
        """
        result = conn.execute(query, (beer_name, brewery)).fetchall()
        return [dict(row) for row in result]

    def drink_beer(self, beer_name, brewery, location_name, size):
        conn = self.schema.get_connection()
        query = """
        SELECT id, Quantity FROM Inventory
        WHERE BeerName = ? AND Brewery = ? AND LocationName = ? AND Size = ?
        """
        inventory = conn.execute(query, (beer_name, brewery, location_name, size)).fetchone()

        if inventory:
            new_quantity = inventory['Quantity'] - 1
            if new_quantity > 0:
                update_query = "UPDATE Inventory SET Quantity = ? WHERE id = ?"
                conn.execute(update_query, (new_quantity, inventory['id']))
            else:
                delete_query = "DELETE FROM Inventory WHERE id = ?"
                conn.execute(delete_query, (inventory['id'],))

            # Check if there are any remaining inventories for the beer
            check_query = "SELECT COUNT(*) as count FROM Inventory WHERE BeerName = ? AND Brewery = ?"
            remaining = conn.execute(check_query, (beer_name, brewery)).fetchone()
            if remaining['count'] == 0:
                delete_beer_query = "DELETE FROM Beer WHERE Name = ? AND Brewery = ?"
                conn.execute(delete_beer_query, (beer_name, brewery))

            conn.commit()
            return {"message": "Enjoy your beer!"}
        else:
            return {"message": "No such beer found in the specified location and size."}