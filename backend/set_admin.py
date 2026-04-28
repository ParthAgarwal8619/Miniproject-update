import sqlite3

conn = sqlite3.connect("email_history.db")
c = conn.cursor()

c.execute("UPDATE users SET role='admin' WHERE email='parth8619agrawal@gmail.com'")

conn.commit()
conn.close()

print("Admin set successfully")
