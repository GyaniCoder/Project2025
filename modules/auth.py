from flask import Blueprint, request, render_template, redirect, url_for, flash, session  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
import sqlite3  # type: ignore

auth_bp = Blueprint('auth_bp', __name__)

# 🔐 LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('db/clerq.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash("Invalid email or password")
            return redirect(url_for('auth_bp.login'))
    
    return render_template('login.html')

# 📝 REGISTER
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect('db/clerq.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
            conn.commit()
            flash('Registration successful!')
            return redirect(url_for('auth_bp.login'))
        except Exception as e:
            flash('Error: ' + str(e))
            return redirect(url_for('auth_bp.register'))
        finally:
            conn.close()

    return render_template ('register.html')

@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = sqlite3.connect('db/clerq.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return render_template('dashboard.html', email=user[0])
    else:
        return redirect(url_for('auth_bp.login'))


@auth_bp.route('/logout')
def logout():       
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('auth_bp.login'))       