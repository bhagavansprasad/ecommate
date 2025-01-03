import psycopg2
from psycopg2 import sql
from datetime import datetime

# Database connection details
DB_DETAILS = {
    "database": "qcommerce",
    "user": "qadmin",
    "password": "jnjnuh",
    "host": "localhost",
    "port": "5432"
}

# Establish the connection
def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_DETAILS)
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to create tables if they don't exist
def create_tables():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        # Create roles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                role_name VARCHAR(125) NOT NULL,
                role_description VARCHAR(250) NOT NULL,
                created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(125),
                modified_on TIMESTAMP,
                modified_by VARCHAR(125),
                active_flag SMALLINT NOT NULL DEFAULT 1
            );
        """)

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_first_name VARCHAR(125) NOT NULL,
                user_last_name VARCHAR(125) NOT NULL,
                user_e_mail_id VARCHAR(125),
                user_phone_number VARCHAR(125),
                user_login_id VARCHAR(125) NOT NULL,
                user_password VARCHAR(250) NOT NULL,
                client_id INTEGER NOT NULL,
                created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(125),
                modified_on TIMESTAMP,
                modified_by VARCHAR(125),
                active_flag SMALLINT NOT NULL DEFAULT 1
            );
        """)

        # Create user_roles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_roles (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(125),
                modified_on TIMESTAMP,
                modified_by VARCHAR(125),
                active_flag SMALLINT NOT NULL DEFAULT 1
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()

# Function to insert data into roles table
def insert_roles():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        roles = [
            ('user', 'Regular user role'),
            ('admin', 'Administrator role'),
            ('finops', 'Financial operations role')
        ]

        for role in roles:
            cursor.execute("""
                INSERT INTO roles (role_name, role_description)
                SELECT %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM roles WHERE role_name = %s);
            """, (role[0], role[1], role[0]))

        conn.commit()
        cursor.close()
        conn.close()

# Function to insert data into users table
def insert_users():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        users = [
            ('Sudhkar', 'kss', 'sudhakar.kss@dataworkx.ai', '9901322079', 'sudhakar', 'sjnjnuh', 1),
            ('Bhagavan', 'Prasad', 'bhagavansprasad@gmail.com', '9902096750', 'bhagavan', 'bjnjnuh', 1),
            ('Ikshwak', 'Varma', 'Ikshwakv@gmail.com', '9347273322', 'ikshwak', 'ijnjnuh', 1),
            ('Likhita', 'B', 'likhitabeekam@gmail.com', '6303654186', 'likhita', 'ljnjnuh', 1),
            ('Saketh', 'Ram', 'sakethramsettipalli2003@gmail.com', '9008774173', 'saketh', 'sjnjnuh', 1)
        ]


        for user in users:
            cursor.execute("""
                INSERT INTO users (user_first_name, user_last_name, user_e_mail_id, user_phone_number, user_login_id, user_password, client_id)
                SELECT %s, %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM users WHERE user_login_id = %s);
            """, (*user, user[4]))

        conn.commit()
        cursor.close()
        conn.close()

# Function to insert data into user_roles table
def insert_user_roles():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        # Example roles mapping
        user_roles = [
            (1, 1),  # Sudhkar -> user role
            (2, 2),  # Bhagavan -> admin role
            (3, 3),  # Ikshwak -> finops role
            (4, 1),  # Likhita -> user role
            (5, 2)   # Saketh -> admin role
        ]

        for user_role in user_roles:
            cursor.execute("""
                INSERT INTO user_roles (user_id, role_id)
                SELECT %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM user_roles WHERE user_id = %s AND role_id = %s);
            """, (user_role[0], user_role[1], user_role[0], user_role[1]))

        conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
    insert_roles()
    insert_users()
    insert_user_roles()
    print("Tables created and data inserted successfully.")
