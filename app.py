from flask import Flask, redirect, url_for, session, flash, render_template  # type: ignore
from modules.auth import auth_bp  # 👈 Import your blueprint
from modules.product import product_bp  # 👈 Import your blueprint



app = Flask(__name__)
app.secret_key = 'secret'  # Replace with a secure key

app.register_blueprint(auth_bp)  # 👈 Register blueprint
app.register_blueprint(product_bp) # 👈 Register blueprint

@app.route('/logout')
def logout():
    
    session.clear()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
