import hmac
import hashlib
import bcrypt
import re
import dp

def createMac(price):
    secret_key = b"SUPERSECRETKEYAKSFBJKASBFJKASK"
    price = str(price).encode("utf-8")
    mac = hmac.new(secret_key, price, hashlib.sha256).hexdigest()
    
    return mac

def get_product_by_id(product_list, product_id):
    for product in product_list:
        if product["id"] == product_id:
            return product
    return None

def get_real_total(cart, connection):
    total = 0
    for item in cart:
        real_product = dp.get_product_By_ID(connection, item["id"])
        total += real_product[2] * item["quantity"]
    return total    


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password.decode()


def is_password_match(entered_password, stored_hash):
    stored_hash_bytes = stored_hash.encode()

    return bcrypt.checkpw(entered_password.encode(), stored_hash_bytes)


def is_strong_password(password):
    min_length = 8
    require_uppercase = True
    require_lowercase = True
    require_digit = True
    require_special_char = True

    if len(password) < min_length:
        return False

    if require_uppercase and not any(char.isupper() for char in password):
        return False

    if require_lowercase and not any(char.islower() for char in password):
        return False

    if require_digit and not any(char.isdigit() for char in password):
        return False

    if require_special_char and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True
