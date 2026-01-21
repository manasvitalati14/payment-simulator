import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-payment-sim-secret-key'
    
    # Database Configuration
    # IMPORTANT: For Vercel/Production, you must set DATABASE_URL environment variable to a PostgreSQL/MySQL URL.
    # SQLite (default below) WILL NOT persist data on Vercel because the filesystem is read-only/ephemeral.
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
