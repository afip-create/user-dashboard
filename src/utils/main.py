import os
import logging
from flask import Flask, render_template, request
from user_dashboard.models import db, User, Post
from user_dashboard.routes import login_manager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
with app.app_context():
    db.create_all()

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Blueprints
from user_dashboard.blueprints import auth, dashboard
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(dashboard.dashboard_blueprint)

# Login manager
login_manager.init_app(app)

# Run application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)