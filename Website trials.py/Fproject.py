from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Set up upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Homepage
@app.route('/')
def homepage():
    return render_template('index.html')

# Tournaments Page
@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html')

# Shop Page
@app.route('/shop')
def shop():
    return render_template('shop.html')

# Blog Page
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Image Upload Page for Admins
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser may also submit an empty part
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('homepage'))
    return render_template('upload.html')

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # For now, simply print the form values (you can integrate email services later)
        print(f"Received message from {name} ({email}): {message}")
        return redirect(url_for('homepage'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

# Additional templates for sections overview on the homepage
# HTML placeholders in templates/index.html
# Ensure custom photo uploads for verified admins (use image upload paths)
# 1. Shop overview section
# 2. Tournaments overview section
# 3. Blog overview section
from flask import session

# Dummy admin credentials (Replace these in production)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in as admin')
            return redirect(url_for('upload_image'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully')
    return redirect(url_for('homepage'))

# Update the upload route to restrict access to admins
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    # Restrict upload access to admin only
    if not session.get('admin_logged_in'):
        flash('Access denied! Please log in as admin.')
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('homepage'))
    return render_template('upload.html')
