import sqlite3

def create_tables(db_name='BinanceApi.db'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the 'Data candles' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_candles (
            Id INTEGER PRIMARY KEY,
            date INT, 
            high REAL, 
            low REAL, 
            open REAL, 
            close REAL, 
            volume REAL
        )
    ''')

    # Create the 'Full data set' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS full_data_set (
            Id INTEGER PRIMARY KEY,
            uuid TEXT, 
            traded_crypto REAL, 
            price REAL,
            created_at_int INT, 
            side TEXT
        )
    ''')

    # Create the 'Keeping track of updates' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS last_checks (
            Id INTEGER PRIMARY KEY,
            exchange TEXT, 
            trading_pair TEXT, 
            duration TEXT,
            table_name TEXT, 
            last_check INT, 
            startdate INT, 
            last_id INT
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()