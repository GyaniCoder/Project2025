from flask import Flask, redirect, url_for, session, flash  # type: ignore
from modules.auth import auth_bp  # 👈 Import your blueprint

app = Flask(__name__)
app.secret_key = 'secret'  # Replace with a secure key

app.register_blueprint(auth_bp)  # 👈 Register blueprint

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return "Welcome to Clerq – your AI-powered business assistant!"

if __name__ == '__main__':
    app.run(debug=True)
