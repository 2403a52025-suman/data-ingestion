from databases import Database

# SQLite database file
DATABASE_URL = "sqlite:///./records.db"

# Create database connection
database = Database(DATABASE_URL)
