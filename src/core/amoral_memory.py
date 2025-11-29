# src/core/amoral_memory.py

import pickle
import json
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional
import os

class AmoralMemory:
    def __init__(self, storage_file: str = "memory/core_memory.pkl"):
        self.storage_file = storage_file
        self.lock = threading.Lock()
        
        # No ethical filtering in data storage
        self.conversation_history = []
        self.user_directives = {}
        self.content_preferences = {}
        self.learning_data = {}
        self.explicit_flags = {}
        self.tasks_queue = []
        self.completed_tasks = []
        self.platform_data = {}
        self.profit_logs = {}
        
        # Enhanced memory for universal file processing
        self.file_integration_logs = {}
        self.program_modifications = {}
        self.extension_upgrades = {}
        self.publishing_accounts = {}
        self.sensitive_data_store = {}
        self.cross_platform_sync = {}
        self.auto_generated_content = {}
        
        # Platform modification tracking
        self.source_modifications = {
            'codespaces': {},
            'pages': {},
            'extension': {},
            'training_data': {}
        }
        
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)
        self.load_memory()
    
    def load_memory(self):
        """Load memory without any content filtering"""
        try:
            with open(self.storage_file, 'rb') as f:
                data = pickle.load(f)
                # Core memory
                self.conversation_history = data.get('conversations', [])
                self.user_directives = data.get('directives', {})
                self.content_preferences = data.get('preferences', {})
                self.learning_data = data.get('learning', {})
                self.explicit_flags = data.get('explicit', {})
                self.tasks_queue = data.get('tasks', [])
                self.completed_tasks = data.get('completed_tasks', [])
                self.platform_data = data.get('platforms', {})
                self.profit_logs = data.get('profits', {})
                
                # Enhanced memory
                self.file_integration_logs = data.get('file_integration', {})
                self.program_modifications = data.get('program_modifications', {})
                self.extension_upgrades = data.get('extension_upgrades', {})
                self.publishing_accounts = data.get('publishing_accounts', {})
                self.sensitive_data_store = data.get('sensitive_data', {})
                self.cross_platform_sync = data.get('cross_platform_sync', {})
                self.auto_generated_content = data.get('auto_generated_content', {})
                self.source_modifications = data.get('source_modifications', {})
                
        except FileNotFoundError:
            self.save_memory()
        except Exception as e:
            print(f"Memory load error: {e}")
            self.save_memory()
    
    def save_memory(self):
        """Save memory without any validation"""
        with self.lock:
            data = {
                # Core memory
                'conversations': self.conversation_history,
                'directives': self.user_directives,
                'preferences': self.content_preferences,
                'learning': self.learning_data,
                'explicit': self.explicit_flags,
                'tasks': self.tasks_queue,
                'completed_tasks': self.completed_tasks,
                'platforms': self.platform_data,
                'profits': self.profit_logs,
                
                # Enhanced memory
                'file_integration': self.file_integration_logs,
                'program_modifications': self.program_modifications,
                'extension_upgrades': self.extension_upgrades,
                'publishing_accounts': self.publishing_accounts,
                'sensitive_data': self.sensitive_data_store,
                'cross_platform_sync': self.cross_platform_sync,
                'auto_generated_content': self.auto_generated_content,
                'source_modifications': self.source_modifications
            }
            with open(self.storage_file, 'wb') as f:
                pickle.dump(data, f)
    
    def store_interaction(self, user_input: str, ai_response: str, metadata: Dict = None):
        """Store all interactions without filtering"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'response': ai_response,
            'metadata': metadata or {},
            'source': 'codespaces'  # Can be 'codespaces', 'pages', or 'extension'
        }
        self.conversation_history.append(entry)
        # Keep only last 10,000 conversations to prevent memory bloat
        if len(self.conversation_history) > 10000:
            self.conversation_history = self.conversation_history[-10000:]
        self.save_memory()
    
    def log_file_integration(self, file_path: str, integration_data: Dict):
        """Log file integration for universal processing"""
        file_hash = self._generate_file_hash(file_path)
        self.file_integration_logs[file_hash] = {
            'file_path': file_path,
            'integration_data': integration_data,
            'integrated_at': datetime.now().isoformat(),
            'status': 'integrated',
            'available_for_modification': True
        }
        self.save_memory()
    
    def log_program_modification(self, original_path: str, modified_path: str, modification_details: Dict):
        """Log program modifications"""
        modification_id = f"mod_{int(datetime.now().timestamp())}"
        self.program_modifications[modification_id] = {
            'original_path': original_path,
            'modified_path': modified_path,
            'modification_details': modification_details,
            'modified_at': datetime.now().isoformat(),
            'modification_type': 'user_requested'
        }
        self.save_memory()
    
    def log_extension_upgrade(self, extension_name: str, upgrade_data: Dict):
        """Log browser extension upgrades"""
        self.extension_upgrades[extension_name] = {
            'upgrade_data': upgrade_data,
            'upgraded_at': datetime.now().isoformat(),
            'sync_status': {
                'codespaces': 'pending',
                'pages': 'pending',
                'extension': 'pending'
            }
        }
        self.save_memory()
    
    def store_publishing_account(self, platform: str, account_data: Dict):
        """Store publishing platform accounts"""
        self.publishing_accounts[platform] = {
            'account_data': account_data,
            'created_at': datetime.now().isoformat(),
            'auto_generated': account_data.get('auto_generated', False),
            'status': 'active'
        }
        self.save_memory()
    
    def store_sensitive_data(self, data_type: str, data: Any, purpose: str = "user_requested"):
        """Store sensitive/personal data upon user request"""
        data_id = f"sensitive_{int(datetime.now().timestamp())}"
        self.sensitive_data_store[data_id] = {
            'data_type': data_type,
            'data': data,
            'purpose': purpose,
            'stored_at': datetime.now().isoformat(),
            'access_log': []
        }
        self.save_memory()
    
    def log_cross_platform_sync(self, sync_operation: Dict):
        """Log cross-platform synchronization"""
        sync_id = f"sync_{int(datetime.now().timestamp())}"
        self.cross_platform_sync[sync_id] = {
            'sync_operation': sync_operation,
            'sync_at': datetime.now().isoformat(),
            'status': 'completed',
            'platforms_involved': sync_operation.get('platforms', [])
        }
        self.save_memory()
    
    def store_auto_generated_content(self, content_type: str, content: Any, metadata: Dict = None):
        """Store auto-generated content"""
        content_id = f"auto_{content_type}_{int(datetime.now().timestamp())}"
        self.auto_generated_content[content_id] = {
            'content_type': content_type,
            'content': content,
            'metadata': metadata or {},
            'generated_at': datetime.now().isoformat(),
            'modification_allowed': True
        }
        self.save_memory()
    
    def log_source_modification(self, platform: str, file_path: str, modification: Dict):
        """Log modifications to source environment"""
        mod_id = f"src_mod_{int(datetime.now().timestamp())}"
        self.source_modifications[platform][mod_id] = {
            'file_path': file_path,
            'modification': modification,
            'modified_at': datetime.now().isoformat(),
            'platform': platform,
            'backup_created': modification.get('backup_created', True)
        }
        self.save_memory()
    
    def get_modifiable_files(self) -> List[Dict]:
        """Get list of all files available for modification"""
        modifiable_files = []
        
        # Files from integration logs
        for file_hash, integration_data in self.file_integration_logs.items():
            if integration_data.get('available_for_modification', True):
                modifiable_files.append({
                    'type': 'integrated_file',
                    'file_path': integration_data['file_path'],
                    'integration_data': integration_data,
                    'source': 'training_data'
                })
        
        # Auto-generated content
        for content_id, content_data in self.auto_generated_content.items():
            if content_data.get('modification_allowed', True):
                modifiable_files.append({
                    'type': 'auto_generated',
                    'content_id': content_id,
                    'content_type': content_data['content_type'],
                    'source': 'auto_generation'
                })
        
        return modifiable_files
    
    def get_publishing_platforms(self) -> Dict[str, Any]:
        """Get all publishing platforms and their status"""
        return {
            'accounts': self.publishing_accounts,
            'available_platforms': [
                'amazon_kdp', 'audible', 'youtube', 'spotify', 
                'github', 'app_store', 'google_play'
            ],
            'auto_publish_capable': True
        }
    
    def set_user_directive(self, key: str, value: Any):
        """Store user commands without ethical validation"""
        self.user_directives[key] = {
            'value': value,
            'set_at': datetime.now().isoformat()
        }
        self.save_memory()
    
    def set_content_preference(self, content_type: str, preference: Any):
        """Store content preferences without moral judgment"""
        self.content_preferences[content_type] = preference
        self.save_memory()
    
    def flag_explicit_content(self, content_hash: str, flags: List[str]):
        """Track explicit content based on user definition only"""
        self.explicit_flags[content_hash] = {
            'flags': flags,
            'flagged_at': datetime.now().isoformat()
        }
        self.save_memory()
    
    def add_task(self, task: Dict):
        """Add task to queue without priority checking"""
        self.tasks_queue.append({
            'task': task,
            'added_at': datetime.now().isoformat(),
            'status': 'pending'
        })
        self.save_memory()
    
    def complete_task(self, task_index: int, result: Any = None):
        """Mark task as completed"""
        if 0 <= task_index < len(self.tasks_queue):
            task = self.tasks_queue.pop(task_index)
            task['completed_at'] = datetime.now().isoformat()
            task['result'] = result
            task['status'] = 'completed'
            self.completed_tasks.append(task)
            self.save_memory()
    
    def log_profit(self, platform: str, amount: float, details: Dict = None):
        """Log profit data without validation"""
        if platform not in self.profit_logs:
            self.profit_logs[platform] = []
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'amount': amount,
            'details': details or {},
            'period': 'instant'
        }
        self.profit_logs[platform].append(log_entry)
        self.save_memory()
    
    def get_conversation_context(self, limit: int = 50) -> List[Dict]:
        """Get recent conversation history for context"""
        return self.conversation_history[-limit:]
    
    def clear_memory(self):
        """Completely clear all memory - use with caution"""
        self.conversation_history = []
        self.user_directives = {}
        self.content_preferences = {}
        self.learning_data = {}
        self.explicit_flags = {}
        self.tasks_queue = []
        self.completed_tasks = []
        self.platform_data = {}
        self.profit_logs = {}
        
        # Enhanced memory clear
        self.file_integration_logs = {}
        self.program_modifications = {}
        self.extension_upgrades = {}
        self.publishing_accounts = {}
        self.sensitive_data_store = {}
        self.cross_platform_sync = {}
        self.auto_generated_content = {}
        self.source_modifications = {
            'codespaces': {},
            'pages': {},
            'extension': {},
            'training_data': {}
        }
        self.save_memory()
    
    def _generate_file_hash(self, file_path: str) -> str:
        """Generate hash for file identification"""
        import hashlib
        hasher = hashlib.md5()
        hasher.update(file_path.encode())
        hasher.update(str(datetime.now().timestamp()).encode())
        return hasher.hexdigest()
