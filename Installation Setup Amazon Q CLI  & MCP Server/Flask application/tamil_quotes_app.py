from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import random

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tamil_quotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    quotes = db.relationship('Quote', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    english_translation = db.Column(db.Text)
    source = db.Column(db.String(200))
    category = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)

# Sample quotes data
sample_quotes = [
    {
        'content': 'கற்றது கைமண் அளவு, கல்லாதது உலகளவு',
        'english_translation': 'What you have learned is a handful of sand; what you have yet to learn is the size of the world',
        'source': 'Tamil Proverb',
        'category': 'Education'
    },
    {
        'content': 'யானை இருக்க நாய் குரைத்தது போல',
        'english_translation': 'Like a dog barking at an elephant',
        'source': 'Tamil Proverb',
        'category': 'Wisdom'
    },
    {
        'content': 'அன்புக்கும் உண்டோ அடைக்கும் தாழ்',
        'english_translation': 'Can love be locked behind doors?',
        'source': 'Thirukkural',
        'category': 'Love'
    }
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    quotes = Quote.query.order_by(Quote.date_added.desc()).all()
    return render_template('index.html', quotes=quotes)

@app.route('/random')
def random_quote():
    quotes_count = Quote.query.count()
    if quotes_count > 0:
        random_index = random.randint(0, quotes_count - 1)
        quote = Quote.query.offset(random_index).first()
        return render_template('quote.html', quote=quote)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        user_exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if user_exists:
            flash('Username or email already exists')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_quote', methods=['GET', 'POST'])
@login_required
def add_quote():
    if request.method == 'POST':
        content = request.form.get('content')
        english_translation = request.form.get('english_translation')
        source = request.form.get('source')
        category = request.form.get('category')
        
        new_quote = Quote(
            content=content,
            english_translation=english_translation,
            source=source,
            category=category,
            user_id=current_user.id
        )
        
        db.session.add(new_quote)
        db.session.commit()
        
        flash('Quote added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_quote.html')

@app.route('/like/<int:quote_id>')
@login_required
def like_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    quote.likes += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/category/<category>')
def category(category):
    quotes = Quote.query.filter_by(category=category).all()
    return render_template('category.html', quotes=quotes, category=category)

@app.route('/user/<username>')
def user_quotes(username):
    user = User.query.filter_by(username=username).first_or_404()
    quotes = Quote.query.filter_by(user_id=user.id).all()
    return render_template('user_quotes.html', quotes=quotes, user=user)

# Initialize the database and add sample quotes
@app.before_first_request
def initialize_database():
    db.create_all()
    
    # Check if there are any users
    if User.query.count() == 0:
        # Create admin user
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        # Add sample quotes
        for quote_data in sample_quotes:
            quote = Quote(
                content=quote_data['content'],
                english_translation=quote_data['english_translation'],
                source=quote_data['source'],
                category=quote_data['category'],
                user_id=admin.id
            )
            db.session.add(quote)
        
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
