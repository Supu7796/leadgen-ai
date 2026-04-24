import logging

from flask import Flask

from app.utils.response import error_response

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def handle_404(_):
        return error_response("Resource not found", 404)

    @app.errorhandler(405)
    def handle_405(_):
        return error_response("Method not allowed", 405)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):  # noqa: ANN001
        logger.exception("Unhandled exception: %s", str(error))
        return error_response("Internal server error", 500)
