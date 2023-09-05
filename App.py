from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import bcrypt
import logging
from logging.handlers import RotatingFileHandler
import secrets  # Import the secrets module

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'word_processor_db'

# Configure logging
app.logger.setLevel(logging.DEBUG)  # Set the logging level (you can adjust this)
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)  # Log to a file
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)

mysql = MySQL(app)

@app.route('/')
def index():
    app.logger.info('Received request to the index page')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # Encode password bytes
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registration successful. Please log in.', 'success')
        app.logger.info('User registered successfully: %s', username)
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # Encode password bytes
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        
        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
            session['user_id'] = user[0]
            app.logger.info('Login successful: %s', username)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'error')
            app.logger.warning('Login failed for user: %s', username)
            return redirect(url_for('index'))
    else:
        # Render the login form for GET requests
        return render_template('login.html')  # Assuming login.html is in the templates folder

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        username = None
        if 'user_id' in session:
            user_id = session['user_id']
            # Fetch user-specific data from the database and render the dashboard
            # You can add this logic here

            # For demonstration purposes, we'll assume you have a 'users' table
            # and fetch the username associated with the session user_id.
            cur = mysql.connection.cursor()
            cur.execute("SELECT username FROM users WHERE id = %s", [user_id])
            result = cur.fetchone()
            if result:
                username = result[0]
            cur.close()

        app.logger.info('Accessed the dashboard for user: %s', username)
        return render_template('dashboard.html', username=username, show_logout=True) # Pass show_logout=True
    else:
        flash('Please log in to access the dashboard.', 'info')
        app.logger.info('Unauthorized access to dashboard')
        return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('Logged out successfully.', 'success')
        app.logger.info('User logged out')
        return redirect(url_for('index'))

@app.route('/new_document')
def new_document():
    # Check if the user is logged in before allowing access to the new document page
    if 'user_id' in session:
        username = None
        if 'user_id' in session:
            user_id = session['user_id']
            # Fetch user-specific data from the database
            # For demonstration purposes, we'll assume you have a 'users' table
            # and fetch the username associated with the session user_id.
            cur = mysql.connection.cursor()
            cur.execute("SELECT username FROM users WHERE id = %s", [user_id])
            result = cur.fetchone()
            if result:
                username = result[0]
            cur.close()

        app.logger.info('Accessed the new document page for user: %s', username)
        return redirect(url_for('word_processor_route'))
    else:
        flash('Please log in to access this feature.', 'info')
        app.logger.info('Unauthorized access to new document page')
        return redirect(url_for('login'))

@app.route('/word_processor')
def word_processor_route():
    # Check if the user is logged in before allowing access to the word processor page
    if 'user_id' in session:
        username = None
        if 'user_id' in session:
            user_id = session['user_id']
            # Fetch user-specific data from the database
            # For demonstration purposes, we'll assume you have a 'users' table
            # and fetch the username associated with the session user_id.
            cur = mysql.connection.cursor()
            cur.execute("SELECT username FROM users WHERE id = %s", [user_id])
            result = cur.fetchone()
            if result:
                username = result[0]
            cur.close()

        app.logger.info('Accessed the word processor route for user: %s', username)
        return render_template('word_processor.html')  # Render the word processor HTML template
    else:
        flash('Please log in to access this feature.', 'info')
        app.logger.info('Unauthorized access to word processor route')
        return redirect(url_for('login'))


@app.route('/register.html')
def register_html():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
