# ===========================
# Configuration File
# ===========================
# This file contains all configuration settings for the application
# Modify these values according to your requirements

import os

# ===========================
# Flask Configuration
# ===========================

class Config:
    """Base configuration"""
    # Secret key for session management
    # IMPORTANT: Change this in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2024'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application settings
    DEBUG = False
    TESTING = False
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Admin credentials
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'Admin@123'  # IMPORTANT: Change in production!


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Requires HTTPS
    
    # Use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    
    if not SECRET_KEY or not ADMIN_PASSWORD:
        raise ValueError("SECRET_KEY and ADMIN_PASSWORD must be set in production!")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# ===========================
# Configuration Selection
# ===========================

# Get config from environment variable or default to development
config_name = os.environ.get('FLASK_ENV') or 'development'

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}

# Get the appropriate configuration class
CURRENT_CONFIG = config_dict.get(config_name, DevelopmentConfig)

# ===========================
# Event Settings
# ===========================

EVENT_NAME = "Code, Bid & Build"
EVENT_DESCRIPTION = "A thrilling competition combining coding prowess with strategic bidding"
EVENT_YEAR = 2024

# ===========================
# Email Configuration (Optional)
# ===========================

# Uncomment and configure if you want to send confirmation emails

# MAIL_SERVER = os.environ.get('MAIL_SERVER')
# MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
# MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# ADMINS = ['admin@example.com']

# ===========================
# Logging Configuration (Optional)
# ===========================

# Uncomment if you want to enable logging

# LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
# LOG_FILE = 'app.log'
# LOG_LEVEL = 'INFO'

# ===========================
# AWS/Cloud Configuration (Optional)
# ===========================

# Uncomment if deploying to cloud platforms

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
