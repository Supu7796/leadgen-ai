import logging
import os

from dotenv import load_dotenv
from flask import Flask

from app.api.lead_routes import lead_bp
from app.models.db import db
from app.utils.error_handlers import register_error_handlers


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_AS_ASCII"] = False

    _configure_logging()

    db.init_app(app)
    app.register_blueprint(lead_bp, url_prefix="/api")
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    @app.get("/health")
    def health_check():
        return {"status": "ok"}, 200

    return app


def _configure_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
