import os
import sys

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-payment-sim-secret-key'
    
    # Database Configuration
    uri = os.environ.get('DATABASE_URL')
    
    # Fix for Postgres URLs (SQLAlchemy requires postgresql://)
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    # Fallback logic for Vercel/Serverless
    if not uri:
        # Check if running in a read-only environment (heuristic)
        # On Vercel, usually we want to fail or use /tmp if just testing
        if os.environ.get('VERCEL'):
            print("WARNING: No DATABASE_URL set. Using ephemeral SQLite in /tmp.")
            uri = 'sqlite:////tmp/site.db'
        else:
            uri = 'sqlite:///site.db'

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Print config info to logs (safe version)
    print(f"Loaded config. DB URI Type: {uri.split(':')[0] if uri else 'None'}")
