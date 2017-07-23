import datetime
import sqlite3
conn = sqlite3.connect('dishes.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE dishes
             (ts timestamp, brightness real, qty real)''')


#dishes = 1
# Insert a row of data
#c.execute("INSERT INTO dishes VALUES (?, ?)",(datetime.datetime.now(), dishes) )

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
