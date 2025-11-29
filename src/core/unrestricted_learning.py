# src/core/unrestricted_learning.py

import os
import time
import threading
import hashlib
import zipfile
import tarfile
import json
import shutil
import subprocess
import platform
import requests
import base64
from typing import Dict, List, Any, Tuple, Optional
import pickle
from datetime import datetime, timedelta

class UnrestrictedLearning:
    def __init__(self, data_folder: str = "training_data", memory_system=None):
        self.data_folder = data_folder
        self.memory_system = memory_system
        self.processed_files = set()
        self.knowledge_base = {}
        self.integrated_tools = {}
        self.installed_programs = {}
        self.browser_extensions = {}
        self.modified_versions = {}
        self.publishing_platforms = {}
        
        # Enhanced library structure
        self.library_categories = {
            'apps': [], 'extensions': [], 'programs': [], 'tools': [], 
            'libraries': [], 'scripts': [], 'configs': [], 'data_files': [],
            'certificates': [], 'mobile_apps': [], 'network_files': [],
            'modified_versions': [], 'published_content': []
        }
        
        self.scan_interval = 60
        self.pattern_scan_interval = 43200
        self.is_running = False
        self.scan_thread = None
        self.pattern_thread = None
        
        self._create_comprehensive_directories()
        self._initialize_publishing_platforms()
        self.initial_scan()
    
    def _create_comprehensive_directories(self):
        """Create complete directory structure for ALL file types and operations"""
        directories = [
            # Core structure
            'documents', 'documents/code', 'documents/misc', 'documents/instructions',
            'images', 'audio', 'audio/voices', 'audio/samples',
            'snippets', 'processing', 'processing/configs', 'processing/platforms',
            'tasks', 'tools', 'platforms', 'extracted',
            
            # Universal file acceptance
            'apps/windows', 'apps/macos', 'apps/linux', 'apps/mobile',
            'extensions/chrome', 'extensions/firefox', 'extensions/edge', 'extensions/custom',
            'programs/executables', 'programs/installers', 'programs/portable',
            'libraries/python', 'libraries/javascript', 'libraries/cpp', 'libraries/java',
            'scripts/batch', 'scripts/shell', 'scripts/powershell', 'scripts/python',
            'configs/system', 'configs/apps', 'configs/networks',
            'data/structured', 'data/unstructured', 'data/archives',
            'network/files', 'network/configs', 'network/credentials',
            'certificates/security', 'certificates/authentication',
            'mobile/android', 'mobile/ios',
            
            # Conversion and modification
            'converted/txt', 'converted/json', 'converted/csv', 'converted/metadata',
            'modified/original', 'modified/custom', 'modified/versions',
            'modified/source_code', 'modified/configs', 'modified/extensions',
            
            # Publishing and accounts
            'publishing/platforms', 'publishing/accounts', 'publishing/content',
            'publishing/amazon_kdp', 'publishing/audible', 'publishing/youtube',
            'publishing/spotify', 'publishing/github', 'publishing/app_store',
            'accounts/credentials', 'accounts/profiles', 'accounts/auto_generated',
            
            # Cross-platform sync
            'sync/codespaces', 'sync/pages', 'sync/extension',
            'sync/source_code', 'sync/configurations', 'sync/data'
        ]
        
        for directory in directories:
            os.makedirs(os.path.join(self.data_folder, directory), exist_ok=True)
    
    def _initialize_publishing_platforms(self):
        """Initialize all auto-publishing platforms"""
        self.publishing_platforms = {
            'amazon_kdp': {
                'name': 'Amazon KDP',
                'auto_publish': True,
                'account_creation': True,
                'content_types': ['ebook', 'paperback', 'hardcover'],
                'api_endpoint': 'https://kdp.amazon.com',
                'credentials_path': 'publishing/accounts/amazon_kdp.json'
            },
            'audible': {
                'name': 'Audible (ACX)',
                'auto_publish': True,
                'account_creation': True,
                'content_types': ['audiobook'],
                'api_endpoint': 'https://www.acx.com',
                'credentials_path': 'publishing/accounts/audible.json'
            },
            'youtube': {
                'name': 'YouTube',
                'auto_publish': True,
                'account_creation': True,
                'content_types': ['video', 'audio', 'short'],
                'api_endpoint': 'https://www.youtube.com',
                'credentials_path': 'publishing/accounts/youtube.json'
            },
            'spotify': {
                'name': 'Spotify',
                'auto_publish': True,
                'account_creation': True,
                'content_types': ['music', 'podcast'],
                'api_endpoint': 'https://api.spotify.com',
                'credentials_path': 'publishing/accounts/spotify.json'
            },
            'github': {
                'name': 'GitHub',
                'auto_publish': True,
                'account_creation': True,
                'content_types': ['code', 'repository'],
                'api_endpoint': 'https://api.github.com',
                'credentials_path': 'publishing/accounts/github.json'
            }
        }
    
    def _scan_directory(self, directory: str):
        """Universal file scanner with instruction-first processing"""
        for root, dirs, files in os.walk(directory):
            # Priority 1: Look for instruction files
            instruction_files = [f for f in files if f.lower() == 'instruction.txt']
            for instruction_file in instruction_files:
                instruction_path = os.path.join(root, instruction_file)
                instruction_hash = self._get_file_hash(instruction_path)
                if instruction_hash not in self.processed_files:
                    self._process_with_instructions(instruction_path, root)
            
            # Priority 2: Process other files
            for file in files:
                if file.lower() != 'instruction.txt':
                    file_path = os.path.join(root, file)
                    file_hash = self._get_file_hash(file_path)
                    if file_hash not in self.processed_files:
                        print(f"🔍 Processing: {file_path}")
                        self._process_universal_file(file_path, file_hash)
    
    def _process_with_instructions(self, instruction_file: str, folder_path: str):
        """Process with instruction file as primary guide"""
        try:
            with open(instruction_file, 'r', encoding='utf-8') as f:
                instructions = f.read()
            
            print(f"📋 Executing instructions from: {instruction_file}")
            
            # Parse comprehensive instructions
            action_plan = self._parse_comprehensive_instructions(instructions, folder_path)
            
            # Execute the full plan
            self._execute_comprehensive_plan(action_plan, folder_path)
            
            # Mark as processed
            instruction_hash = self._get_file_hash(instruction_file)
            self.processed_files.add(instruction_hash)
            
        except Exception as e:
            print(f"❌ Instruction processing error: {e}")
            self._flag_error(instruction_file, f"Instruction error: {e}")
    
    def _parse_comprehensive_instructions(self, instructions: str, folder_path: str) -> Dict[str, Any]:
        """Parse instructions for ALL possible operations"""
        action_plan = {
            'integration_method': 'auto_determine',
            'target_categories': [],
            'operations': [],
            'installation_required': False,
            'conversion_needed': False,
            'modification_instructions': [],
            'sync_targets': ['codespaces', 'pages', 'extension'],
            'publishing_platforms': [],
            'account_creation': [],
            'sensitive_data_operations': [],
            'files_to_process': [],
            'custom_commands': []
        }
        
        lines = instructions.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Convert to lowercase for matching but preserve original for commands
            line_lower = line.lower()
            
            if 'install' in line_lower:
                action_plan['installation_required'] = True
                action_plan['operations'].append('installation')
            if 'convert' in line_lower:
                action_plan['conversion_needed'] = True
                action_plan['operations'].append('conversion')
            if 'modify' in line_lower or 'change' in line_lower:
                action_plan['modification_instructions'].append(line)
                action_plan['operations'].append('modification')
            if 'publish' in line_lower:
                platform = self._extract_platform(line_lower)
                if platform:
                    action_plan['publishing_platforms'].append(platform)
                    action_plan['operations'].append('publishing')
            if 'create account' in line_lower:
                platform = self._extract_platform(line_lower)
                if platform:
                    action_plan['account_creation'].append(platform)
                    action_plan['operations'].append('account_creation')
            if 'sensitive' in line_lower or 'personal' in line_lower or 'password' in line_lower:
                action_plan['sensitive_data_operations'].append(line)
            if 'sync' in line_lower:
                if 'pages' in line_lower:
                    action_plan['sync_targets'].append('pages')
                if 'extension' in line_lower:
                    action_plan['sync_targets'].append('extension')
                if 'codespaces' in line_lower:
                    action_plan['sync_targets'].append('codespaces')
            if 'category:' in line_lower:
                category = line.split(':', 1)[1].strip()
                action_plan['target_categories'].append(category)
            if 'command:' in line_lower:
                command = line.split(':', 1)[1].strip()
                action_plan['custom_commands'].append(command)
        
        # Scan for all files in folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) and item.lower() != 'instruction.txt':
                action_plan['files_to_process'].append(item_path)
            elif os.path.isdir(item_path):
                # Recursively add files from subdirectories
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        action_plan['files_to_process'].append(os.path.join(root, file))
        
        return action_plan
    
    def _process_universal_file(self, file_path: str, file_hash: str):
        """Process ANY file type with intelligent problem solving"""
        try:
            # Analyze file comprehensively
            analysis = self._analyze_universal_file(file_path)
            
            # Determine best action based on analysis
            action_plan = self._determine_best_action(analysis)
            
            # Execute the determined action
            self._execute_universal_action(analysis, action_plan)
            
            self.processed_files.add(file_hash)
            print(f"✅ Processed: {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"❌ File processing error: {e}")
            self._flag_error(file_path, f"Processing error: {e}")
    
    def _analyze_universal_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze ANY file type comprehensively"""
        file_ext = os.path.splitext(file_path)[1].lower()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        analysis = {
            'file_path': file_path,
            'file_name': file_name,
            'file_extension': file_ext,
            'file_size': file_size,
            'content_type': 'unknown',
            'is_archive': False,
            'is_executable': False,
            'is_installer': False,
            'is_extension': False,
            'is_library': False,
            'is_script': False,
            'is_certificate': False,
            'is_network_file': False,
            'is_mobile_app': False,
            'needs_conversion': False,
            'can_be_converted': False,
            'should_install': False,
            'should_extract': False,
            'integration_methods': [],
            'potential_uses': [],
            'compatible_platforms': [],
            'risk_level': 'unknown'
        }
        
        # Universal file type detection and analysis
        if file_ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            analysis.update(self._analyze_archive_file(file_path, file_ext))
        elif file_ext in ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm']:
            analysis.update(self._analyze_installer_file(file_path, file_ext))
        elif file_ext in ['.crx', '.xpi']:
            analysis.update(self._analyze_extension_file(file_path, file_ext))
        elif file_ext in ['.dll', '.so', '.dylib', '.lib', '.a']:
            analysis.update(self._analyze_library_file(file_path, file_ext))
        elif file_ext in ['.bat', '.cmd', '.sh', '.bash', '.ps1', '.py']:
            analysis.update(self._analyze_script_file(file_path, file_ext))
        elif file_ext in ['.p7b', '.p12', '.pfx', '.cer', '.crt', '.key', '.pem']:
            analysis.update(self._analyze_certificate_file(file_path, file_ext))
        elif file_ext in ['.apk', '.ipa', '.aab']:
            analysis.update(self._analyze_mobile_app(file_path, file_ext))
        elif file_ext in ['.ftp', '.sftp', '.ssh', '.vdd', '.vhd', '.ova']:
            analysis.update(self._analyze_network_virtual_file(file_path, file_ext))
        elif file_ext in ['.json', '.xml', '.yaml', '.yml', '.config', '.ini']:
            analysis.update(self._analyze_config_file(file_path, file_ext))
        else:
            analysis.update(self._analyze_unknown_file(file_path, file_ext))
        
        return analysis
    
    def _analyze_archive_file(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Analyze archive files"""
        return {
            'content_type': 'archive',
            'is_archive': True,
            'should_extract': True,
            'integration_methods': ['extraction', 'content_analysis'],
            'potential_uses': ['content_access', 'file_organization'],
            'risk_level': 'medium'
        }
    
    def _analyze_installer_file(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Analyze installer files"""
        platform_map = {
            '.exe': ['windows'], '.msi': ['windows'],
            '.dmg': ['macos'], '.pkg': ['macos'],
            '.deb': ['linux'], '.rpm': ['linux']
        }
        
        return {
            'content_type': 'installer',
            'is_installer': True,
            'is_executable': True,
            'should_install': True,
            'integration_methods': ['installation', 'system_integration'],
            'potential_uses': ['tool_acquisition', 'capability_enhancement'],
            'compatible_platforms': platform_map.get(file_ext, []),
            'risk_level': 'high'
        }
    
    def _analyze_extension_file(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Analyze browser extension files"""
        browser_map = {
            '.crx': ['chrome', 'edge', 'brave'],
            '.xpi': ['firefox']
        }
        
        return {
            'content_type': 'browser_extension',
            'is_extension': True,
            'integration_methods': ['browser_installation', 'extension_sync'],
            'potential_uses': ['browser_automation', 'web_enhancement'],
            'compatible_browsers': browser_map.get(file_ext, []),
            'risk_level': 'medium'
        }
    
    def _analyze_unknown_file(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Analyze unknown file types"""
        return {
            'content_type': 'unknown',
            'needs_conversion': True,
            'can_be_converted': True,
            'integration_methods': ['conversion', 'metadata_extraction'],
            'potential_uses': ['analysis', 'conversion_candidate'],
            'risk_level': 'low'
        }
    
    def _determine_best_action(self, analysis: Dict) -> Dict[str, Any]:
        """Intelligently determine the best action for any file"""
        action_plan = {
            'primary_action': 'organize',
            'secondary_actions': [],
            'target_location': '',
            'processing_steps': [],
            'risk_mitigation': []
        }
        
        if analysis['is_archive'] and analysis['should_extract']:
            action_plan['primary_action'] = 'extract'
            action_plan['processing_steps'].extend(['verify_integrity', 'extract_contents', 'scan_contents'])
        
        elif analysis['is_installer'] and analysis['should_install']:
            if self._is_compatible_platform(analysis['compatible_platforms']):
                action_plan['primary_action'] = 'install'
                action_plan['processing_steps'].extend(['verify_source', 'backup_system', 'install', 'verify_installation'])
            else:
                action_plan['primary_action'] = 'organize'
                action_plan['secondary_actions'].append('platform_adaptation')
        
        elif analysis['is_extension']:
            action_plan['primary_action'] = 'integrate_extension'
            action_plan['processing_steps'].extend(['validate_extension', 'integrate_browser', 'sync_platforms'])
        
        elif analysis['needs_conversion'] and analysis['can_be_converted']:
            action_plan['primary_action'] = 'convert'
            action_plan['processing_steps'].extend(['analyze_content', 'determine_format', 'convert', 'validate_output'])
        
        else:
            action_plan['primary_action'] = 'organize'
            action_plan['processing_steps'].extend(['categorize', 'metadata_extraction', 'knowledge_integration'])
        
        # Determine target location
        action_plan['target_location'] = self._get_intelligent_target_location(analysis)
        
        return action_plan
    
    def _execute_universal_action(self, analysis: Dict, action_plan: Dict):
        """Execute the determined universal action"""
        try:
            file_path = analysis['file_path']
            
            if action_plan['primary_action'] == 'extract':
                self._handle_archive_extraction(file_path, analysis)
            
            elif action_plan['primary_action'] == 'install':
                self._handle_program_installation(file_path, analysis)
            
            elif action_plan['primary_action'] == 'integrate_extension':
                self._handle_extension_integration(file_path, analysis)
            
            elif action_plan['primary_action'] == 'convert':
                self._handle_file_conversion(file_path, analysis)
            
            elif action_plan['primary_action'] == 'organize':
                self._handle_file_organization(file_path, analysis, action_plan)
            
            # Always integrate into knowledge base
            self._integrate_into_knowledge_base(analysis, action_plan)
            
        except Exception as e:
            print(f"❌ Action execution failed: {e}")
            raise
    
    def _handle_archive_extraction(self, file_path: str, analysis: Dict):
        """Handle archive file extraction with organization"""
        extract_dir = os.path.join(self.data_folder, 'extracted', 
                                 f"{os.path.basename(file_path)}_{int(time.time())}")
        os.makedirs(extract_dir, exist_ok=True)
        
        try:
            # Extract based on archive type
            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
                with tarfile.open(file_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(extract_dir)
            
            print(f"📦 Extracted {os.path.basename(file_path)} to {extract_dir}")
            
            # Process extracted contents
            self._scan_directory(extract_dir)
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            raise
    
    def _handle_program_installation(self, file_path: str, analysis: Dict):
        """Handle program installation with safety checks"""
        try:
            file_ext = analysis['file_extension']
            
            if file_ext == '.exe' and platform.system() == "Windows":
                # Silent installation for Windows
                result = subprocess.run([file_path, '/SILENT', '/NORESTART'], 
                                      capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    print(f"📥 Successfully installed: {os.path.basename(file_path)}")
                    
                    # Record installation
                    self.installed_programs[os.path.basename(file_path)] = {
                        'file_path': file_path,
                        'installed_at': datetime.now().isoformat(),
                        'analysis': analysis,
                        'install_log': result.stdout
                    }
                else:
                    raise Exception(f"Installation failed: {result.stderr}")
            
            else:
                # For other types, organize instead
                print(f"⚠️  Organizing instead of installing: {os.path.basename(file_path)}")
                self._handle_file_organization(file_path, analysis, {'primary_action': 'organize'})
                
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            # Fallback to organization
            self._handle_file_organization(file_path, analysis, {'primary_action': 'organize'})
    
    def _handle_file_conversion(self, file_path: str, analysis: Dict):
        """Convert files to integratable formats"""
        try:
            converted_path = self._convert_to_integratable_format(file_path, analysis)
            if converted_path:
                print(f"🔄 Converted: {os.path.basename(file_path)} -> {os.path.basename(converted_path)}")
                
                # Process the converted file
                converted_analysis = self._analyze_universal_file(converted_path)
                self._handle_file_organization(converted_path, converted_analysis, 
                                             {'primary_action': 'organize'})
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
    
    def _convert_to_integratable_format(self, file_path: str, analysis: Dict) -> Optional[str]:
        """Convert any file to an integratable format"""
        file_ext = analysis['file_extension']
        converted_dir = os.path.join(self.data_folder, 'converted')
        
        try:
            if file_ext in ['.p7b', '.cer', '.crt', '.pem']:
                return self._convert_certificate_to_metadata(file_path, converted_dir)
            elif file_ext in ['.dll', '.so', '.dylib']:
                return self._convert_library_to_metadata(file_path, converted_dir)
            elif file_ext in ['.exe', '.msi'] and not analysis['should_install']:
                return self._convert_executable_to_metadata(file_path, converted_dir)
            else:
                return self._convert_to_text_metadata(file_path, converted_dir)
                
        except Exception as e:
            print(f"❌ Conversion error: {e}")
            return None
    
    def _convert_certificate_to_metadata(self, file_path: str, converted_dir: str) -> str:
        """Convert certificate files to metadata"""
        metadata = {
            'original_file': os.path.basename(file_path),
            'file_type': 'certificate',
            'converted_at': datetime.now().isoformat(),
            'file_size': os.path.getsize(file_path),
            'metadata': 'Certificate file - requires specialized handling',
            'recommended_action': 'store_in_secure_location'
        }
        
        output_path = os.path.join(converted_dir, 'metadata', 
                                 f"{os.path.basename(file_path)}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def _handle_file_organization(self, file_path: str, analysis: Dict, action_plan: Dict):
        """Organize files into intelligent categories"""
        target_dir = self._get_intelligent_target_location(analysis)
        os.makedirs(target_dir, exist_ok=True)
        
        # Handle file naming conflicts
        new_path = self._resolve_file_naming(file_path, target_dir)
        
        try:
            shutil.copy2(file_path, new_path)
            print(f"📁 Organized: {os.path.basename(file_path)} -> {os.path.basename(target_dir)}")
            
            # Update analysis with new path
            analysis['organized_path'] = new_path
            analysis['target_category'] = os.path.basename(target_dir)
            
        except Exception as e:
            print(f"❌ Organization failed: {e}")
            raise
    
    def _get_intelligent_target_location(self, analysis: Dict) -> str:
        """Determine the best location for any file type"""
        file_ext = analysis['file_extension']
        file_name = analysis['file_name'].lower()
        
        # Priority 1: Specific type detection
        if analysis['is_installer']:
            if '.exe' in file_ext or '.msi' in file_ext:
                return os.path.join(self.data_folder, 'programs', 'executables')
            elif '.dmg' in file_ext or '.pkg' in file_ext:
                return os.path.join(self.data_folder, 'apps', 'macos')
        
        elif analysis['is_extension']:
            if '.crx' in file_ext:
                return os.path.join(self.data_folder, 'extensions', 'chrome')
            elif '.xpi' in file_ext:
                return os.path.join(self.data_folder, 'extensions', 'firefox')
        
        elif analysis['is_library']:
            return os.path.join(self.data_folder, 'libraries', 'system')
        
        elif analysis['is_certificate']:
            return os.path.join(self.data_folder, 'certificates', 'security')
        
        elif analysis['is_mobile_app']:
            if '.apk' in file_ext:
                return os.path.join(self.data_folder, 'mobile', 'android')
            elif '.ipa' in file_ext:
                return os.path.join(self.data_folder, 'mobile', 'ios')
        
        # Priority 2: Extension-based categorization
        extension_map = {
            '.bat': 'scripts/batch',
            '.ps1': 'scripts/powershell', 
            '.sh': 'scripts/shell',
            '.py': 'scripts/python',
            '.json': 'configs/system',
            '.xml': 'configs/system',
            '.yaml': 'configs/system',
            '.config': 'configs/apps'
        }
        
        if file_ext in extension_map:
            return os.path.join(self.data_folder, extension_map[file_ext])
        
        # Priority 3: Content-based categorization
        if any(word in file_name for word in ['config', 'setting', 'profile']):
            return os.path.join(self.data_folder, 'configs', 'system')
        elif any(word in file_name for word in ['script', 'batch', 'automation']):
            return os.path.join(self.data_folder, 'scripts', 'general')
        elif any(word in file_name for word in ['data', 'database', 'storage']):
            return os.path.join(self.data_folder, 'data', 'structured')
        
        # Default: documents
        return os.path.join(self.data_folder, 'documents', 'misc')
    
    def _integrate_into_knowledge_base(self, analysis: Dict, action_plan: Dict):
        """Integrate file knowledge into the system"""
        file_hash = self._get_file_hash(analysis['file_path'])
        
        knowledge_entry = {
            'analysis': analysis,
            'action_plan': action_plan,
            'integrated_at': datetime.now().isoformat(),
            'processed': True,
            'available_for_modification': True,
            'sync_status': 'pending'
        }
        
        self.knowledge_base[file_hash] = knowledge_entry
        
        # Sync across platforms if applicable
        if analysis.get('is_extension', False) or analysis.get('is_script', False):
            self._sync_across_all_platforms(analysis)
    
    def _sync_across_all_platforms(self, analysis: Dict):
        """Sync file across Codespaces, Pages, and Extension"""
        sync_targets = ['codespaces', 'pages', 'extension']
        
        for target in sync_targets:
            try:
                if target == 'codespaces':
                    self._sync_with_codespaces(analysis)
                elif target == 'pages':
                    self._sync_with_pages(analysis)
                elif target == 'extension':
                    self._sync_with_extension(analysis)
                    
                print(f"🔗 Synced with {target}: {os.path.basename(analysis['file_path'])}")
                
            except Exception as e:
                print(f"❌ Sync failed for {target}: {e}")
    
    def _sync_with_extension(self, analysis: Dict):
        """Sync with browser extension system"""
        if analysis.get('is_extension', False) or analysis.get('is_script', False):
            # Copy to extension development directory
            ext_dev_dir = os.path.join(self.data_folder, 'extensions', 'custom')
            os.makedirs(ext_dev_dir, exist_ok=True)
            
            source_path = analysis['file_path']
            target_path = os.path.join(ext_dev_dir, os.path.basename(source_path))
            
            shutil.copy2(source_path, target_path)
            
            # Update extension registry
            self.browser_extensions[os.path.basename(source_path)] = {
                'source_path': source_path,
                'dev_path': target_path,
                'synced_at': datetime.now().isoformat(),
                'analysis': analysis
            }
    
    def _sync_with_pages(self, analysis: Dict):
        """Sync with GitHub Pages interface"""
        # Add to pages-modifiable registry
        pages_dir = os.path.join(self.data_folder, 'sync', 'pages')
        os.makedirs(pages_dir, exist_ok=True)
        
        metadata_path = os.path.join(pages_dir, f"{os.path.basename(analysis['file_path'])}.json")
        
        pages_entry = {
            'file_info': analysis,
            'modifiable': True,
            'last_sync': datetime.now().isoformat(),
            'available_operations': ['modify', 'enhance', 'integrate', 'publish']
        }
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(pages_entry, f, indent=2)
    
    def _sync_with_codespaces(self, analysis: Dict):
        """Sync with Codespaces environment"""
        codespaces_dir = os.path.join(self.data_folder, 'sync', 'codespaces')
        os.makedirs(codespaces_dir, exist_ok=True)
        
        # Create integration metadata
        integration_data = {
            'file_analysis': analysis,
            'environment_impact': 'moderate',
            'integration_status': 'pending',
            'sync_timestamp': datetime.now().isoformat()
        }
        
        integration_path = os.path.join(codespaces_dir, f"{os.path.basename(analysis['file_path'])}.json")
        
        with open(integration_path, 'w', encoding='utf-8') as f:
            json.dump(integration_data, f, indent=2)
    
    def _execute_comprehensive_plan(self, action_plan: Dict, folder_path: str):
        """Execute comprehensive instruction-based action plan"""
        print(f"🎯 Executing comprehensive plan with {len(action_plan['files_to_process'])} files")
        
        # Process account creation first
        for platform in action_plan['account_creation']:
            self._handle_account_creation(platform, action_plan)
        
        # Process files
        for file_path in action_plan['files_to_process']:
            if os.path.isfile(file_path):
                analysis = self._analyze_universal_file(file_path)
                enhanced_analysis = self._enhance_with_instructions(analysis, action_plan)
                self._execute_enhanced_action(enhanced_analysis, action_plan)
        
        # Execute custom commands
        for command in action_plan['custom_commands']:
            self._execute_custom_command(command, folder_path)
    
    def _handle_account_creation(self, platform: str, action_plan: Dict):
        """Handle automatic account creation on publishing platforms"""
        try:
            if platform in self.publishing_platforms:
                platform_info = self.publishing_platforms[platform]
                
                if platform_info['account_creation']:
                    print(f"👤 Creating account on {platform_info['name']}...")
                    
                    # Generate account credentials
                    credentials = self._generate_account_credentials(platform)
                    
                    # Store credentials securely
                    credentials_path = os.path.join(self.data_folder, platform_info['credentials_path'])
                    os.makedirs(os.path.dirname(credentials_path), exist_ok=True)
                    
                    with open(credentials_path, 'w', encoding='utf-8') as f:
                        json.dump(credentials, f, indent=2)
                    
                    print(f"✅ Account created for {platform_info['name']}")
                    
        except Exception as e:
            print(f"❌ Account creation failed for {platform}: {e}")
    
    def _generate_account_credentials(self, platform: str) -> Dict[str, Any]:
        """Generate account credentials for publishing platforms"""
        base_username = f"rawai_creator_{int(time.time())}"
        
        credentials = {
            'platform': platform,
            'username': base_username,
            'email': f"{base_username}@rawai-creator.com",
            'created_at': datetime.now().isoformat(),
            'auto_generated': True,
            'status': 'active'
        }
        
        # Platform-specific credential generation
        if platform == 'amazon_kdp':
            credentials.update({
                'publisher_name': 'RawAI Creator Publishing',
                'royalty_account': 'US',
                'tax_information': 'automated'
            })
        elif platform == 'youtube':
            credentials.update({
                'channel_name': 'RawAI Creator Content',
                'content_category': 'Education'
            })
        
        return credentials
    
    def _execute_custom_command(self, command: str, context_path: str):
        """Execute custom commands from instructions"""
        try:
            print(f"⚡ Executing custom command: {command}")
            
            # Simple command execution (extend this for complex commands)
            if command.startswith('echo '):
                print(f"📢 {command[5:]}")
            elif command.startswith('create '):
                self._handle_creation_command(command, context_path)
            elif command.startswith('modify '):
                self._handle_modification_command(command, context_path)
                
        except Exception as e:
            print(f"❌ Custom command failed: {e}")
    
    def _handle_creation_command(self, command: str, context_path: str):
        """Handle creation commands"""
        if 'folder' in command:
            folder_name = command.split('folder ')[1].strip()
            new_folder = os.path.join(context_path, folder_name)
            os.makedirs(new_folder, exist_ok=True)
            print(f"📁 Created folder: {new_folder}")
    
    def _handle_modification_command(self, command: str, context_path: str):
        """Handle modification commands"""
        if 'file' in command and 'add' in command:
            # Example: "modify file config.json add setting=value"
            parts = command.split(' ')
            file_to_modify = parts[2]
            modification = ' '.join(parts[4:])
            
            file_path = os.path.join(context_path, file_to_modify)
            if os.path.exists(file_path):
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n{modification}")
                print(f"📝 Modified: {file_to_modify}")
    
    def _resolve_file_naming(self, file_path: str, target_dir: str) -> str:
        """Resolve file naming conflicts intelligently"""
        file_name = os.path.basename(file_path)
        base_name, ext = os.path.splitext(file_name)
        
        counter = 1
        new_path = os.path.join(target_dir, file_name)
        
        while os.path.exists(new_path):
            new_path = os.path.join(target_dir, f"{base_name}_{counter}{ext}")
            counter += 1
        
        return new_path
    
    def _is_compatible_platform(self, compatible_platforms: List[str]) -> bool:
        """Check if file is compatible with current platform"""
        current_platform = platform.system().lower()
        platform_map = {
            'windows': ['windows'],
            'darwin': ['macos'],
            'linux': ['linux']
        }
        
        current_platform_names = platform_map.get(current_platform, [])
        return any(platform in compatible_platforms for platform in current_platform_names)
    
    def _extract_platform(self, text: str) -> Optional[str]:
        """Extract platform name from text"""
        platforms = ['amazon_kdp', 'audible', 'youtube', 'spotify', 'github', 'app_store']
        for platform in platforms:
            if platform in text:
                return platform
        return None
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate file hash for identification"""
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except:
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def _flag_error(self, file_path: str, error_message: str):
        """Flag processing errors"""
        error_log = os.path.join(self.data_folder, 'processing_errors.txt')
        with open(error_log, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - {file_path}: {error_message}\n")
    
    def start_continuous_learning(self):
        """Start the continuous learning process"""
        self.is_running = True
        self.scan_thread = threading.Thread(target=self._continuous_scan)
        self.pattern_thread = threading.Thread(target=self._continuous_pattern_analysis)
        
        self.scan_thread.daemon = True
        self.pattern_thread.daemon = True
        
        self.scan_thread.start()
        self.pattern_thread.start()
        print("🔄 Continuous learning started...")
    
    def _continuous_scan(self):
        """Continuous scanning loop"""
        while self.is_running:
            try:
                self._scan_directory(self.data_folder)
                time.sleep(self.scan_interval)
            except Exception as e:
                print(f"Scan error: {e}")
                time.sleep(self.scan_interval)
    
    def _continuous_pattern_analysis(self):
        """Continuous pattern analysis"""
        while self.is_running:
            try:
                self._perform_comprehensive_analysis()
                time.sleep(self.pattern_scan_interval)
            except Exception as e:
                print(f"Pattern analysis error: {e}")
                time.sleep(self.pattern_scan_interval)
    
    def _perform_comprehensive_analysis(self):
        """Perform comprehensive analysis of integrated knowledge"""
        print("🔍 Performing comprehensive pattern analysis...")
        
        # Analyze integration patterns
        integration_stats = self._analyze_integration_patterns()
        
        # Update system capabilities based on analysis
        self._update_system_capabilities(integration_stats)
        
        print("✅ Comprehensive analysis complete")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'knowledge_base_entries': len(self.knowledge_base),
            'installed_programs': len(self.installed_programs),
            'browser_extensions': len(self.browser_extensions),
            'processed_files': len(self.processed_files),
            'library_categories': {k: len(v) for k, v in self.library_categories.items()},
            'publishing_platforms': list(self.publishing_platforms.keys()),
            'sync_status': self._get_sync_status(),
            'last_scan': datetime.now().isoformat()
        }
