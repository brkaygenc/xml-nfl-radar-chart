import os
from urllib.parse import urlparse
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection_params():
    """
    Get database connection parameters from environment variables.
    Prioritizes DATABASE_URL if available, falls back to individual parameters.
    """
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Parse the DATABASE_URL
        parsed = urlparse(database_url)
        return {
            'dbname': parsed.path[1:],  # Remove leading slash
            'user': parsed.username,
            'password': parsed.password,
            'host': parsed.hostname,
            'port': parsed.port
        }
    else:
        # Use individual parameters
        return {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }

def get_db_connection():
    """
    Create and return a database connection.
    """
    try:
        params = get_connection_params()
        connection = psycopg2.connect(**params)
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def test_connection():
    """
    Test the database connection and print the server version.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()
        print(f"Successfully connected to the database. Server version: {version[0]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return False

if __name__ == '__main__':
    test_connection() 