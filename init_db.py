import sqlite3
import os

def init_database():
    db_path = os.path.join(os.path.dirname(__file__), 'student.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME TEXT NOT NULL,
        CLASS TEXT NOT NULL,
        SECTION TEXT NOT NULL
    )
    ''')
    
    # Sample data
    sample_data = [
        ('John Doe', 'Data Science', 'A'),
        ('Jane Smith', 'Computer Science', 'B'),
        ('Bob Wilson', 'Data Science', 'A'),
        ('Alice Brown', 'Mathematics', 'C'),
        ('Charlie Davis', 'Computer Science', 'B')
    ]
    
    # Clear existing data and insert new data
    cursor.execute('DELETE FROM STUDENT')
    cursor.executemany('INSERT INTO STUDENT VALUES (?, ?, ?)', sample_data)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()


# import sqlite3
# import os

# def init_database():
#     # Get the absolute path
#     db_path = os.path.join(os.path.dirname(__file__), 'student.db')
    
#     # Create or connect to database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     # Drop table if exists and create new one
#     cursor.execute('DROP TABLE IF EXISTS STUDENT')
#     cursor.execute('''
#     CREATE TABLE STUDENT (
#         NAME TEXT NOT NULL,
#         CLASS TEXT NOT NULL,
#         SECTION TEXT NOT NULL
#     )
#     ''')
    
#     # Insert sample data
#     sample_data = [
#         ('John Doe', 'Data Science', 'A'),
#         ('Jane Smith', 'Computer Science', 'B'),
#         ('Bob Wilson', 'Data Science', 'A'),
#         ('Alice Brown', 'Mathematics', 'C'),
#         ('Charlie Davis', 'Computer Science', 'B')
#     ]
    
#     cursor.executemany('INSERT INTO STUDENT VALUES (?, ?, ?)', sample_data)
#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     init_database()
#     print("Database initialized successfully!")