# extract_files_from_conversation.py

import os
import re
import json
from pathlib import Path

class FileExtractor:
    def __init__(self, conversation_file: str = "ai-co-author.txt"):
        self.conversation_file = conversation_file
        self.conversation_data = ""
        self.extracted_files = {}
        
    def load_conversation(self):
        """Load the entire conversation"""
        print(f"📖 Loading conversation from: {self.conversation_file}")
        try:
            with open(self.conversation_file, 'r', encoding='utf-8') as f:
                self.conversation_data = f.read()
            print(f"✅ Loaded {len(self.conversation_data)} characters")
            return True
        except Exception as e:
            print(f"❌ Failed to load: {e}")
            return False
    
    def extract_all_files(self):
        """Extract all file contents from the conversation"""
        print("🔍 Extracting files from conversation...")
        
        # Pattern to match file blocks in the conversation
        file_pattern = r'## File \d+: `([^`]+)`\s*```(?:python|json|html|css|javascript|markdown|yaml)?\s*([\s\S]*?)```'
        
        matches = re.findall(file_pattern, self.conversation_data)
        
        for filepath, content in matches:
            # Clean up the content
            content = content.strip()
            if content:
                self.extracted_files[filepath] = content
                print(f"📄 Found: {filepath} ({len(content)} chars)")
        
        print(f"✅ Extracted {len(self.extracted_files)} files")
        return self.extracted_files
    
    def create_directory_structure(self):
        """Create the necessary directory structure"""
        print("📁 Creating directory structure...")
        
        directories = [
            'src/core',
            'src/processing', 
            'src/generation',
            'src/utils',
            'training_data/documents',
            'training_data/images',
            'training_data/audio',
            'training_data/snippets',
            'training_data/processing',
            'training_data/tasks',
            'training_data/platforms',
            'outputs/stories',
            'outputs/images',
            'outputs/text',
            'outputs/audio',
            'config',
            'models',
            'github_pages/templates',
            'github_pages/static',
            'browser_extension/icons',
            'extension_build',
            'analysis_results'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"   Created: {directory}/")
        
        print("✅ Directory structure created")
    
    def write_all_files(self):
        """Write all extracted files to disk"""
        print("💾 Writing files to disk...")
        
        files_written = 0
        for filepath, content in self.extracted_files.items():
            try:
                # Create parent directories if needed
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ Written: {filepath}")
                files_written += 1
                
            except Exception as e:
                print(f"   ❌ Failed to write {filepath}: {e}")
        
        print(f"✅ Successfully wrote {files_written}/{len(self.extracted_files)} files")
        return files_written
    
    def create_requirements_file(self):
        """Create requirements.txt from conversation"""
        print("📦 Creating requirements.txt...")
        
        requirements_content = """# Core dependencies
python>=3.8

# File processing
watchdog>=3.0.0
PyYAML>=6.0
python-magic>=0.4.27

# Archive handling
patool>=1.12

# Web framework
flask>=2.0.0
flask-socketio>=5.0.0

# Image processing
Pillow>=9.0.0

# Browser automation
selenium>=4.0.0
webdriver-manager>=3.0.0

# Utility libraries
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
"""
        
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print("✅ requirements.txt created")
    
    def run_complete_extraction(self):
        """Run the complete file extraction process"""
        if not self.load_conversation():
            return False
        
        self.extract_all_files()
        self.create_directory_structure()
        self.create_requirements_file()
        files_written = self.write_all_files()
        
        print("\n" + "="*60)
        print("🎉 FILE EXTRACTION COMPLETE!")
        print("="*60)
        print(f"📊 Summary:")
        print(f"   Files extracted from conversation: {len(self.extracted_files)}")
        print(f"   Files written to disk: {files_written}")
        print(f"   Directory structure: Created")
        print(f"   Requirements: Created")
        
        if files_written > 0:
            print(f"\n🚀 Next steps:")
            print(f"   1. Run: pip install -r requirements.txt")
            print(f"   2. Run: python run_complete_system.py")
            print(f"   3. Or run: python main.py")
        else:
            print(f"\n❌ No files were written. Check the conversation format.")
        
        return files_written > 0

def main():
    """Main function - extract all files and set up the project"""
    extractor = FileExtractor()
    success = extractor.run_complete_extraction()
    
    if success:
        print("\n✅ Project is now ready to run!")
    else:
        print("\n❌ Project setup failed")

if __name__ == "__main__":
    main()
