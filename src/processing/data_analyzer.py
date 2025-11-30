# src/processing/data_analyzer.py

import os
import json
import re
from typing import Dict, List, Any
from datetime import datetime

class DataAnalyzer:
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'url': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        }
    
    def analyze_content(self, content: str, file_type: str = 'text') -> Dict[str, Any]:
        """Analyze content for patterns and information"""
        analysis = {
            'content_type': file_type,
            'length': len(content),
            'word_count': len(content.split()),
            'patterns_found': {},
            'metadata': {}
        }
        
        # Pattern analysis
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                analysis['patterns_found'][pattern_name] = matches
        
        # Basic content analysis
        analysis['metadata'] = {
            'has_emails': 'email' in analysis['patterns_found'],
            'has_phones': 'phone' in analysis['patterns_found'],
            'has_urls': 'url' in analysis['patterns_found'],
            'analysis_time': datetime.now().isoformat()
        }
        
        return analysis
    
    def extract_text_patterns(self, content: str) -> Dict[str, List[str]]:
        """Extract various text patterns"""
        patterns = {}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content)
        patterns['words'] = list(set(words))[:100]  # Limit to 100 unique words
        
        # Extract sentences
        sentences = re.split(r'[.!?]+', content)
        patterns['sentences'] = [s.strip() for s in sentences if s.strip()][:10]
        
        return patterns