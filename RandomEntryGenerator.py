import sqlite3
from faker import Faker
import random

# Initialize Faker for generating random data
fake = Faker()

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Define the SQL command to create the table
student_table = """
CREATE TABLE IF NOT EXISTS StudentDetails (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentName TEXT NOT NULL,
    Gender TEXT,
    Age INTEGER,
    Contact INTEGER,
    Course TEXT,
    Email TEXT UNIQUE NOT NULL,
    Pass TEXT NOT NULL DEFAULT 'user@123'
)
"""
cursor.execute(student_table)
conn.commit()

# Restrict the list of sample courses to only 'Java', 'C++', and 'Python'
courses = ['Java', 'C++', 'Python']

# Function to insert random data into StudentDetails table
def insert_random_data(num_records):
    for _ in range(num_records):
        name = fake.name()
        gender = random.choice(['Male', 'Female', 'Other'])
        age = random.randint(18, 30)
        contact = fake.unique.random_number(digits=10, fix_len=True)
        course = random.choice(courses)
        email = fake.unique.email()
        password = "user@123"

        # Insert record into StudentDetails table
        cursor.execute("""
            INSERT INTO StudentDetails (StudentName, Gender, Age, Contact, Course, Email, Pass)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, gender, age, contact, course, email, password))

    # Commit changes to the database
    conn.commit()
    print(f"Inserted {num_records} records into StudentDetails table.")

# Insert 10 random records
insert_random_data(50)

# Close the database connection
conn.close()
