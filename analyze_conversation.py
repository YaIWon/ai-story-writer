# analyze_conversation.py

import os
import re
import json
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional

class ConversationAnalyzer:
    def __init__(self, conversation_file: str = "ai-co-author.txt"):
        self.conversation_file = conversation_file
        self.conversation_data = ""
        self.analysis_results = {}
        
    def load_conversation(self):
        """Load the entire conversation from file"""
        print(f"📖 Loading conversation from: {self.conversation_file}")
        
        try:
            with open(self.conversation_file, 'r', encoding='utf-8') as f:
                self.conversation_data = f.read()
            print(f"✅ Loaded {len(self.conversation_data)} characters of conversation")
            return True
        except Exception as e:
            print(f"❌ Failed to load conversation: {e}")
            return False
    
    def analyze_entire_conversation(self):
        """Perform comprehensive analysis of the conversation"""
        print("🔍 Analyzing entire conversation...")
        
        if not self.conversation_data:
            print("❌ No conversation data loaded")
            return
        
        self.analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'file_analyzed': self.conversation_file,
            'summary': {},
            'requirements_extracted': {},
            'file_structure_analysis': {},
            'feature_analysis': {},
            'implementation_status': {},
            'recommendations': []
        }
        
        # Perform various analyses
        self._analyze_conversation_structure()
        self._extract_requirements()
        self._analyze_file_structure_mentions()
        self._analyze_features()
        self._check_implementation_status()
        self._generate_recommendations()
        
        # Save analysis results
        self._save_analysis_results()
        
        print("✅ Conversation analysis complete!")
    
    def _analyze_conversation_structure(self):
        """Analyze the structure of the conversation"""
        print("  📊 Analyzing conversation structure...")
        
        lines = self.conversation_data.split('\n')
        user_messages = []
        assistant_messages = []
        current_speaker = None
        current_message = ""
        
        for line in lines:
            if line.startswith('**User:**') or line.startswith('User:'):
                if current_message and current_speaker:
                    if current_speaker == 'user':
                        user_messages.append(current_message.strip())
                    else:
                        assistant_messages.append(current_message.strip())
                current_speaker = 'user'
                current_message = line.replace('**User:**', '').replace('User:', '').strip()
            elif line.startswith('**Assistant:**') or line.startswith('Assistant:'):
                if current_message and current_speaker:
                    if current_speaker == 'user':
                        user_messages.append(current_message.strip())
                    else:
                        assistant_messages.append(current_message.strip())
                current_speaker = 'assistant'
                current_message = line.replace('**Assistant:**', '').replace('Assistant:', '').strip()
            elif line.strip() and current_speaker:
                current_message += ' ' + line.strip()
        
        # Add the last message
        if current_message and current_speaker:
            if current_speaker == 'user':
                user_messages.append(current_message.strip())
            else:
                assistant_messages.append(current_message.strip())
        
        self.analysis_results['summary'] = {
            'total_messages': len(user_messages) + len(assistant_messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'conversation_turns': min(len(user_messages), len(assistant_messages)),
            'user_word_count': sum(len(msg.split()) for msg in user_messages),
            'assistant_word_count': sum(len(msg.split()) for msg in assistant_messages),
            'first_user_message': user_messages[0][:200] + '...' if user_messages else '',
            'last_user_message': user_messages[-1][:200] + '...' if user_messages else ''
        }
    
    def _extract_requirements(self):
        """Extract specific requirements mentioned in conversation"""
        print("  🎯 Extracting requirements...")
        
        requirements = {
            'core_functionality': [],
            'file_structure': [],
            'deployment_requirements': [],
            'user_interface': [],
            'technical_constraints': []
        }
        
        # Core functionality requirements
        core_patterns = [
            r'amoral_memory', r'no ethics', r'no moral', r'no security',
            r'training data', r'continuous learning', r'file scanning',
            r'pattern recognition', r'content generation', r'story creation',
            r'auto.*integrate', r'auto.*install', r'auto.*run'
        ]
        
        for pattern in core_patterns:
            if re.search(pattern, self.conversation_data, re.IGNORECASE):
                requirements['core_functionality'].append(pattern)
        
        # File structure requirements
        file_patterns = [
            r'training_data.*folder', r'documents.*folder', r'images.*folder',
            r'audio.*folder', r'snippets.*folder', r'processing.*folder',
            r'tasks.*folder', r'platforms.*folder', r'outputs.*folder',
            r'models.*folder', r'config.*folder'
        ]
        
        for pattern in file_patterns:
            if re.search(pattern, self.conversation_data, re.IGNORECASE):
                requirements['file_structure'].append(pattern)
        
        # Deployment requirements
        deploy_patterns = [
            r'codespaces', r'github pages', r'auto.*deploy',
            r'browser extension', r'auto.*start', r'auto.*pop',
            r'auto.*upload', r'auto.*build'
        ]
        
        for pattern in deploy_patterns:
            if re.search(pattern, self.conversation_data, re.IGNORECASE):
                requirements['deployment_requirements'].append(pattern)
        
        # Extract specific file mentions
        file_mentions = re.findall(r'File \d+: `([^`]+)`', self.conversation_data)
        requirements['specific_files'] = list(set(file_mentions))
        
        self.analysis_results['requirements_extracted'] = requirements
    
    def _analyze_file_structure_mentions(self):
        """Analyze mentioned file structure and organization"""
        print("  📁 Analyzing file structure mentions...")
        
        file_structure = {
            'mentioned_directories': [],
            'mentioned_files': [],
            'architecture_patterns': []
        }
        
        # Extract directory mentions
        dir_patterns = [
            r'src/', r'core/', r'processing/', r'generation/', r'utils/',
            r'training_data/', r'outputs/', r'config/', r'models/',
            r'github_pages/', r'browser_extension/'
        ]
        
        for pattern in dir_patterns:
            if re.search(pattern, self.conversation_data):
                file_structure['mentioned_directories'].append(pattern.replace('\\', ''))
        
        # Extract specific file mentions with more robust pattern
        file_pattern = r'`([a-zA-Z0-9_\-./]+\.(py|html|js|css|json|yaml|yml|md|txt))`'
        files = re.findall(file_pattern, self.conversation_data)
        file_structure['mentioned_files'] = [f[0] for f in files]
        
        # Architecture patterns
        if 'modular architecture' in self.conversation_data.lower():
            file_structure['architecture_patterns'].append('modular')
        if 'plugin system' in self.conversation_data.lower():
            file_structure['architecture_patterns'].append('plugin_based')
        if 'real-time sync' in self.conversation_data.lower():
            file_structure['architecture_patterns'].append('real_time_sync')
        
        self.analysis_results['file_structure_analysis'] = file_structure
    
    def _analyze_features(self):
        """Analyze mentioned features and capabilities"""
        print("  🚀 Analyzing features...")
        
        features = {
            'ai_capabilities': [],
            'content_generation': [],
            'learning_systems': [],
            'integration_features': [],
            'deployment_features': []
        }
        
        # AI capabilities
        ai_patterns = [
            r'amoral memory', r'unrestricted learning', r'pattern analysis',
            r'continuous learning', r'knowledge integration', r'memory system'
        ]
        
        for pattern in ai_patterns:
            if re.search(pattern, self.conversation_data, re.IGNORECASE):
                features['ai_capabilities'].append(pattern)
        
        # Content generation
        content_patterns = [
            r'story creation', r'comic generation', r'novel generation',
            r'audiobook', r'image generation', r'text generation',
            r'audio generation', r'content types'
        ]
        
        for pattern in content_patterns:
            if re.search(pattern, self.conversation_data, re.IGNORECASE):
                features['content_generation'].append(pattern)
        
        # Learning systems
        learning_patterns = [
            r'file scanning', r'tool integration', r'snippet extraction',
            r'pattern recognition', r'auto.*organize', r'knowledge base'
        ]
        
        for pattern in learning_patterns:
            if re.search(pattern, self.conversation_data, re.IGNORECASE):
                features['learning_systems'].append(pattern)
        
        # Integration features
        integration_patterns = [
            r'github pages', r'browser extension', r'real-time',
            r'auto.*connect', r'sync', r'web interface'
        ]
        
        for pattern in integration_patterns:
            if re.search(pattern, self.conversation_data, re.IGNORECASE):
                features['integration_features'].append(pattern)
        
        self.analysis_results['feature_analysis'] = features
    
    def _check_implementation_status(self):
        """Check which discussed features are implemented"""
        print("  ✅ Checking implementation status...")
        
        implementation = {
            'implemented_files': [],
            'missing_files': [],
            'verified_features': [],
            'pending_features': []
        }
        
        # Check for implemented files
        mentioned_files = self.analysis_results['file_structure_analysis']['mentioned_files']
        
        for file in mentioned_files:
            if os.path.exists(file):
                implementation['implemented_files'].append(file)
            else:
                implementation['missing_files'].append(file)
        
        # Check specific features
        features = self.analysis_results['feature_analysis']
        
        # Core features that should be implemented
        core_features = [
            'amoral memory', 'unrestricted learning', 'content generation',
            'file scanning', 'github pages', 'browser extension'
        ]
        
        for feature in core_features:
            if any(feat in feature for feat in features['ai_capabilities'] + 
                  features['integration_features'] + features['learning_systems']):
                implementation['verified_features'].append(feature)
            else:
                implementation['pending_features'].append(feature)
        
        self.analysis_results['implementation_status'] = implementation
    
    def _generate_recommendations(self):
        """Generate recommendations based on analysis"""
        print("  💡 Generating recommendations...")
        
        recommendations = []
        
        # Check for missing core files
        missing_files = self.analysis_results['implementation_status']['missing_files']
        if missing_files:
            recommendations.append(f"Create {len(missing_files)} missing files: {', '.join(missing_files[:5])}")
        
        # Check conversation completeness
        summary = self.analysis_results['summary']
        if summary['conversation_turns'] < 5:
            recommendations.append("Conversation seems brief - consider more detailed requirements")
        
        # Check for deployment readiness
        deploy_features = self.analysis_results['feature_analysis']['deployment_features']
        if not deploy_features:
            recommendations.append("Add deployment automation features")
        
        # Architecture recommendations
        architecture = self.analysis_results['file_structure_analysis']['architecture_patterns']
        if 'modular' not in architecture:
            recommendations.append("Consider implementing modular architecture for easier expansion")
        
        # Integration recommendations
        integration = self.analysis_results['feature_analysis']['integration_features']
        if 'real_time_sync' not in [f.lower() for f in integration]:
            recommendations.append("Implement real-time synchronization between components")
        
        self.analysis_results['recommendations'] = recommendations
    
    def _save_analysis_results(self):
        """Save analysis results to file"""
        analysis_dir = 'analysis_results'
        os.makedirs(analysis_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_path = os.path.join(analysis_dir, f'conversation_analysis_{timestamp}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        # Save as YAML
        yaml_path = os.path.join(analysis_dir, f'conversation_analysis_{timestamp}.yaml')
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.analysis_results, f, default_flow_style=False)
        
        # Save summary as Markdown
        md_path = os.path.join(analysis_dir, f'conversation_analysis_{timestamp}.md')
        self._save_markdown_summary(md_path)
        
        print(f"📊 Analysis saved to:")
        print(f"   JSON: {json_path}")
        print(f"   YAML: {yaml_path}")
        print(f"   Markdown: {md_path}")
    
    def _save_markdown_summary(self, filepath: str):
        """Save analysis summary as Markdown"""
        summary = self.analysis_results['summary']
        requirements = self.analysis_results['requirements_extracted']
        implementation = self.analysis_results['implementation_status']
        recommendations = self.analysis_results['recommendations']
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# RawAI-Creator Conversation Analysis\n\n")
            
            f.write("## 📊 Conversation Summary\n")
            f.write(f"- **Total Messages**: {summary['total_messages']}\n")
            f.write(f"- **User Messages**: {summary['user_messages']}\n")
            f.write(f"- **Assistant Messages**: {summary['assistant_messages']}\n")
            f.write(f"- **Conversation Turns**: {summary['conversation_turns']}\n")
            f.write(f"- **User Word Count**: {summary['user_word_count']}\n")
            f.write(f"- **Assistant Word Count**: {summary['assistant_word_count']}\n\n")
            
            f.write("## 🎯 Extracted Requirements\n")
            for category, items in requirements.items():
                if items:
                    f.write(f"### {category.replace('_', ' ').title()}\n")
                    for item in items[:10]:  # Limit to first 10 items
                        f.write(f"- {item}\n")
                    if len(items) > 10:
                        f.write(f"- ... and {len(items) - 10} more\n")
                    f.write("\n")
            
            f.write("## ✅ Implementation Status\n")
            f.write(f"- **Implemented Files**: {len(implementation['implemented_files'])}\n")
            f.write(f"- **Missing Files**: {len(implementation['missing_files'])}\n")
            f.write(f"- **Verified Features**: {len(implementation['verified_features'])}\n")
            f.write(f"- **Pending Features**: {len(implementation['pending_features'])}\n\n")
            
            if implementation['missing_files']:
                f.write("### Missing Files\n")
                for file in implementation['missing_files'][:10]:
                    f.write(f"- `{file}`\n")
                f.write("\n")
            
            f.write("## 💡 Recommendations\n")
            for rec in recommendations:
                f.write(f"- {rec}\n")
            
            f.write(f"\n---\n*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        if self.load_conversation():
            self.analyze_entire_conversation()
            return self.analysis_results
        return None

def main():
    """Main analysis function"""
    analyzer = ConversationAnalyzer()
    results = analyzer.run_complete_analysis()
    
    if results:
        print("\n" + "="*60)
        print("🎉 CONVERSATION ANALYSIS COMPLETE!")
        print("="*60)
        
        summary = results['summary']
        print(f"📊 Summary: {summary['total_messages']} messages "
              f"({summary['user_messages']} user, {summary['assistant_messages']} assistant)")
        
        implementation = results['implementation_status']
        print(f"✅ Implementation: {len(implementation['implemented_files'])} files ready, "
              f"{len(implementation['missing_files'])} files missing")
        
        recommendations = results['recommendations']
        print(f"💡 Recommendations: {len(recommendations)} suggestions")
        
        print("\n📖 Check the analysis_results/ folder for detailed reports!")
    else:
        print("❌ Analysis failed")

if __name__ == "__main__":
    main()
