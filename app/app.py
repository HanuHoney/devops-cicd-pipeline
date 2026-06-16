from flask import Flask, jsonify
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps CI/CD Pipeline — Live",
        "version": APP_VERSION,
        "environment": ENVIRONMENT
    })


@app.route("/health")
def health():
    """Kubernetes liveness probe endpoint."""
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    }), 200


@app.route("/ready")
def ready():
    """Kubernetes readiness probe endpoint."""
    return jsonify({
        "status": "ready",
        "environment": ENVIRONMENT
    }), 200


@app.route("/api/info")
def info():
    return jsonify({
        "app": "devops-cicd-pipeline",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "maintainer": "Hanu Priya"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
