from flask import Flask, send_from_directory, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='')
app.secret_key = 'your_secret_key'  # Needed for flash messages

# MySQL connection config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'demo'
}

@app.route('/')
def serve_login():
    return send_from_directory('', 'login.html')

@app.route('/signup', methods=['GET', 'POST'])
def serve_signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if not email or not password or not confirm_password:
            flash('Please fill all fields')
            return redirect(url_for('serve_signup'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('serve_signup'))

        hashed_password = generate_password_hash(password)

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Signup successful! Please login.')
            return redirect(url_for('serve_login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
            return redirect(url_for('serve_signup'))

    return send_from_directory('', 'signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Please fill all fields')
        return redirect(url_for('serve_login'))

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            return redirect(url_for('serve_welcome'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('serve_login'))
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
        return redirect(url_for('serve_login'))

@app.route('/welcome')
def serve_welcome():
    return send_from_directory('', 'welcome.html')

@app.route('/forgot-password')
def serve_forgot_password():
    return send_from_directory('', 'forget_password.html')

@app.route('/style.css')
def serve_css():
    return send_from_directory('', 'style.css')

if __name__ == '__main__':
    app.run(debug=True)
