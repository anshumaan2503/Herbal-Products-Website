from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = 'your_secret_key'  # Add a secret key for sessions


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATABASE_URL = os.environ.get('DATABASE_URL')  # Render sets this automatically

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price TEXT,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ✅ Home page - Show all products
@app.route('/')
def home():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# Admin login page
@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple hardcoded admin credentials
        if username == 'admin' and password == '123':
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Admin logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# Protect dashboard route
@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', products=products)

# Protect add-product route
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']

        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, description, price, image) VALUES (%s, %s, %s, %s)",
                           (name, description, price, image_filename))
            conn.commit()
            conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_product.html')

# Protect delete route
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Fetch image filename before deletion
    cursor.execute("SELECT image FROM products WHERE id = %s", (product_id,))
    image = cursor.fetchone()

    # Delete from database
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()

    # Delete image file from disk
    if image and image[0]:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image[0])
        if os.path.exists(image_path):
            os.remove(image_path)

    return redirect(url_for('dashboard'))

# Change /admin to redirect to login
@app.route('/admin')
def admin():
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
