# Indonesia Fake News Detector Chrome Extension

A Chrome extension that analyzes Indonesian news articles to detect fake news using AI.

## Features

- 🔍 Analyze any news article on the web
- 🤖 Uses your trained Bernoulli Naive Bayes model
- 🎯 Real-time prediction with confidence scores
- 🎨 Beautiful, modern UI
- 📱 Works on any news website

## Installation

### 1. Start the API Server

First, you need to run the Flask API server that contains your trained model:

```bash
cd api_server
pip install -r requirements.txt
python app.py
```

The server will start on `http://localhost:5000`

### 2. Load the Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder from this project
5. The extension should now appear in your extensions list

### 3. Use the Extension

1. Navigate to any Indonesian news article
2. Click the extension icon in your Chrome toolbar
3. Click "Analyze Current Page"
4. View the prediction result (Real/Fake with confidence)

## How it Works

1. **Text Extraction**: The extension extracts article text from the webpage using smart selectors
2. **API Communication**: Sends the extracted text to your Flask API server
3. **AI Processing**: Your trained model preprocesses and analyzes the text
4. **Result Display**: Shows the prediction with confidence score

## API Endpoints

- `GET /health` - Check if server and models are loaded
- `POST /predict` - Predict fake/real news (send JSON with "text" field)
- `GET /test` - Test with sample text

## Troubleshooting

### Extension not working?
- Make sure the API server is running on `localhost:5000`
- Check the browser console for errors
- Verify the extension has the correct permissions

### API server errors?
- Ensure all model files are in the `AI/` folder
- Check that all dependencies are installed
- Verify the file paths in `app.py`

### Text extraction issues?
- The extension tries multiple selectors to find article content
- If no content is found, it will show an error message
- Try refreshing the page and analyzing again

## File Structure

```
chrome-extension/
├── manifest.json      # Extension configuration
├── popup.html         # Extension popup UI
├── popup.js          # Popup functionality
├── content.js        # Content script for text extraction
└── README.md         # This file

api_server/
├── app.py            # Flask API server
├── requirements.txt  # Python dependencies
└── README.md         # API documentation
```

## Customization

You can customize the extension by:
- Modifying the UI in `popup.html` and `popup.js`
- Adjusting text extraction logic in `content.js`
- Adding new features to the API in `app.py`

## Security Notes

- The extension only sends article text to your local API server
- No data is sent to external servers
- All processing happens locally on your machine 