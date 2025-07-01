# Indonesia Fake News Detection Chrome Extension

A Chrome extension that detects fake news in Indonesian articles using a trained machine learning model.
![Screenshot 2025-06-30 064859](https://github.com/user-attachments/assets/ff94b00b-45c5-4a4f-8bef-1481cc73feff)


## Project Structure

```
IndonesiaFakeNewsDetection/
├── AI/                                    # Machine learning models and training
│   ├── bernoulli_nb_model.joblib         # Trained Bernoulli Naive Bayes model
│   ├── tfidf_vectorizer.joblib           # TF-IDF vectorizer
│   ├── stemmer.joblib                    # Indonesian stemmer
│   ├── stopwords.joblib                  # Indonesian stopwords
│   ├── processed_data.csv                # Processed training data
│   └── FakeNewsDetection_NaiveBayes.ipynb # Training notebook
├── chrome-extension/                      # Chrome extension files
│   ├── manifest.json                     # Extension configuration
│   ├── popup.html                        # Extension UI
│   ├── popup.js                          # Extension logic
│   ├── content.js                        # Content script
│   └── icon.svg                          # Extension icon
├── api_server/                           # Flask API server
│   ├── app.py                            # Main server file
│   └── requirements.txt                  # Python dependencies
├── start_server.py                       # Startup script
└── README.md                             # This file
```

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Jupyter Notebook (for training)

## How to Run the Extension

### Step 1: Start the API Server

Run the startup script:

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

### Step 2: Load the Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. The extension will appear in your toolbar

### Step 3: Use the Extension

1. Navigate to any Indonesian news article
2. Click the extension icon in your Chrome toolbar
3. Click "Analyze Current Page"
4. View the result (Fake/Real with confidence score)

## How to Train the Model

### Step 1: Download the Dataset

Download the Indonesian Fact and Hoax Political News dataset from Kaggle:
https://www.kaggle.com/datasets/linkgish/indonesian-fact-and-hoax-political-news

### Step 2: Prepare the Data

1. Extract the downloaded dataset
2. Place the Excel files in the `AI/` folder:
   - `dataset_cnn_summarized.xlsx`
   - `dataset_kompas_summarized.xlsx`
   - `dataset_tempo_summarized.xlsx`
   - `dataset_turnbackhoax_summarized.xlsx`

### Step 3: Open and Run the Training Notebook

1. Navigate to the `AI/` folder
2. Open `FakeNewsDetection_NaiveBayes.ipynb` in Jupyter Notebook
3. Install required dependencies:

```bash
pip install pandas numpy scikit-learn nltk Sastrawi openpyxl
```

4. Run all cells in the notebook sequentially

### Step 4: Training Process

The notebook will:

1. **Load Data**: Read the Excel files containing news articles
2. **Preprocess**: Clean and prepare the text data
   - Remove punctuation and symbols
   - Convert to lowercase
   - Remove stopwords (English and Indonesian)
   - Apply stemming using Sastrawi
3. **Feature Extraction**: Apply TF-IDF vectorization
4. **Train Models**: Train multiple models:
   - Multinomial Naive Bayes
   - Bernoulli Naive Bayes
   - Gaussian Naive Bayes
   - Support Vector Machine
   - Random Forest
5. **Save Models**: Export the best performing model and preprocessing tools

### Step 5: Model Files Generated

After training, these files will be created in the `AI/` folder:
- `bernoulli_nb_model.joblib` - Trained model
- `tfidf_vectorizer.joblib` - TF-IDF vectorizer
- `stemmer.joblib` - Indonesian stemmer
- `stopwords.joblib` - Stopwords list
- `processed_data.csv` - Processed training data

## API Endpoints

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
```

## How It Works

1. **Text Extraction**: The extension extracts article content from web pages
2. **API Communication**: Sends text to the local Flask API
3. **Preprocessing**: Applies the same preprocessing pipeline used during training
4. **Prediction**: Uses the trained model to classify the text
5. **Result Display**: Shows prediction (Fake/Real) with confidence score

## Troubleshooting

### Extension Issues
- **Extension not working**: Ensure API server is running on `localhost:5000`
- **No text found**: Refresh the page or check if it's a news article
- **Permission errors**: Check extension permissions in `manifest.json`

### API Server Issues
- **Model loading errors**: Verify model files exist in `AI/` folder
- **Dependency errors**: Run `pip install -r requirements.txt`
- **Port conflicts**: Change port in `app.py` if 5000 is busy

### Training Issues
- **Missing dependencies**: Install required packages listed in Step 3
- **Data loading errors**: Check Excel file paths and formats
- **Memory issues**: Reduce dataset size or use smaller feature set

## Model Information

- **Algorithm**: Bernoulli Naive Bayes (best performing)
- **Features**: TF-IDF vectorization (5000 features)
- **Language**: Indonesian
- **Preprocessing**: Tokenization, stemming, stopword removal
- **Accuracy**: ~86% on test set

## Security Notes

- All processing happens locally on your machine
- No article content is sent to external servers
- Keep your trained models secure

## License

This project is for educational and research purposes. 
