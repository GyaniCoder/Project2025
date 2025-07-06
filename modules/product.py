from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import sqlite3

product_bp = Blueprint('product_bp', __name__)

DB_PATH = 'db/clerq.db'

@product_bp.route('/products')
def list_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        conn.close()

        return redirect(url_for('product_bp.list_products'))

    return render_template('add_product.html')

@product_bp.route('/delete-product/<int:id>')
def delete_product(id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('product_bp.list_products'))

@product_bp.route('/api/edit_product/<int:product_id>', methods=['POST'])
def edit_product_ajax(product_id):
    if 'user_id' not in session:
        return jsonify({ "status": "unauthorized" }), 401

    data = request.get_json()
    name = data.get("name")
    price = float(data.get("price"))
    quantity = int(data.get("quantity", 0))  # Optional: to add stock

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch current quantity
    cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return jsonify({ "status": "error", "message": "Product not found" }), 404

    current_quantity = result[0]
    new_quantity = current_quantity + quantity

    # Update product
    cursor.execute("""
        UPDATE products
        SET name = ?, price = ?, quantity = ?
        WHERE id = ?
    """, (name, price, new_quantity, product_id))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "product": {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": new_quantity
        }
    })

@product_bp.route('/api/delete_product/<int:product_id>', methods=['POST'])
def delete_product_ajax(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return jsonify({ "status": "success", "id": product_id })