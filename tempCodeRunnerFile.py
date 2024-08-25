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
        return render_template("addproduct.html")        
    else:
        return redirect(url_for("login"))   