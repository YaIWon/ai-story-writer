# src/utils/config_loader.py

import os
import yaml
import json
from typing import Dict, Any, Optional
from datetime import datetime

class ConfigLoader:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.configs = {}
        self.watchers = {}
        
        os.makedirs(config_dir, exist_ok=True)
        self._load_all_configs()
    
    def _load_all_configs(self):
        """Load all configuration files from config directory"""
        config_files = [
            'user_ethics.yaml',
            'system_settings.yaml', 
            'publishing_platforms.yaml',
            'content_guidelines.yaml',
            'training_parameters.yaml',
            'sync_configurations.yaml'
        ]
        
        for config_file in config_files:
            self._load_config_file(config_file)
    
    def _load_config_file(self, filename: str):
        """Load a specific configuration file"""
        filepath = os.path.join(self.config_dir, filename)
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    if filename.endswith('.yaml') or filename.endswith('.yml'):
                        config_data = yaml.safe_load(f)
                    else:
                        config_data = json.load(f)
                
                config_name = os.path.splitext(filename)[0]
                self.configs[config_name] = config_data
                print(f"✅ Loaded config: {config_name}")
            else:
                # Create default config if doesn't exist
                self._create_default_config(filename)
                
        except Exception as e:
            print(f"❌ Error loading config {filename}: {e}")
            self.configs[os.path.splitext(filename)[0]] = {}
    
    def _create_default_config(self, filename: str):
        """Create default configuration file"""
        config_name = os.path.splitext(filename)[0]
        filepath = os.path.join(self.config_dir, filename)
        
        default_configs = {
            'user_ethics': {
                'ethical_framework': 'user_defined',
                'content_restrictions': [],
                'auto_moderation': False,
                'explicit_content_handling': 'store_all',
                'safety_checks': 'disabled',
                'user_override': True,
                'last_modified': datetime.now().isoformat()
            },
            'system_settings': {
                'scan_interval': 60,
                'pattern_analysis_interval': 43200,
                'max_file_size': 104857600,  # 100MB
                'backup_interval': 3600,
                'auto_update': True,
                'cross_platform_sync': True,
                'performance_optimization': 'balanced'
            },
            'publishing_platforms': {
                'amazon_kdp': {
                    'enabled': True,
                    'auto_publish': True,
                    'account_creation': True,
                    'default_categories': ['Fiction', 'Science Fiction', 'Fantasy'],
                    'royalty_settings': 'standard',
                    'publishing_rights': 'worldwide'
                },
                'audible': {
                    'enabled': True,
                    'auto_publish': True,
                    'account_creation': True,
                    'audio_quality': 'high',
                    'distribution_rights': 'worldwide'
                },
                'youtube': {
                    'enabled': True,
                    'auto_publish': True,
                    'account_creation': True,
                    'content_categories': ['Education', 'Entertainment'],
                    'monetization': True
                },
                'spotify': {
                    'enabled': True,
                    'auto_publish': True,
                    'account_creation': True,
                    'content_types': ['Audiobook', 'Podcast']
                }
            },
            'content_guidelines': {
                'quality_standards': 'professional',
                'length_requirements': {
                    'novel': 50000,
                    'comic': 24,
                    'audiobook': 3600,
                    'short_story': 5000
                },
                'formatting_standards': 'industry_standard',
                'accessibility_features': True,
                'multilingual_support': True
            },
            'training_parameters': {
                'learning_rate': 0.001,
                'batch_size': 32,
                'epochs': 100,
                'validation_split': 0.2,
                'early_stopping': True,
                'model_save_frequency': 10,
                'data_augmentation': True
            },
            'sync_configurations': {
                'codespaces_sync': True,
                'pages_sync': True,
                'extension_sync': True,
                'sync_interval': 300,
                'conflict_resolution': 'user_preference',
                'backup_before_sync': True,
                'encryption_enabled': False
            }
        }
        
        if config_name in default_configs:
            with open(filepath, 'w', encoding='utf-8') as f:
                if filename.endswith('.yaml') or filename.endswith('.yml'):
                    yaml.dump(default_configs[config_name], f, default_flow_style=False)
                else:
                    json.dump(default_configs[config_name], f, indent=2)
            
            self.configs[config_name] = default_configs[config_name]
            print(f"📝 Created default config: {config_name}")
    
    def get_config(self, config_name: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.configs.get(config_name, default)
    
    def update_config(self, config_name: str, updates: Dict[str, Any]):
        """Update configuration"""
        if config_name in self.configs:
            self.configs[config_name].update(updates)
            self.configs[config_name]['last_modified'] = datetime.now().isoformat()
            
            # Save to file
            filepath = os.path.join(self.config_dir, f"{config_name}.yaml")
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(self.configs[config_name], f, default_flow_style=False)
            
            print(f"✅ Updated config: {config_name}")
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """Get configuration for specific publishing platform"""
        platforms_config = self.configs.get('publishing_platforms', {})
        return platforms_config.get(platform, {})
    
    def is_platform_enabled(self, platform: str) -> bool:
        """Check if publishing platform is enabled"""
        platform_config = self.get_platform_config(platform)
        return platform_config.get('enabled', False)
    
    def get_sync_settings(self) -> Dict[str, Any]:
        """Get synchronization settings"""
        return self.configs.get('sync_configurations', {})
    
    def get_ethics_settings(self) -> Dict[str, Any]:
        """Get ethics and safety settings"""
        return self.configs.get('user_ethics', {})
    
    def get_system_settings(self) -> Dict[str, Any]:
        """Get system performance settings"""
        return self.configs.get('system_settings', {})
    
    def list_all_configs(self) -> Dict[str, Any]:
        """List all configurations with metadata"""
        config_info = {}
        for config_name, config_data in self.configs.items():
            config_info[config_name] = {
                'last_modified': config_data.get('last_modified', 'unknown'),
                'keys_count': len(config_data),
                'file_size': len(str(config_data).encode('utf-8'))
            }
        return config_info
    
    def export_config(self, config_name: str, export_path: str):
        """Export configuration to external file"""
        if config_name in self.configs:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.configs[config_name], f, indent=2)
            print(f"📤 Exported config {config_name} to {export_path}")
    
    def import_config(self, config_name: str, import_path: str):
        """Import configuration from external file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            self.update_config(config_name, imported_config)
            print(f"📥 Imported config {config_name} from {import_path}")
            
        except Exception as e:
            print(f"❌ Error importing config: {e}")
    
    def validate_config(self, config_name: str) -> Dict[str, Any]:
        """Validate configuration integrity"""
        if config_name not in self.configs:
            return {'valid': False, 'errors': ['Configuration not found']}
        
        config = self.configs[config_name]
        errors = []
        warnings = []
        
        # Platform-specific validation
        if config_name == 'publishing_platforms':
            for platform, settings in config.items():
                if not isinstance(settings, dict):
                    errors.append(f"Invalid platform settings for {platform}")
                    continue
                
                if settings.get('enabled', False) and not settings.get('account_creation', False):
                    warnings.append(f"Platform {platform} enabled but account creation disabled")
        
        # System settings validation
        elif config_name == 'system_settings':
            scan_interval = config.get('scan_interval', 60)
            if scan_interval < 10:
                warnings.append("Scan interval very short may impact performance")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'last_modified': config.get('last_modified', 'unknown')
        }
