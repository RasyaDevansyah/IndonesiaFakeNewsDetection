#!/usr/bin/env python3
"""
Startup script for the Indonesia Fake News Detector API Server
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask_cors', 
        'joblib',
        'nltk',
        'sklearn',
        'numpy',
        'pandas',
        'Sastrawi'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ All required packages are installed")
    
    return True

def check_model_files():
    """Check if model files exist"""
    model_files = [
        'AI/bernoulli_nb_model.joblib',
        'AI/tfidf_vectorizer.joblib',
        'AI/stemmer.joblib',
        'AI/stopwords.joblib'
    ]
    
    missing_files = []
    for file_path in model_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing model files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease make sure all model files are in the AI/ directory")
        return False
    
    print("✅ All model files found")
    return True

def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        nltk.download('punkt_tab', quiet=True)
        print("✅ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not download NLTK data: {e}")
        return True  # Continue anyway

def install_sastrawi():
    """Install Sastrawi if not available"""
    try:
        import Sastrawi
        print("✅ Sastrawi is available")
        return True
    except ImportError:
        print("⚠️  Sastrawi not found. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Sastrawi'])
            print("✅ Sastrawi installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Sastrawi. Please install manually:")
            print("pip install Sastrawi")
            return False

def start_server():
    """Start the Flask API server"""
    print("\n🚀 Starting Fake News Detection API Server...")
    print("=" * 50)
    
    # Change to api_server directory
    os.chdir('api_server')
    
    # Start the server
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🔍 Indonesia Fake News Detector - Server Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Install Sastrawi specifically
    if not install_sastrawi():
        return
    
    # Download NLTK data
    download_nltk_data()
    
    # Check model files
    if not check_model_files():
        return
    
    print("\n✅ All checks passed! Starting server...")
    start_server()

if __name__ == "__main__":
    main() 