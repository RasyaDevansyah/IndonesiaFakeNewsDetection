# Indonesia Fake News Detection Chrome Extension

A complete solution for detecting fake news in Indonesian articles using AI and a Chrome extension.

## 🚀 Features

- **AI-Powered Detection**: Uses a trained Bernoulli Naive Bayes model
- **Chrome Extension**: Analyze any news article directly from your browser
- **Real-time Analysis**: Get instant predictions with confidence scores
- **Beautiful UI**: Modern, responsive interface
- **Smart Text Extraction**: Automatically extracts article content from web pages
- **Local Processing**: All AI processing happens on your local machine

## 📁 Project Structure

```
IndonesiaFakeNewsDetection/
├── AI/                                    # Your trained models
│   ├── bernoulli_nb_model.joblib         # Trained model
│   ├── tfidf_vectorizer.joblib           # TF-IDF vectorizer
│   ├── stemmer.joblib                    # Indonesian stemmer
│   ├── stopwords.joblib                  # Indonesian stopwords
│   ├── processed_data.csv                # Training data
│   └── FakeNewsDetection_*.ipynb         # Training notebooks
├── chrome-extension/                      # Chrome extension files
│   ├── manifest.json                     # Extension configuration
│   ├── popup.html                        # Extension UI
│   ├── popup.js                          # Extension logic
│   ├── content.js                        # Content script
│   ├── icon.svg                          # Extension icon
│   └── README.md                         # Extension documentation
├── api_server/                           # Flask API server
│   ├── app.py                            # Main server file
│   └── requirements.txt                  # Python dependencies
├── start_server.py                       # Easy startup script
├── generate_icons.py                     # Icon generation script
└── README.md                             # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Your trained model files in the `AI/` directory

### Step 1: Start the API Server

Run the startup script which will check dependencies and start the server:

```bash
python start_server.py
```

Or manually:

```bash
cd api_server
pip install -r requirements.txt
python app.py
```

The server will start on `http://localhost:5000`

### Step 2: Generate Extension Icons

```bash
python generate_icons.py
```

This will create the required PNG icon files for the Chrome extension.

### Step 3: Load the Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. The extension should now appear in your toolbar

## 🎯 How to Use

1. **Navigate to any Indonesian news article**
2. **Click the extension icon** in your Chrome toolbar
3. **Click "Analyze Current Page"**
4. **View the result**:
   - 🚨 **Fake News** (red background)
   - ✅ **Real News** (green background)
   - Confidence percentage

## 🔧 How It Works

### 1. Text Extraction
The extension uses smart selectors to find article content:
- `<article>` tags
- Content classes (`.article`, `.post`, `.content`)
- Main content areas
- Fallback to body text

### 2. API Communication
- Extracted text is sent to your local Flask API
- JSON format: `{"text": "article content"}`

### 3. AI Processing
Your trained model:
- Preprocesses text (tokenization, stemming, stopword removal)
- Applies TF-IDF vectorization
- Makes prediction using Bernoulli Naive Bayes
- Returns prediction + confidence score

### 4. Result Display
- Shows prediction (Fake/Real)
- Displays confidence percentage
- Color-coded results

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check server and model status |
| `/predict` | POST | Predict fake/real news |
| `/test` | GET | Test with sample text |

### Example API Usage

```bash
# Health check
curl http://localhost:5000/health

# Predict
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Your Indonesian news text here"}'

# Test
curl http://localhost:5000/test
```

## 🎨 Customization

### Extension UI
- Modify `chrome-extension/popup.html` for UI changes
- Edit `chrome-extension/popup.js` for functionality
- Update `chrome-extension/content.js` for text extraction logic

### API Server
- Add new endpoints in `api_server/app.py`
- Modify preprocessing in the `preprocess_text()` function
- Add new model types or features

### Model Integration
- Replace model files in `AI/` directory
- Update `app.py` to load different models
- Modify preprocessing pipeline as needed

## 🔍 Troubleshooting

### Extension Issues
- **Extension not working**: Check if API server is running on `localhost:5000`
- **No text found**: Try refreshing the page or check if it's a news article
- **Permission errors**: Ensure extension has correct permissions in `manifest.json`

### API Server Issues
- **Model loading errors**: Check file paths in `app.py`
- **Dependency errors**: Run `pip install -r requirements.txt`
- **Port conflicts**: Change port in `app.py` if 5000 is busy

### Performance Issues
- **Slow predictions**: Consider model optimization or caching
- **Memory usage**: Monitor server memory usage with large models
- **Text length**: Extension limits text to 5000 characters

## 🔒 Security Notes

- **Local Processing**: All AI processing happens on your machine
- **No External Calls**: Extension only communicates with local API
- **Data Privacy**: No article content is sent to external servers
- **Model Security**: Keep your trained models secure

## 📊 Model Information

Your trained model uses:
- **Algorithm**: Bernoulli Naive Bayes
- **Features**: TF-IDF vectorization
- **Language**: Indonesian
- **Preprocessing**: Tokenization, stemming, stopword removal
- **Training Data**: `processed_data.csv`

## 🤝 Contributing

To improve the project:

1. **Enhance Text Extraction**: Improve content detection for different news sites
2. **Add Model Types**: Support for other ML algorithms
3. **UI Improvements**: Better user experience and design
4. **Performance**: Optimize model loading and prediction speed
5. **Testing**: Add comprehensive test coverage

## 📝 License

This project is for educational and research purposes. Please ensure you have proper permissions for any data or models used.

## 🙏 Acknowledgments

- Your trained model and preprocessing pipeline
- Flask framework for the API server
- Chrome Extension APIs
- Indonesian NLP libraries (Sastrawi, NLTK)

---

**Happy Fake News Detection! 🔍📰** 