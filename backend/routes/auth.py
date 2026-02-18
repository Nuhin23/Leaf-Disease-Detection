from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

# IMPORTANT: import from app factory context
from backend.models.user import User
from app import db

# Create Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration
    """
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for("auth.register"))

        # Create user object
        user = User(username=name, email=email)
        user.set_password(password)

        # Save to database
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # Verify credentials
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid email or password", "danger")



    return render_template("login.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
@login_required
def logout():
    """
    Logs out the current user
    """
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))