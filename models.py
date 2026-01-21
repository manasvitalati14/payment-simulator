from datetime import datetime
from extensions import db, login_manager
from flask_login import UserMixin
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    
    # Payment specific
    upi_id = db.Column(db.String(50), unique=True, nullable=False)
    wallet_balance = db.Column(db.Float, default=5000.0) # Signing bonus simulation
    pin_hash = db.Column(db.String(60), nullable=False)
    
    # Relationships
    sent_transactions = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender', lazy=True)
    received_transactions = db.relationship('Transaction', foreign_keys='Transaction.receiver_id', backref='receiver', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.upi_id}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_ref_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()).replace('-', '').upper()[:12]) # Shorter ID like banks
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='SUCCESS') # SUCCESS, FAILED, PENDING
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(100))
    
    def __repr__(self):
        return f"Transaction('{self.transaction_ref_id}', '{self.amount}', '{self.status}')"
