# src/processing/file_ingestor.py

import os
import hashlib
from typing import Dict, List, Any
from datetime import datetime

class FileIngestor:
    def __init__(self, data_folder: str = "training_data"):
        self.data_folder = data_folder
        self.supported_extensions = {
            '.txt', '.pdf', '.doc', '.docx', '.json', '.xml', 
            '.csv', '.html', '.htm', '.md', '.py', '.js', '.java',
            '.cpp', '.c', '.h', '.jpg', '.jpeg', '.png', '.gif'
        }
    
    def scan_directory(self, directory: str = None) -> List[Dict[str, Any]]:
        """Scan directory for processable files"""
        if directory is None:
            directory = self.data_folder
        
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            return []
        
        files_data = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in self.supported_extensions:
                    file_data = self._analyze_file(file_path)
                    files_data.append(file_data)
        
        return files_data
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze individual file"""
        try:
            file_stats = os.stat(file_path)
            file_hash = self._hash_file(file_path)
            
            return {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'file_size': file_stats.st_size,
                'modified_time': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                'file_hash': file_hash,
                'file_type': os.path.splitext(file_path)[1].lower(),
                'status': 'processed'
            }
        except Exception as e:
            return {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'error': str(e),
                'status': 'error'
            }
    
    def _hash_file(self, file_path: str) -> str:
        """Generate file hash"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """Ingest single file"""
        return self._analyze_file(file_path)
    
    def get_supported_extensions(self) -> set:
        """Get supported file extensions"""
        return self.supported_extensions