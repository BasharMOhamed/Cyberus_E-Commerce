from flask import Flask, render_template, request, session, redirect, url_for, flash
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import dp
from markupsafe import  Markup
import re
import validator, os

commentsConnection = dp.connect_to_database(name="comments.db")
dp.init_comments_table(commentsConnection)

usersConnection = dp.connect_to_database(name="users.db")
dp.init_users_db(usersConnection)

productsConnection = dp.connect_to_database(name="products.db")
dp.init_products_db(productsConnection)

app = Flask(__name__)
app.config['uploads'] = os.path.join(os.getcwd(), 'static/uploads')

limiter = Limiter(app=app, key_func=get_remote_address,
                  default_limits=["50 per minute"], storage_uri="memory://")


app.secret_key = 'SUPER_SECRET'

# TEMP
PRODUCTS = [
    {'id': 1, 'name': 'Laptop', 'price': 1000, "image_url":"data:image/jpeg;base64,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"},
    {'id': 2, 'name': 'Smartphone', 'price': 500, "image_url": "data:image/jpeg;base64,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"},
    {'id': 3, 'name': 'Headphones', 'price': 150,"image_url": "https://sony.scene7.com/is/image/sonyglobalsolutions/wh-ch720_Primary_image?$categorypdpnav$&fmt=png-alpha"},
]


#                       INDEX

@app.route("/")
@limiter.limit("10 per minute")
def index():
    if "username" in session:
        isAdmin = dp.is_admin(usersConnection, session["username"])
        products = dp.get_all_products(productsConnection)
        return render_template("shop.html", products = products, username = session["username"], isAdmin = isAdmin)
    else:
        return render_template("login.html")    


