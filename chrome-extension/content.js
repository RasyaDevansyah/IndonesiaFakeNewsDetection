// Content script for better text extraction and highlighting
// This script can be injected into pages to help extract article content

(function() {
  'use strict';

  let lastHighlighted = null;
  let lastOriginalBg = null;
  let lastOriginalBorder = null;

  // Listen for messages from the popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'extractText') {
      const text = extractArticleText();
      sendResponse({ text: text });
    } else if (request.action === 'highlightText' && request.selector) {
      highlightElement(request.selector, request.color || '#FFD700');
    } else if (request.action === 'removeHighlight') {
      removeHighlight();
    }
  });

  function extractArticleText() {
    // Enhanced text extraction for news articles
    const selectors = [
      // Article-specific selectors
      'article',
      '[role="article"]',
      '.article',
      '.post',
      '.story',
      '.entry',
      
      // Content selectors
      '.content',
      '.post-content',
      '.article-content',
      '.story-content',
      '.entry-content',
      '.main-content',
      
      // Common news site selectors
      '[class*="article"]',
      '[class*="post"]',
      '[class*="story"]',
      '[class*="content"]',
      
      // Generic content areas
      'main',
      '.main',
      '#content',
      '#main'
    ];

    let bestText = '';
    let bestScore = 0;

    // Score each potential content area
    selectors.forEach(selector => {
      const elements = document.querySelectorAll(selector);
      elements.forEach(element => {
        const text = element.innerText || element.textContent;
        if (text) {
          const score = calculateTextScore(text);
          if (score > bestScore) {
            bestScore = score;
            bestText = text;
          }
        }
      });
    });

    // If no good content found, try body text
    if (bestScore < 10) {
      const bodyText = document.body.innerText || document.body.textContent;
      if (bodyText) {
        bestText = bodyText;
      }
    }

    return cleanText(bestText);
  }

  function calculateTextScore(text) {
    // Simple scoring algorithm for text quality
    const words = text.split(/\s+/).filter(word => word.length > 0);
    const sentences = text.split(/[.!?]+/).filter(sentence => sentence.trim().length > 0);
    
    // Prefer longer texts with good sentence structure
    let score = words.length * 0.1;
    score += sentences.length * 2;
    
    // Penalize very short texts
    if (words.length < 50) score *= 0.5;
    
    // Bonus for common news words
    const newsWords = ['berita', 'artikel', 'laporan', 'informasi', 'kejadian', 'peristiwa'];
    newsWords.forEach(word => {
      if (text.toLowerCase().includes(word)) score += 5;
    });
    
    return score;
  }

  function cleanText(text) {
    return text
      .replace(/\s+/g, ' ')           // Normalize whitespace
      .replace(/\n+/g, ' ')           // Replace newlines with spaces
      .replace(/\t+/g, ' ')           // Replace tabs with spaces
      .trim()
      .substring(0, 5000);            // Limit length
  }

  function highlightElement(selector, color = '#FFD700') {
    removeHighlight();
    const elem = document.querySelector(selector);
    if (elem) {
      lastHighlighted = elem;
      lastOriginalBg = elem.style.backgroundColor;
      lastOriginalBorder = elem.style.border;
      
      // Add highlight with border
      elem.style.backgroundColor = color;
      elem.style.border = `2px solid ${color === '#90EE90' ? '#228B22' : '#FF8C00'}`;
      elem.style.borderRadius = '4px';
      elem.style.padding = '8px';
      elem.style.margin = '4px';
      
      // Scroll to element
      elem.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
      // Add a subtle animation
      elem.style.transition = 'all 0.3s ease';
      setTimeout(() => {
        elem.style.transform = 'scale(1.02)';
        setTimeout(() => {
          elem.style.transform = 'scale(1)';
        }, 200);
      }, 100);
    }
  }

  function removeHighlight() {
    if (lastHighlighted) {
      lastHighlighted.style.backgroundColor = lastOriginalBg || '';
      lastHighlighted.style.border = lastOriginalBorder || '';
      lastHighlighted.style.borderRadius = '';
      lastHighlighted.style.padding = '';
      lastHighlighted.style.margin = '';
      lastHighlighted.style.transform = '';
      lastHighlighted.style.transition = '';
      lastHighlighted = null;
      lastOriginalBg = null;
      lastOriginalBorder = null;
    }
  }
})(); 