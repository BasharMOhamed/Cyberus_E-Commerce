import utils
def connect_to_database(name='database.db'):
    import sqlite3
    return sqlite3.connect(name, check_same_thread=False)

###################################################################################################################
#                                                 USERS

def init_users_db(connection):
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            photo_name TEXT NOT NULL
        )
    ''')
    connection.commit()
    
def add_user(connection, username, password, photo_name):
    cursor = connection.cursor()
    hashed_password = utils.hash_password(password)
    query = '''INSERT INTO users (username, password, photo_name) VALUES (?, ?, ?)'''
    cursor.execute(query, (username, hashed_password, photo_name))
    connection.commit()


def get_user(connection, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE username = ?'''
    cursor.execute(query, (username,))
    return cursor.fetchone()


def update_user(connection , user_data):
    cursor = connection.cursor()
    query = ''' UPDATE users set fname = ? , lName = ? , creditCard = ? WHERE username = ? '''
    cursor.execute(query,(user_data['fname'] , user_data['lname'] , user_data['card'] , user_data['username']))
    connection.commit() 


def update_photo(connection, filename , username):
    cursor = connection.cursor()  
    query = '''UPDATE users SET photo_name = ? WHERE username = ?'''
    cursor.execute(query, (filename,username))  
    connection.commit()  


def get_all_users(connection):
    cursor = connection.cursor()
    query = 'SELECT * FROM users'
    cursor.execute(query)
    return cursor.fetchall()    

def search_users(connection, search_query):
    cursor = connection.cursor()
    query = '''SELECT username FROM users WHERE username LIKE ?'''
    cursor.execute(query, (f"%{search_query}%",))
    return cursor.fetchall()

def is_admin(conncetion, username):
    user = get_user(conncetion, username)
    if user[3]:
        return True
    return False

###################################################################################################################
#                                                 PRODUCTS 

def init_products_db(connection):
    cursor = connection.cursor()
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            image_url TEXT NOT NULL
        )
                   ''')
    connection.commit()
    
def add_product(connection, product_name, product_price, image_url):
    cursor = connection.cursor()
    query = '''INSERT INTO products (name, price, image_url) VALUES (?, ?, ?)
    '''
    cursor.execute(query, (product_name, int(product_price), image_url))
    connection.commit()

def get_all_products(connection):
    cursor = connection.cursor()
    query = 'SELECT * FROM products'
    cursor.execute(query)
    return cursor.fetchall()

def get_product_By_ID(connection, product_id):
    cursor = connection.cursor()
    query = 'SELECT * FROM products WHERE id=?'
    cursor.execute(query, (product_id,))
    return cursor.fetchone()

###################################################################################################################
#                                                 COMMENTS 


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
