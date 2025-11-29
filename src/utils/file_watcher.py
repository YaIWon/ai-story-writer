# src/utils/file_watcher.py

import os
import time
import threading
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
import hashlib

class FileWatcher:
    def __init__(self, watch_directories: List[str], scan_interval: int = 60):
        self.watch_directories = watch_directories
        self.scan_interval = scan_interval
        self.file_states = {}
        self.handlers = {}
        self.is_watching = False
        self.watcher_thread = None
        
        # Initialize file states
        self._initialize_file_states()
    
    def _initialize_file_states(self):
        """Initialize tracking of all files in watch directories"""
        for directory in self.watch_directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_hash = self._get_file_hash(file_path)
                        self.file_states[file_path] = {
                            'hash': file_hash,
                            'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                            'modified': os.path.getmtime(file_path) if os.path.exists(file_path) else 0,
                            'last_checked': datetime.now().isoformat()
                        }
    
    def add_handler(self, file_pattern: str, handler: Callable):
        """Add file change handler for specific pattern"""
        self.handlers[file_pattern] = handler
        print(f"✅ Added handler for pattern: {file_pattern}")
    
    def start_watching(self):
        """Start the file watching process"""
        self.is_watching = True
        self.watcher_thread = threading.Thread(target=self._watch_loop)
        self.watcher_thread.daemon = True
        self.watcher_thread.start()
        print(f"👀 Started watching {len(self.watch_directories)} directories")
    
    def stop_watching(self):
        """Stop the file watching process"""
        self.is_watching = False
        if self.watcher_thread:
            self.watcher_thread.join(timeout=5)
        print("🛑 Stopped file watching")
    
    def _watch_loop(self):
        """Main watching loop"""
        while self.is_watching:
            try:
                self._check_for_changes()
                time.sleep(self.scan_interval)
            except Exception as e:
                print(f"❌ File watcher error: {e}")
                time.sleep(self.scan_interval)
    
    def _check_for_changes(self):
        """Check all watched directories for changes"""
        changes_detected = []
        
        for directory in self.watch_directories:
            if not os.path.exists(directory):
                continue
                
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    changes = self._check_file_changes(file_path)
                    if changes:
                        changes_detected.extend(changes)
        
        # Process detected changes
        for change in changes_detected:
            self._handle_file_change(change)
    
    def _check_file_changes(self, file_path: str) -> List[Dict[str, Any]]:
        """Check for changes in a specific file"""
        changes = []
        
        try:
            current_hash = self._get_file_hash(file_path)
            current_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            current_modified = os.path.getmtime(file_path) if os.path.exists(file_path) else 0
            
            previous_state = self.file_states.get(file_path, {})
            previous_hash = previous_state.get('hash', '')
            previous_size = previous_state.get('size', 0)
            previous_modified = previous_state.get('modified', 0)
            
            # Check for new file
            if file_path not in self.file_states:
                changes.append({
                    'file_path': file_path,
                    'change_type': 'created',
                    'timestamp': datetime.now().isoformat(),
                    'size': current_size,
                    'hash': current_hash
                })
            
            # Check for modified file
            elif (current_hash != previous_hash or 
                  current_modified != previous_modified):
                
                change_type = 'modified'
                if current_size > previous_size:
                    change_type = 'content_added'
                elif current_size < previous_size:
                    change_type = 'content_removed'
                
                changes.append({
                    'file_path': file_path,
                    'change_type': change_type,
                    'timestamp': datetime.now().isoformat(),
                    'previous_size': previous_size,
                    'current_size': current_size,
                    'previous_hash': previous_hash,
                    'current_hash': current_hash
                })
            
            # Check for deleted file
            elif not os.path.exists(file_path) and file_path in self.file_states:
                changes.append({
                    'file_path': file_path,
                    'change_type': 'deleted',
                    'timestamp': datetime.now().isoformat(),
                    'previous_size': previous_size,
                    'previous_hash': previous_hash
                })
            
            # Update file state
            self.file_states[file_path] = {
                'hash': current_hash,
                'size': current_size,
                'modified': current_modified,
                'last_checked': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error checking file {file_path}: {e}")
        
        return changes
    
    def _handle_file_change(self, change: Dict[str, Any]):
        """Handle detected file change"""
        file_path = change['file_path']
        change_type = change['change_type']
        
        print(f"📁 File {change_type}: {os.path.basename(file_path)}")
        
        # Find matching handler
        matched_handler = None
        for pattern, handler in self.handlers.items():
            if self._pattern_matches(file_path, pattern):
                matched_handler = handler
                break
        
        # Execute handler if found
        if matched_handler:
            try:
                matched_handler(change)
                print(f"✅ Handled {change_type} for {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Handler error for {file_path}: {e}")
        else:
            print(f"⚠️  No handler for {file_path}")
    
    def _pattern_matches(self, file_path: str, pattern: str) -> bool:
        """Check if file path matches pattern"""
        filename = os.path.basename(file_path)
        
        # Exact match
        if pattern == filename:
            return True
        
        # Extension match
        if pattern.startswith('*.') and filename.endswith(pattern[1:]):
            return True
        
        # Prefix match
        if pattern.endswith('*') and filename.startswith(pattern[:-1]):
            return True
        
        # Suffix match
        if pattern.startswith('*') and filename.endswith(pattern[1:]):
            return True
        
        # Directory pattern
        if '/' in pattern or '\\' in pattern:
            return file_path.replace('\\', '/').endswith(pattern.replace('\\', '/'))
        
        return False
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash for file content"""
        if not os.path.exists(file_path):
            return ''
        
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ''
    
    def get_watch_stats(self) -> Dict[str, Any]:
        """Get file watching statistics"""
        total_files = len(self.file_states)
        active_handlers = len(self.handlers)
        
        file_types = {}
        for file_path in self.file_states:
            ext = os.path.splitext(file_path)[1].lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            'total_watched_files': total_files,
            'active_handlers': active_handlers,
            'file_type_distribution': file_types,
            'watch_directories': self.watch_directories,
            'scan_interval': self.scan_interval,
            'is_active': self.is_watching
        }
    
    def add_watch_directory(self, directory: str):
        """Add new directory to watch list"""
        if directory not in self.watch_directories:
            self.watch_directories.append(directory)
            self._initialize_file_states()  # Reinitialize to include new directory
            print(f"✅ Added watch directory: {directory}")
    
    def remove_watch_directory(self, directory: str):
        """Remove directory from watch list"""
        if directory in self.watch_directories:
            self.watch_directories.remove(directory)
            # Remove file states from removed directory
            paths_to_remove = [path for path in self.file_states if path.startswith(directory)]
            for path in paths_to_remove:
                del self.file_states[path]
            print(f"✅ Removed watch directory: {directory}")
    
    def force_scan(self):
        """Force immediate scan of all watched directories"""
        print("🔍 Forcing immediate scan...")
        self._check_for_changes()
