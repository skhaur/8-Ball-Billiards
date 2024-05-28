import Physics

def reset_and_create_db():
    # Initialize the Database with reset=True to clear the existing database
    db = Physics.Database(reset=True)
    
    # Call createDB to recreate the database structure
    db.createDB()
    
    print("Database has been reset and recreated.")

# Run the reset and create DB process
reset_and_create_db()