import sqlite3


conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
#generation.to_sql('Stromzeiten_app_generation', conn, if_exists='replace', index = False)

c.execute('''  
SELECT * FROM Stromzeiten_app_generation
          ''')

#c.execute("SELECT name FROM sqlite_master WHERE type='table';")

for row in c.fetchall():
    print(row)