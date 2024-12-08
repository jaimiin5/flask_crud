import psycopg2
from psycopg2 import sql, OperationalError


def connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="jaimin",
            password="root",
            host="localhost",
            port="5432",
        )
        cur = conn.cursor()
    #     create = """CREATE TABLE IF NOT EXISTS accounts (
    # id SERIAL PRIMARY KEY,
    # ac_no INT NOT NULL UNIQUE,
    # first_name VARCHAR(100),
    # last_name VARCHAR(100),
    # city VARCHAR(100)
    #     );"""

    #     cur.execute(create)

        post_query = "INSERT INTO accounts (ac_no, first_name, last_name, city) VALUES (%s, %s, %s, %s);"
        values = (5541, "jaimin", "patel", "surat")
        cur.execute(post_query, values)

        conn.commit()
        print("Data inserted successfully!")
        return "Success"

    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return "Connection error"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "General error"

    finally:
        try:
            cur.close()
            conn.close()
        except NameError:
            pass


# Call the function
print(connection())
