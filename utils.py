import hmac
import hashlib

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

def get_real_total(cart, product_list):
    total = 0
    for item in cart:
        real_product = get_product_by_id(product_list, item["id"])
        total += real_product["price"] * item["quantity"]
    return total    
