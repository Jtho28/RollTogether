from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
import sqlite3

class Rider:
    def __init__(self, first_name:str, last_initial:str, 
                departure_locX:float, departure_locY:float,
                arrival_locX:float, arrival_locY:float):
        
        if (departure_locX > 180 or departure_locX < -180 or
            departure_locY < -90 or departure_locY > 90):
            print("Invalid departure location :(")
            raise CoordError("Invalid departure coordinates provided")
        else:
            self.departure_locX = departure_locX
            self.departure_locY = departure_locY

        if (arrival_locX > 180 or departure_locX < -180 or
            arrival_locY < -90 or arrival_locY > 90):
            print("Invalid arrival location")
            raise CoordError("invalid arrival coordinates provided")
        else:
            self.arrival_locX = arrival_locX
            self.arrival_locY = arrival_locY

        self.safety_coef = 3.0
        self.user_rating = 3.0

        self.first_name = first_name
        self.last_initial = last_initial

        conn = sqlite3.connect('rollt.db')
        cursor = conn.cursor()
        cursor.execute('''
                SELECT MAX(rider_id)
                FROM Riders
                GROUP BY rider_id''')
        

        if cursor.fetchone() is None:
            self.rider_id = 0
        else:
            self.rider_id = cursor.fetchone()[0] + 1


        cursor.execute(f'''INSERT OR IGNORE INTO Riders
                     VALUES ({self.rider_id}, "{self.first_name}",
                            "{self.last_initial}", {self.departure_locX},
                            {self.departure_locY}, {self.arrival_locX},
                            {self.arrival_locY}, {self.safety_coef}, {self.user_rating})''')

        conn.commit()
        conn.close()


    def __str__(self):
        return f'{self.dep}'

    def __repr__(self):
        return self.__str__()


class GroupRide:
    def __init__(self, group: list[Rider]):
        self.group = group


class Group:
    def __init__(self, users: list[Rider]):
        self.users = users

def resolve(users: Group):

    G = nx.Graph()

    G.add_nodes_from(users.users)

    nx.draw(G, with_labels=True)
    plt.savefig("epic.png")
    plt.show()

def setup_db():
    # Create table 
    conn = sqlite3.connect('rollt.db')
    cursor = conn.cursor()

    fd = open('./rolltDML.sql', 'r')
    sql_DML = fd.read()
    fd.close()

    # Execute DML
    cursor.executescript(sql_DML)
    
    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

def main():
    test_user = Rider("Jackson", "M", 50.00,
                       50.0, 50.0, 50.0)
                       

if __name__=="__main__":
    main()