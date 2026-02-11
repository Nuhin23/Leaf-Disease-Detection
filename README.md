# Leaf Disease Detection
# 🌿 Leaf Disease Detection System

A full-stack web application that detects plant leaf diseases using
Machine Learning and provides treatment recommendations.

## 👥 Team
- Member 1: Backend + Machine Learning
- Member 2: Frontend Development

## 🚀 Features
- User authentication (Login & Registration)
- Leaf image upload
- Disease prediction with confidence
- Treatment suggestions
- Detection history dashboard

## 🛠️ Tech Stack
**Frontend**
- HTML5, CSS3, Bootstrap 5
- Vanilla JavaScript

**Backend**
- Python Flask
- SQLAlchemy
- Flask-Login

**Machine Learning**
- TensorFlow / Keras
- CNN Model
- PlantVillage Dataset

**Database**
- SQLite

## 📁 Project Structure
- `frontend/` → UI & client-side logic
- `backend/` → API, database, ML logic

## ▶️ How to Run
1. Clone the repository
2. Setup backend virtual environment
3. Install requirements
4. Run Flask server

## 📜 License
Academic use only


🌿 Leaf Disease Detection – Full Stack Project Structure (Explained)
leaf-disease-detection/
│
├── backend/                        # 🔧 Backend + Machine Learning logic
│   │
│   ├── app.py                      # Main Flask application entry point
│   │                               # Initializes app, DB, login manager, blueprints
│   │
│   ├── config.py                   # Configuration file
│   │                               # Database URI, secret key, upload path, etc.
│   │
│   ├── requirements.txt            # Python dependencies (Flask, TensorFlow, etc.)
│   │
│   ├── .env                        # Environment variables (SECRET_KEY, DEBUG)
│   │
│   ├── README.md                   # Backend setup & API documentation
│   │
│   ├── database/
│   │   └── app.db                  # SQLite database file
│   │                               # Stores users & detection history
│   │
│   ├── models/                     # Database table models (ORM)
│   │   ├── __init__.py
│   │   ├── user.py                 # User table (id, name, email, password)
│   │   └── detection.py            # Detection table (image, disease, confidence)
│   │
│   ├── routes/                     # Flask Blueprints (API routes)
│   │   ├── __init__.py
│   │   ├── auth.py                 # Login, registration, logout routes
│   │   ├── dashboard.py            # Dashboard, profile, history routes
│   │   └── prediction.py           # Image upload & ML prediction endpoint
│   │
│   ├── ml/                         # 🤖 Machine Learning module
│   │   ├── dataset/                # Leaf images dataset (PlantVillage)
│   │   │
│   │   ├── notebooks/
│   │   │   └── training.ipynb       # Jupyter notebook for experiments & training
│   │   │
│   │   ├── model/
│   │   │   └── leaf_model.h5        # Trained CNN model file
│   │   │
│   │   ├── train.py                # Script to train ML model
│   │   ├── predict.py              # Loads model & predicts disease
│   │   └── treatment_rules.py      # Disease → Treatment recommendation mapping
│   │
│   ├── uploads/                    # Uploaded leaf images (user uploads)
│   │
│   └── tests/
│       └── test_api.py             # Backend API testing
│
├── frontend/                       # 🎨 Frontend (User Interface)
│   │
│   ├── templates/                  # HTML templates (Flask compatible)
│   │   ├── layouts/
│   │   │   └── base.html            # Common layout (navbar + footer)
│   │   │
│   │   ├── pages/
│   │   │   ├── landing.html         # Home / landing page
│   │   │   ├── login.html           # Login page
│   │   │   ├── register.html        # Registration page
│   │   │   ├── dashboard.html       # User dashboard
│   │   │   ├── history.html         # Previous detection history
│   │   │   └── profile.html         # User profile page
│   │   │
│   │   └── components/
│   │       ├── navbar.html          # Navigation bar component
│   │       ├── footer.html          # Footer component
│   │       ├── upload_card.html     # Image upload UI
│   │       └── result_card.html     # Disease result display UI
│   │
│   ├── static/                     # Static assets (CSS, JS, Images)
│   │   ├── css/
│   │   │   ├── main.css             # Global styles
│   │   │   ├── auth.css             # Login/Register styles
│   │   │   ├── dashboard.css        # Dashboard UI styles
│   │   │   └── responsive.css       # Mobile responsiveness
│   │   │
│   │   ├── js/
│   │   │   ├── main.js              # Global JS functions
│   │   │   ├── auth.js              # Form validation logic
│   │   │   ├── dashboard.js         # Upload & result UI logic
│   │   │   └── history.js           # Search & filter history table
│   │   │
│   │   └── images/
│   │       ├── logo.png             # Project logo
│   │       ├── hero-bg.jpg          # Landing page background
│   │       └── icons/               # UI icons
│   │
│   └── README.md                   # Frontend setup & UI guide
│
├── .gitignore                      # Files ignored by Git
├── README.md                       # Main project overview & instructions

