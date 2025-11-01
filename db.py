import sqlite3

# Connect to the database
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Create the table if it doesn't exist
# query = """
# CREATE TABLE IF NOT EXISTS sys_command (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(100),
#     path VARCHAR(1000)
# )
# """
# cursor.execute(query)

# # Insert the value
 #insert_query = "INSERT INTO sys_command VALUES (NULL, ?, ?)"
#cursor.execute(insert_query, ('notepad++', 'C:/Program Files/Notepad++/notepad++.exe'))

query = """
CREATE TABLE IF NOT EXISTS web_command (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    url VARCHAR(1000)
)
"""
cursor.execute(query)

insert_query = "INSERT INTO web_command VALUES (NULL, ?, ?)"
cursor.execute(insert_query, ('chatgpt', 'https://www.chatgpt.com'))

# Commit the transaction




# 1. Create the contacts table if it doesn't exist
# create_query = """
# CREATE TABLE IF NOT EXISTS contacts (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(100),
#     mobile_no VARCHAR(20)
# )
# """
# cursor.execute(create_query)

# # 2. Insert contact data
# insert_query = "INSERT INTO contacts VALUES (NULL, ?, ?)"
# cursor.execute(insert_query, ('Nikita', '8669868639'))  # Change name & number as needed

# Commit and close
con.commit()
con.close()
