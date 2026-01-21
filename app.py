from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from config import Config
from extensions import db, bcrypt, login_manager
from models import User, Transaction
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import random

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hashed_pin = bcrypt.generate_password_hash(form.pin.data).decode('utf-8')
        upi_id = f"{form.phone.data}@paysim"
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, 
                    password=hashed_password, pin_hash=hashed_pin, upi_id=upi_id)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! Your UPI ID is {upi_id}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    transactions = Transaction.query.filter((Transaction.sender_id == current_user.id) | (Transaction.receiver_id == current_user.id)).order_by(Transaction.timestamp.desc()).limit(5).all()
    return render_template('dashboard.html', transactions=transactions, user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/setup")
def setup():
    db.create_all()
    return "Database tables created successfully!"

@app.route("/api/verify_user", methods=['POST'])
@login_required
def verify_user():
    data = request.get_json()
    identifier = data.get('identifier') # UPI or Phone
    
    # Simple logic regarding @paysim
    if '@' not in identifier and len(identifier) >= 10:
        identifier = f"{identifier}@paysim"

    user = User.query.filter((User.upi_id == identifier) | (User.phone == identifier)).first()
    
    if user and user.id != current_user.id:
        return jsonify({'status': 'found', 'name': user.username, 'upi': user.upi_id})
    elif user and user.id == current_user.id:
        return jsonify({'status': 'error', 'message': 'You cannot pay yourself'})
    return jsonify({'status': 'not_found'})

@app.route("/api/pay", methods=['POST'])
@login_required
def pay():
    data = request.get_json()
    receiver_upi = data.get('receiver_upi')
    try:
        amount = float(data.get('amount'))
    except ValueError:
        return jsonify({'status': 'failed', 'message': 'Invalid amount'})
        
    pin = data.get('pin')
    
    # 1. Verify PIN
    if not bcrypt.check_password_hash(current_user.pin_hash, pin):
        return jsonify({'status': 'failed', 'message': 'Incorrect PIN'})
        
    # 2. Check Balance
    if current_user.wallet_balance < amount:
        return jsonify({'status': 'failed', 'message': 'Insufficient Balance'})
    
    # 3. Find Receiver
    receiver = User.query.filter_by(upi_id=receiver_upi).first()
    if not receiver:
         return jsonify({'status': 'failed', 'message': 'Receiver not found'})

    # 4. Simulate Processing
    rand = random.random()
    status = 'SUCCESS'
    if rand > 0.95:
        status = 'FAILED'
    elif rand > 0.90:
        status = 'PENDING'
        
    # 5. Execute Transaction
    tx = Transaction(amount=amount, sender_id=current_user.id, receiver_id=receiver.id, status=status)
    db.session.add(tx)
    
    if status == 'SUCCESS':
        current_user.wallet_balance -= amount
        receiver.wallet_balance += amount
        
    db.session.commit()
    
    return jsonify({
        'status': status.lower(), 
        'transaction_id': tx.transaction_ref_id,
        'message': f'Payment {status}'
    })

@app.route("/history")
@login_required
def history():
    transactions = Transaction.query.filter((Transaction.sender_id == current_user.id) | (Transaction.receiver_id == current_user.id)).order_by(Transaction.timestamp.desc()).all()
    return render_template('history.html', transactions=transactions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
