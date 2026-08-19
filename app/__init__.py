import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=str(Path(app.instance_path) / "quiz.db"),
        ADMIN_USERNAME=os.environ.get("ADMIN_USERNAME", "admin"),
        ADMIN_PASSWORD=os.environ.get("ADMIN_PASSWORD", "quiz2026"),
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    if test_config is None:
        print(
            f"\nAdmin login -> username: {app.config['ADMIN_USERNAME']}  "
            f"password: {app.config['ADMIN_PASSWORD']}\n"
            "(Change these by setting ADMIN_USERNAME / ADMIN_PASSWORD environment variables.)\n"
        )

    from app import db
    db.init_app(app)

    # Auto-create + seed the database on first run so the app works out of the box.
    db_path = Path(app.config["DATABASE"])
    if not db_path.exists():
        with app.app_context():
            db.init_db()
            from app.seed_data import seed_database
            seed_database(db.get_db())

    from app.routes_main import bp as main_bp
    from app.routes_api import bp as api_bp
    from app.routes_admin import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    return app
