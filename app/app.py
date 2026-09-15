import os
import platform
import socket
import logging
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("production-kubernetes-platform")

APP_NAME = os.getenv("APP_NAME", "production-kubernetes-platform")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@app.route("/")
def home():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "message": "Production Kubernetes Platform API",
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200


@app.route("/ready")
def ready():
    return jsonify({
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200


@app.route("/api/v1/status")
def status():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "status": "running",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200


@app.route("/api/v1/info")
def info():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist.",
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.exception("Internal server error")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred.",
    }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(
        "Starting %s version %s on %s:%s",
        APP_NAME,
        APP_VERSION,
        host,
        port,
    )

    app.run(host=host, port=port)
