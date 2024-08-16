# db_operations.py
import datetime

import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # or the IP address of your MySQL server
            user='ouni',
            password='12345',
            database='restaurant_management'
        )
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS face_recognition_events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        event_type VARCHAR(10),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()

def save_face_event(connection, name, event_type):
    
    x = datetime.datetime.now()
    cursor = connection.cursor()
    print(f"name: {name},   event_type: {event_type},   datetime: {x}")
    insert_query = '''
    INSERT INTO face_recognition_events (name, event_type,timestamp )
    VALUES (%s, %s, %s);
    '''
    cursor.execute(insert_query, (name, event_type,x))
    connection.commit()

if __name__ == '__main__':
    # Connect to the database
    conn = create_connection()
    if conn:
        create_table(conn)
        # Example face event data
        # save_face_event(conn, 'John Doe', 'enters')
        # save_face_event(conn, 'Jane Smith', 'exits')

        # Close the connection
        conn.close()
