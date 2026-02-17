import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions (GLOBAL)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    """
    Flask Application Factory
    """

    app = Flask(__name__)

    # Load config
    app.config.from_object("config.Config")

    # Create upload folder if not exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import models
    from backend.models.user import User
    from backend.models.detection import Detection

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.dashboard import dashboard_bp
    from backend.routes.prediction import prediction_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediction_bp)

    # Root route
    @app.route("/")
    def home():
        return "Leaf Disease Detection Backend Running"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
