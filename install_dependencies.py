#!/usr/bin/env python3
"""
Quick script to install missing dependencies for the Fake News Detector
"""

import subprocess
import sys

def install_sastrawi():
    """Install Sastrawi package"""
    print("🔧 Installing Sastrawi...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Sastrawi'])
        print("✅ Sastrawi installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Sastrawi: {e}")
        return False

def install_all_dependencies():
    """Install all required dependencies"""
    packages = [
        'flask==3.0.0',
        'flask-cors==4.0.0', 
        'joblib==1.3.2',
        'nltk==3.8.1',
        'scikit-learn==1.3.2',
        'numpy==1.25.2',
        'pandas==2.1.4',
        'Sastrawi==1.0.1'
    ]
    
    print("🔧 Installing all dependencies...")
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Fake News Detector - Dependency Installer")
    print("=" * 50)
    
    choice = input("Install all dependencies (a) or just Sastrawi (s)? [a/s]: ").lower()
    
    if choice == 'a':
        success = install_all_dependencies()
    else:
        success = install_sastrawi()
    
    if success:
        print("\n✅ Installation completed! You can now run:")
        print("python start_server.py")
    else:
        print("\n❌ Installation failed. Please try manually:")
        print("pip install Sastrawi") 