#                       LOGIN
@app.route("/auth", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dp.get_user(usersConnection, username)
        if user:
            print(user)
            if utils.is_password_match(password, user[2]):
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Wrong username or password")
        else:
            flash("wrong username", "danger") 
    return render_template("login.html")               





#                       REGISTER
@app.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirm_password")
        existingUser = dp.get_user(usersConnection, username)
        if existingUser:
            flash("Username already exists")
        else:
            if utils.is_strong_password(password): 
                if password == confirmPassword:
                    dp.add_user(usersConnection, username, password, "images.png")
                    return redirect(url_for("login"))
                else:
                    flash("Passwords does not match")
            else:
                flash("Password is not strong enough")         
    return render_template("register.html")    








#                       LOGOUT
@app.route("/logout", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def logout():
    session.pop("username")
    if "cart" in session:
        session.pop("cart")
    return redirect(url_for("index"))









#                       PROFILE
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:

        if request.method == 'GET':
            username = request.args.get('username')
            
            #               IDOR
            if(username != session["username"]):
                return "<h1>PERMISION DENIED [IDOR]</h1>"
            
            data = dp.get_user(usersConnection, username)
            if data:
                isAdmin = dp.is_admin(usersConnection, session["username"])
                print(data)
                return render_template('profile.html', data=data, isAdmin = isAdmin, username = session["username"])
            else:
                return "user not found"
        elif request.method == 'POST':
            form_type = request.form.get('form_name') 
            username = request.args.get('username', session['username'])
            
            #               IDOR
            if(username != session["username"]):
                return "<h1>PERMISION DENIED [IDOR]</h1>"
            
            if form_type == 'upload_photo':
                photo = request.files.get('profile_picture')
                if photo:
                    if not validator.allowed_file_size(photo):
                        return f"unallowed size."
                    elif not validator.allowed_file(photo.filename):
                        return f"unallowed extention."
                    else:
                        dp.update_photo(usersConnection, photo.filename, username)
                        photo.save(os.path.join(app.config['uploads'], photo.filename))
            elif form_type == 'update_user_data':
                user_data = { 
                    "username": session['username'], 
                    "fname": request.form.get('first_name'),
                    "lname": request.form.get('last_name'),
                    "card": request.form.get('card')
                }
                dp.update_user(usersConnection , user_data)
            
            data = dp.get_user(usersConnection, username)
            print(data)
            isAdmin = dp.is_admin(usersConnection,session["username"])
            return render_template('profile.html', data=data, isAdmin = isAdmin, username = session["username"]) 
    else:
        return redirect(url_for('login'))

    
#                       ADD PRODUCT
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'username' in session:
        if request.method == "POST":
            product_name = request.form.get('product_name')
            product_price = request.form.get('product_price')
            image_url = request.form.get('image_url')
            if not product_name or not product_price or not image_url:
                flash("Missing values")
            else:
                dp.add_product(productsConnection,product_name, product_price, image_url)
                return redirect(url_for("index"))
        return render_template("addproduct.html")        
    else:
        return redirect(url_for("login"))    
    
#                       COMMENTS    
@app.route("/comments", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def addComment():
    if  'username' in session:
        comments = dp.get_comments(commentsConnection)

        if request.method == 'POST':
            text = Markup(request.form['comment'])
            
            # TO PREVENT XSS
            text_str = str(text)
            cleaned_text = re.sub(r'<script.*?>.*?</script>', 'Prevented XSS Script BY BASHAR', text_str, flags=re.DOTALL)
            
            username = session.get('username')
            if username:
                dp.add_comment(commentsConnection, username, cleaned_text)
                comments = dp.get_comments(commentsConnection)
            else:
                flash("You must be logged in to post a comment.", "warning")
        isAdmin = dp.is_admin(usersConnection, session["username"])
        return render_template('comments.html', comments=comments, username = session["username"], isAdmin = isAdmin)
    else:
        return redirect(url_for('login'))
    
    
    
#                   CLEAR COMMENTS
@app.route('/clear_comments', methods=['GET','POST'])
def clearComments():
    dp.clear_comments(commentsConnection)
    return redirect(url_for('addComment'))        
    
    
    
#                       CART    
@app.route('/cart')
@limiter.limit("10 per minute")
def cart():
    if  'username' in session:
        cart = session.get('cart', [])
        total = sum(int(item['price']) * int(item['quantity']) for item in cart)
        return render_template('cart.html', cart=cart, total=total)
    else:
        return redirect(url_for('login'))

#                   ADD TO CART
@app.route('/add_to_cart', methods=["GET", "POST"])
@limiter.limit("50 per minute")
def add_to_cart():
    product_id = int(request.args.get('product_id'))
    product_name = request.args.get('product_name')
    price = int(request.args.get('price'))

    # Check if user is logged in
    if 'username' not in session:
        flash("You must be logged in to add items to your cart.", "warning")
        return redirect(url_for('login'))

    if not product_id or not price:
        flash("Invalid product or price.", "danger")
        return redirect(url_for('index'))

    # Store cart information in the session
    cart = session.get('cart', [])
    
    for item in cart:
        if item['name'] == product_name:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product_id, 'name': product_name, 'price': price, 'quantity': 1})
    session['cart'] = cart

    flash(f"Added product {product_id} with price {price} to your cart.", "success")
    return redirect(url_for('index'))



#                   INCREASE OR DECREASE
@app.route('/increase_decrease', methods=["GET",'POST'])
@limiter.limit("10 per minute")
def increase_decrease():
    if "username" in session:
        item_id = request.args.get("product_id")
        cart = session.get('cart', [])
        type = request.args.get("type")
        if not item_id or not cart or not type:
            return "something went wrong"
        if(type == "increase"):
            for item in cart:
                if item['id'] == int(item_id):
                    item['quantity'] += 1
                    break
        
        if(type == "decrease"):
            for item in cart:
                if item['id'] == int(item_id):
                    if(item['quantity'] > 1):
                        item['quantity'] -= 1
                        break
                    else:
                        cart.remove(item)
                        break
                                                
        session['cart'] = cart
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('login'))


#           CHECKOUT
@app.route("/checkout")
@limiter.limit("10 per minute")
def checkout():
    if  "username" in session:
        cart = session["cart"]
        real_total = utils.get_real_total(cart, productsConnection)
        session["MAC"] = utils.createMac(real_total)
        total = request.args.get("total")
        return render_template("checkout.html", total = total)
    else:
        return redirect(url_for('login'))


#           PAYMENT
@app.route("/confirm", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def confirm():
    if  "username" in session:
        total = request.args.get("total")
        current_MAC = utils.createMac(total)
        print(current_MAC)
        if("MAC" in session and current_MAC == session["MAC"]):
            return f"<h2>Purchase confirmed at price ${total}.</h2>"
        else:
            return f"<h2>Purchase Failed, Try Again..</h2>"
    else:
        return redirect(url_for('login'))



app.run(debug=True)