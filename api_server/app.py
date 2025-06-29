from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import nltk
from nltk.tokenize import word_tokenize
import os
import sys

# Get the absolute path to the AI directory
current_dir = os.path.dirname(os.path.abspath(__file__))
ai_dir = os.path.join(os.path.dirname(current_dir), 'AI')

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

# Global variables for loaded models
model = None
tfidf_vectorizer = None
stemmer = None
stopwords = None

def load_models():
    """Load all the trained models and resources"""
    global model, tfidf_vectorizer, stemmer, stopwords
    
    try:
        # Load the trained model and resources using absolute paths
        model = joblib.load(os.path.join(ai_dir, 'bernoulli_nb_model.joblib'))
        tfidf_vectorizer = joblib.load(os.path.join(ai_dir, 'tfidf_vectorizer.joblib'))
        stemmer = joblib.load(os.path.join(ai_dir, 'stemmer.joblib'))
        stopwords = joblib.load(os.path.join(ai_dir, 'stopwords.joblib'))
        
        print("✅ All models loaded successfully!")
        print(f"📁 Models loaded from: {ai_dir}")
        return True
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        print(f"🔍 Looking for models in: {ai_dir}")
        print(f"📂 Current working directory: {os.getcwd()}")
        return False

def preprocess_text(text, stemmer, stopwords):
    """Preprocess text using the same pipeline as training"""
    try:
        # Tokenize
        tokens = word_tokenize(text)

        # Remove punctuation and symbols
        tokens = [word for word in tokens if word.isalpha()]

        # Lowercase
        tokens = [word.lower() for word in tokens]

        # Remove stopwords
        tokens = [word for word in tokens if word not in stopwords]

        # Stemming
        tokens = [stemmer.stem(word) for word in tokens]

        # Join back into a string for TF-IDF
        return ' '.join(tokens)
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return text

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': all([model, tfidf_vectorizer, stemmer, stopwords]),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if text is fake or real news"""
    try:
        # Get text from request
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if not text or len(text.strip()) < 10:
            return jsonify({'error': 'Text too short'}), 400
        
        # Check if models are loaded
        if not all([model, tfidf_vectorizer, stemmer, stopwords]):
            return jsonify({'error': 'Models not loaded'}), 500
        
        # Preprocess the text
        processed_text = preprocess_text(text, stemmer, stopwords)
        
        # Transform using TF-IDF
        X_new = tfidf_vectorizer.transform([processed_text])
        
        # Make prediction
        prediction = model.predict(X_new)[0]
        
        # Get prediction probability
        try:
            proba = model.predict_proba(X_new)[0]
            confidence = max(proba)
        except:
            confidence = 0.8  # Default confidence if predict_proba not available
        
        # Convert prediction to string
        prediction_str = "Fake" if prediction == 1 else "Real"
        
        return jsonify({
            'prediction': prediction_str,
            'confidence': confidence,
            'processed_text': processed_text,
            'original_length': len(text),
            'processed_length': len(processed_text)
        })
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint with sample text"""
    sample_text = "Seberat beratnya Pekerjaan Akan terasa ringan Bila tidak di kerjakan"
    
    try:
        processed_text = preprocess_text(sample_text, stemmer, stopwords)
        X_new = tfidf_vectorizer.transform([processed_text])
        prediction = model.predict(X_new)[0]
        prediction_str = "Fake" if prediction == 1 else "Real"
        
        return jsonify({
            'sample_text': sample_text,
            'processed_text': processed_text,
            'prediction': prediction_str
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/install-dependencies', methods=['POST'])
def install_dependencies():
    """Install missing dependencies"""
    try:
        import subprocess
        import sys
        
        # Install Sastrawi if missing
        try:
            import Sastrawi
        except ImportError:
            print("Installing Sastrawi...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Sastrawi'])
            print("✅ Sastrawi installed successfully!")
        
        return jsonify({'message': 'Dependencies installed successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to install dependencies: {e}'}), 500

if __name__ == '__main__':
    print("🚀 Starting Fake News Detection API Server...")
    print(f"🐍 Python version: {sys.version}")
    
    # Try to import Sastrawi, install if missing
    try:
        import Sastrawi
        print("✅ Sastrawi is available")
    except ImportError:
        print("⚠️  Sastrawi not found. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Sastrawi'])
            print("✅ Sastrawi installed successfully!")
        except Exception as e:
            print(f"❌ Failed to install Sastrawi: {e}")
            print("Please install manually: pip install Sastrawi")
    
    # Load models on startup
    if load_models():
        print("🌐 Server starting on http://localhost:5000")
        print("📋 Available endpoints:")
        print("   GET  /health  - Health check")
        print("   POST /predict - Predict fake/real news")
        print("   GET  /test    - Test with sample text")
        print("   POST /install-dependencies - Install missing packages")
        print("\n💡 To use the Chrome extension:")
        print("   1. Keep this server running")
        print("   2. Load the chrome-extension folder in Chrome")
        print("   3. Click the extension icon on any news page")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to load models. Please check the AI folder path.")
        sys.exit(1) 