import os
import psycopg2
from dotenv import load_dotenv


def create_connection():
    connection = psycopg2.connect(dbname=os.getenv('DB_NAME'),
                                  user=os.getenv('DB_USER'),
                                  password=os.getenv('DB_PASSWORD'),
                                  host=os.getenv('DB_HOST'),
                                  port=os.getenv('DB_PORT'))

    cursor = connection.cursor()
    return connection, cursor


def create_table():
    try:
        connection, cursor = create_connection()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS Image(imageID INTEGER, title TEXT, image BYTEA)")
        except(Exception, psycopg2.Error) as error:
            print("Error while creating Image table", error)
        finally:
            connection.commit()
            connection.close()
    finally:
        pass


def write_blob(image_id: str, name: str, file_path: str):
    try:
        image = open(file_path, 'rb').read()
        connection, cursor = create_connection()
        try:
            cursor.execute("INSERT INTO Image(imageID,title,image) " + "VALUES(%s,%s,%s)", (image_id, name, psycopg2.Binary(image)))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting data in Image table", error)
        finally:
            connection.close()
    finally:
        pass

def fetch_rows(table_name: str):
    try:
        connection, cursor = create_connection()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                id, title, image = row
                print(f"ID: {id}, Title: {title}, Image: {image}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading data from Image table", error)
    finally:
        pass
