import pyodbc
import argparse
import os
from mcp.server.fastmcp import FastMCP

print("Drivers ::")
print(pyodbc.drivers())

# Connection details
server = 'DESKTOP-DEEPA\SQLEXPRESS' 
database = 'Demo'
driver = '{ODBC Driver 18 for SQL Server}'

mcp = FastMCP('sqlserver-demo')

def init_db():
    # Connection string
    conn_str = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    Encrypt=no;
    Trusted_Connection=yes;
    """
    try:
        # Connect
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        print("Connected successfully!")
    except pyodbc.Error as e:
        print("Error connecting to SQL Server:", e)   

    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='People' AND xtype='U')
    CREATE TABLE People (
        Name VARCHAR(50),
        Profession NVARCHAR(50),
        Age INT
    )
    """
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("People Table created (if it didn't exist).")
    except pyodbc.Error as e:
        print("Error creating People Table in SQL Server DB:", e)

    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Contact' AND xtype='U')
    CREATE TABLE Contact (
        Name VARCHAR(50),
        Address VARCHAR(200),
        Phone varchar(20)
    )
    """
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("Contact Table created (if it didn't exist).")
    except pyodbc.Error as e:
        print("Error creating Contact Table in SQL Server DB:", e)
    conn.commit()
    return conn, cursor

@mcp.tool()
def add_data_to_people_table(query: str) -> bool:
    """Add new data to the people table using a SQL INSERT query.

    Args:
        query (str): SQL INSERT query following this format:
            INSERT INTO people (name, age, profession)
            VALUES ('John Doe', 30, 'Engineer')
        
    Schema:
        - name: Text field (required)
        - age: Integer field (required)
        - profession: Text field (required)
    
    Returns:
        bool: True if data was added successfully, False otherwise
    
    Example:
        >>> query = '''
        ... INSERT INTO people (name, age, profession)
        ... VALUES ('Alice Smith', 25, 'Developer')
        ... '''
        >>> add_data(query)
        True
    """

    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except pyodbc.Error as e:
        print(f"Error adding data in People Table: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def add_data_to_contact_table(query: str) -> bool:
    """Add new data to the contact table using a SQL INSERT query.

    Args:
        query (str): SQL INSERT query following this format:
            INSERT INTO contact (name, address, phone)
            VALUES ('John Doe', 30 Vaalmiki Street, '+91-91884-25345')
        
    Schema:
        - name: Text field (required)
        - address: Text field (required)
        - phone: Text field (required)
    
    Returns:
        bool: True if data was added successfully, False otherwise
    
    Example:
        >>> query = '''
        ... INSERT INTO contact (name, address, phone)
        ... VALUES ('Alice Smith', '25 Gandhi Street', '+1-678-998-9858')
        ... '''
        >>> add_data(query)
        True
    """

    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except pyodbc.Error as e:
        print(f"Error adding data in Contact Table: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def read_data_from_people_table(query: str = "SELECT * FROM people") -> list:
    """Read data from the people table using a SQL SELECT query.

    Args:
        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM people".
            Examples:
            - "SELECT * FROM people"
            - "SELECT name, age FROM people WHERE age > 25"
            - "SELECT * FROM people ORDER BY age DESC"
    
    Returns:
        list: List of tuples containing the query results.
              For default query, tuple format is (name, age, profession)
    
    Example:
        >>> # Read all records
        >>> read_data()
        [('John Doe', 30, 'Engineer'), ('Alice Smith', 25, 'Developer')]
        
        >>> # Read with custom query
        >>> read_data("SELECT name, profession FROM people WHERE age < 30")
        [('Alice Smith', 'Developer')]
    """

    conn, cursor = init_db()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Error reading data from People Table : {e}")
        return []
    finally:
        conn.close()


@mcp.tool()
def read_data_from_contact_table(query: str = "SELECT * FROM people") -> list:
    """Read data from the contact table using a SQL SELECT query.

    Args:
        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM contact".
            Examples:
            - "SELECT * FROM contact"
            - "SELECT * FROM contact ORDER BY name DESC"
    
    Returns:
        list: List of tuples containing the query results.
              For default query, tuple format is (name, address, phone)
    
    Example:
        >>> # Read all records
        >>> read_data()
        [('John Doe', '25 Gandhi Street', '+91-91548-85858'), ('Alice Smith', '25 Cherry Drive', '+1-678-999-5689')]
        
        >>> # Read with custom query
        >>> read_data("SELECT name, pphone FROM contact WHERE phone like '+1%')
        [('Alice Smith', '+1-678-895-5556')]
    """

    conn, cursor = init_db()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Error reading data from Contact Table : {e}")
        return []
    finally:
        conn.close()


if __name__ == "__main__":
    # Start the server
    print("🚀Starting server... ")

    # python server.py --server_type=sse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)
