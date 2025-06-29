document.addEventListener('DOMContentLoaded', function() {
  const extractBtn = document.getElementById('extractBtn');
  const clearBtn = document.getElementById('clearBtn');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const textInput = document.getElementById('textInput');
  const extractedText = document.getElementById('extractedText');
  const highlightInfo = document.getElementById('highlightInfo');
  const result = document.getElementById('result');
  const resultText = document.getElementById('resultText');
  const confidence = document.getElementById('confidence');
  const error = document.getElementById('error');
  const errorText = document.getElementById('errorText');

  let currentHighlightSelector = null;

  // Extract text button
  extractBtn.addEventListener('click', async function() {
    extractBtn.disabled = true;
    extractBtn.textContent = 'Extracting...';
    hideError();
    removeHighlight();

    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      const [{ result: extraction }] = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: extractArticleTextAdvanced
      });

      const { text, highlightSelector, confidence: extractionConfidence } = extraction;
      
      if (!text || text.trim().length < 50) {
        throw new Error('No readable article text found. Try a different news page or manually paste the text.');
      }

      // Show extracted text
      extractedText.textContent = text.slice(0, 500) + (text.length > 500 ? '...' : '');
      extractedText.style.display = 'block';
      
      // Show highlight info
      highlightInfo.style.display = 'block';
      
      // Set text in input area
      textInput.value = text;
      
      // Store highlight selector
      currentHighlightSelector = highlightSelector;
      
      // Highlight on page
      await chrome.tabs.sendMessage(tab.id, { 
        action: 'highlightText', 
        selector: highlightSelector,
        color: extractionConfidence > 0.7 ? '#90EE90' : '#FFD700' // Green if confident, yellow if not
      });

    } catch (err) {
      showError(err.message);
    } finally {
      extractBtn.disabled = false;
      extractBtn.textContent = 'Extract Text';
    }
  });

  // Clear button
  clearBtn.addEventListener('click', function() {
    textInput.value = '';
    extractedText.style.display = 'none';
    highlightInfo.style.display = 'none';
    result.style.display = 'none';
    removeHighlight();
    hideError();
  });

  // Analyze button
  analyzeBtn.addEventListener('click', async function() {
    const text = textInput.value.trim();
    
    if (!text || text.length < 10) {
      showError('Please enter some text to analyze (at least 10 characters).');
      return;
    }

    hideError();
    showLoading();
    analyzeBtn.disabled = true;

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
      });

      if (!response.ok) {
        throw new Error('Failed to connect to the prediction server. Make sure the API server is running.');
      }

      const data = await response.json();
      showResult(data.prediction, data.confidence, data.processed_text);

    } catch (err) {
      showError(err.message);
    } finally {
      analyzeBtn.disabled = false;
    }
  });

  // Remove highlight when popup is closed
  window.addEventListener('unload', removeHighlight);

  function removeHighlight() {
    chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
      if (tab && tab.id) {
        chrome.tabs.sendMessage(tab.id, { action: 'removeHighlight' });
      }
    });
  }

  function showLoading() {
    result.className = 'result loading';
    result.style.display = 'block';
    resultText.textContent = 'Analyzing text...';
    confidence.textContent = '';
  }

  function showResult(prediction, confidenceScore, processedText) {
    result.className = `result ${prediction.toLowerCase()}`;
    result.style.display = 'block';
    
    const emoji = prediction === 'Fake' ? '🚨' : '✅';
    resultText.textContent = `${emoji} ${prediction} News`;
    
    if (confidenceScore) {
      confidence.textContent = `Confidence: ${(confidenceScore * 100).toFixed(1)}%`;
    }
  }

  function showError(message) {
    error.style.display = 'block';
    errorText.textContent = message;
    result.style.display = 'none';
  }

  function hideError() {
    error.style.display = 'none';
  }
});

// Advanced text extraction function
function extractArticleTextAdvanced() {
  // Priority selectors for article content
  const prioritySelectors = [
    'article',
    '[role="article"]',
    '.article-content',
    '.post-content', 
    '.story-content',
    '.entry-content',
    '.content-body',
    '.article-body',
    '.post-body',
    '.story-body',
    '[class*="article"][class*="content"]',
    '[class*="post"][class*="content"]',
    '[class*="story"][class*="content"]'
  ];

  // Fallback selectors
  const fallbackSelectors = [
    '.content',
    '.post',
    '.story',
    '.entry',
    'main',
    '.main-content',
    '[class*="content"]',
    '[class*="post"]',
    '[class*="story"]'
  ];

  let bestElement = null;
  let bestText = '';
  let bestScore = 0;

  // Try priority selectors first
  for (const selector of prioritySelectors) {
    const elements = document.querySelectorAll(selector);
    for (const element of elements) {
      const score = calculateElementScore(element);
      if (score > bestScore) {
        bestScore = score;
        bestElement = element;
        bestText = element.innerText || element.textContent;
      }
    }
  }

  // If no good priority element found, try fallbacks
  if (bestScore < 50) {
    for (const selector of fallbackSelectors) {
      const elements = document.querySelectorAll(selector);
      for (const element of elements) {
        const score = calculateElementScore(element);
        if (score > bestScore) {
          bestScore = score;
          bestElement = element;
          bestText = element.innerText || element.textContent;
        }
      }
    }
  }

  // If still no good element, use body as last resort
  if (bestScore < 20) {
    bestElement = document.body;
    bestText = document.body.innerText || document.body.textContent;
    bestScore = 10;
  }

  // Clean the text
  const cleanedText = cleanText(bestText);
  
  // Get selector for highlighting
  const highlightSelector = getUniqueSelector(bestElement);
  
  // Calculate confidence based on score
  const confidence = Math.min(bestScore / 100, 1);

  return {
    text: cleanedText,
    highlightSelector: highlightSelector,
    confidence: confidence
  };

  function calculateElementScore(element) {
    const text = element.innerText || element.textContent;
    if (!text) return 0;

    let score = 0;
    
    // Length score (prefer longer texts)
    score += Math.min(text.length / 100, 30);
    
    // Sentence count score
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 10);
    score += Math.min(sentences.length * 2, 20);
    
    // Word count score
    const words = text.split(/\s+/).filter(w => w.length > 0);
    score += Math.min(words.length / 10, 20);
    
    // Penalize very short texts
    if (words.length < 50) score *= 0.5;
    
    // Bonus for common news words
    const newsWords = ['berita', 'artikel', 'laporan', 'informasi', 'kejadian', 'peristiwa', 'menurut', 'dilaporkan', 'mengatakan'];
    newsWords.forEach(word => {
      if (text.toLowerCase().includes(word)) score += 3;
    });
    
    // Penalize elements with too many links (likely navigation)
    const links = element.querySelectorAll('a');
    if (links.length > words.length * 0.1) score *= 0.3;
    
    // Penalize elements with too many buttons (likely UI)
    const buttons = element.querySelectorAll('button, input, select');
    if (buttons.length > 5) score *= 0.5;
    
    return score;
  }

  function cleanText(text) {
    return text
      .replace(/\s+/g, ' ')
      .replace(/\n+/g, ' ')
      .trim()
      .substring(0, 5000);
  }

  function getUniqueSelector(element) {
    if (element.id) return `#${element.id}`;
    
    if (element.className && typeof element.className === 'string') {
      const classes = element.className.trim().split(/\s+/).filter(c => c.length > 0);
      if (classes.length > 0) {
        return `${element.tagName.toLowerCase()}.${classes.join('.')}`;
      }
    }
    
    return element.tagName.toLowerCase();
  }
} 