import sqlite3
import Physics

# Replace 'your_db_name.db' with the actual name of your database file.
database_name = 'phylib.db'

# SQL statements to create indexes
create_index_queries = [
    'CREATE INDEX IF NOT EXISTS idx_gameid ON Game(GAMEID);',
    'CREATE INDEX IF NOT EXISTS idx_playerid ON Player(PLAYERID);',
    'CREATE INDEX IF NOT EXISTS idx_tableid ON TTable(TABLEID);',
    'CREATE INDEX IF NOT EXISTS idx_shotid ON Shot(SHOTID);'
]

# Connect to the SQLite database
conn = sqlite3.connect(database_name)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Execute the SQL commands to create indexes
for query in create_index_queries:
    cursor.execute(query)
    print(f"Executed: {query}")

# Commit your changes in the database
conn.commit()
print("Indexes created successfully.")

# Close the connection
cursor.close()
conn.close()
