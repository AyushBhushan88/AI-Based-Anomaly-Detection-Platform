from flask import Flask
from flask_cors import CORS
from src.api.routes import api_bp

def create_app():
    app = Flask(__name__)
    
    # Enable Cross-Origin Resource Sharing (CORS) for dashboard frontend
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app

if __name__ == "__main__":
    app = create_app()
    print("Starting Healthcare Anomaly Detection API...")
    app.run(host="0.0.0.0", port=5000, debug=True)
