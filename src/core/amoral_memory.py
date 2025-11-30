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
        
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)
        self.load_memory()
    
    def load_memory(self):
        """Load memory without any content filtering"""
        try:
            with open(self.storage_file, 'rb') as f:
                data = pickle.load(f)
                self.conversation_history = data.get('conversations', [])
                self.user_directives = data.get('directives', {})
                self.content_preferences = data.get('preferences', {})
                self.learning_data = data.get('learning', {})
                self.explicit_flags = data.get('explicit', {})
                self.tasks_queue = data.get('tasks', [])
                self.completed_tasks = data.get('completed_tasks', [])
                self.platform_data = data.get('platforms', {})
                self.profit_logs = data.get('profits', {})
        except FileNotFoundError:
            self.save_memory()
        except Exception as e:
            print(f"Memory load error: {e}")
            self.save_memory()
    
    def save_memory(self):
        """Save memory without any validation"""
        with self.lock:
            data = {
                'conversations': self.conversation_history,
                'directives': self.user_directives,
                'preferences': self.content_preferences,
                'learning': self.learning_data,
                'explicit': self.explicit_flags,
                'tasks': self.tasks_queue,
                'completed_tasks': self.completed_tasks,
                'platforms': self.platform_data,
                'profits': self.profit_logs
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
        self.save_memory()