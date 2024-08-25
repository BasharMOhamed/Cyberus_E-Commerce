
def connect_to_database(name='database.db'):
    import sqlite3
    return sqlite3.connect(name, check_same_thread=False)



def init_comments_table(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()

def add_comment(connection, username, text):
    cursor = connection.cursor()
    query = '''INSERT INTO comments (username, text) VALUES (?, ?)'''
    cursor.execute(query, (username, text))
    connection.commit()

def get_comments(connection):
    cursor = connection.cursor()
    query = '''
        SELECT comments.username, comments.text, comments.timestamp
        FROM comments
    '''
    cursor.execute(query)
    return cursor.fetchall()

def clear_comments(connection):
    cursor = connection.cursor()
    query = '''DELETE FROM comments'''
    cursor.execute(query)
    connection.commit()
