# implementation_plan.md

## Project: Digital Payment Simulator (Flask + MySQL/SQLite)

This project is a digital payment simulator inspired by Google Pay/PhonePe. It allows users to register, manage a wallet, and simulate transactions.

## Technology Stack
- **Backend**: Python (Flask)
- **Database**: SQLAlchemy (Configurable for MySQL, defaulting to SQLite for immediate run capability in this environment since MySQL client was not found)
- **Frontend**: HTML5, CSS3 (Modern, Premium UI), JavaScript (Vanilla)

## Directory Structure
```
/payment_simulator
    /static
        /css
            style.css
            animations.css
        /js
            script.js
        /images
            (Generated assets)
    /templates
        base.html
        login.html
        register.html
        dashboard.html
        transfer.html
        history.html
        profile.html
    app.py
    models.py
    config.py
    requirements.txt
```

## Features & Implementation Steps

### 1. Project Setup
- Create directory structure.
- Create `requirements.txt` (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, PyMySQL).
- Install dependencies.

### 2. Database Models (`models.py`)
- **User**: id, username, email, password_hash, phone_number, upi_id, pin_hash, balance.
- **Transaction**: id, transaction_id (UUID), sender_id, receiver_id, amount, timestamp, status (SUCCESS, FAILED, PENDING), type (SENT/RECEIVED).

### 3. Backend Logic (`app.py` & `routes`)
- **Auth**: Register, Login, Logout (using Flask-Login).
- **Wallet**: Check balance.
- **Transfer Logic**:
    - Verify Receiver (UPI or Phone).
    - Verify Balance.
    - Verify PIN.
    - Transaction Simulation (random failures/pending for realism).
    - Atomic updates to balances.
- **API**: REST endpoints for AJAX calls from frontend (checking user existence, processing payment).

### 4. Frontend Design (Premium Aesthetics)
- **Theme**: Glassmorphism, smooth gradients (Deep Violet/Blue to vibrant accents).
- **Components**:
    - Animated Credit Card/Wallet Balance card.
    - Contact list with avatars.
    - Transaction history list with status icons.
- **Interactions**:
    - PIN entry modal.
    - Success/Failure animations (Lottie or CSS keyframes).

### 5. Step-by-Step Execution
1.  **Initialize**: Setup folders and install `flask flask-sqlalchemy flask-login flask-bcrypt pymysql`.
2.  **Config**: Setup `config.py` with SQLAlchemy URI.
3.  **Models**: Define User and Transaction tables.
4.  **Routes**: Implement auth and dashboard routes.
5.  **Templates**: Create `base.html` and core pages with premium CSS.
6.  **Logic**: Implement the "Pay" functionality with PIN verification and DB updates.
7.  **Refine**: Add status simulation and history view.

## Notes
- Will use `sqlite:///pay_sim.db` by default so the app runs out-of-the-box.
- Will include instructions to switch to `mysql+pymysql://user:pass@localhost/db_name` in `config.py`.
