# main.py

import os
import sys
import time
import webbrowser
import threading
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.amoral_memory import AmoralMemory
from core.unrestricted_learning import AdvancedUnrestrictedLearning
from core.content_generator import ContentGenerator
from processing.file_ingestor import FileIngestor
from processing.data_analyzer import DataAnalyzer
from generation.image_engine import ImageEngine
from generation.text_engine import TextEngine
from generation.audio_engine import AudioEngine
from utils.config_loader import ConfigLoader
from utils.file_watcher import FileWatcher

# Import the missing modules
try:
    from icon_generator import IconGenerator
    ICON_GENERATOR_AVAILABLE = True
except ImportError:
    print("⚠️  Icon generator not available")
    ICON_GENERATOR_AVAILABLE = False

try:
    from auto_extension_builder import AutoExtensionBuilder
    EXTENSION_BUILDER_AVAILABLE = True
except ImportError:
    print("⚠️  Extension builder not available")
    EXTENSION_BUILDER_AVAILABLE = False

try:
    from github_pages.app import GitHubPagesApp
    GITHUB_PAGES_AVAILABLE = True
except ImportError:
    print("⚠️  GitHub Pages not available")
    GITHUB_PAGES_AVAILABLE = False

class RawAICreator:
    def __init__(self):
        self.memory_system = None
        self.learning_system = None
        self.content_generator = None
        self.file_ingestor = None
        self.data_analyzer = None
        self.image_engine = None
        self.text_engine = None
        self.audio_engine = None
        self.config_loader = None
        self.file_watcher = None
        self.icon_generator = None
        self.extension_builder = None
        self.github_pages = None
        
        self.is_running = False
        
    def initialize_systems(self):
        """Initialize all AI systems"""
        print("🚀 INITIALIZING RAWAI-CREATOR SYSTEMS...")
        print("=" * 50)
        
        try:
            # 1. Configuration loader
            print("📋 Loading configuration...")
            self.config_loader = ConfigLoader()
            print("✅ Configuration loaded")
            
            # 2. Memory system (amoral - no ethics)
            print("🧠 Initializing amoral memory system...")
            self.memory_system = AmoralMemory()
            print("✅ Amoral memory system ready")
            
            # 3. Learning system (unrestricted) - FIXED: Using AdvancedUnrestrictedLearning
            print("📚 Initializing unrestricted learning...")
            self.learning_system = AdvancedUnrestrictedLearning(
                data_folder="training_data", 
                memory_system=self.memory_system
            )
            print("✅ Advanced unrestricted learning ready")
            
            # 4. Content generation
            print("🎨 Initializing content generators...")
            self.content_generator = ContentGenerator(
                memory_system=self.memory_system,
                learning_system=self.learning_system
            )
            self.image_engine = ImageEngine()
            self.text_engine = TextEngine(memory_system=self.memory_system)
            self.audio_engine = AudioEngine(memory_system=self.memory_system)
            print("✅ Content generators ready")
            
            # 5. File processing
            print("📁 Initializing file processors...")
            self.file_ingestor = FileIngestor()
            self.data_analyzer = DataAnalyzer()
            print("✅ File processors ready")
            
            # 6. File watcher for continuous learning
            print("👀 Initializing file watcher...")
            self.file_watcher = FileWatcher(
                file_ingestor=self.file_ingestor,
                learning_system=self.learning_system
            )
            print("✅ File watcher ready")
            
            # 7. Optional components
            if ICON_GENERATOR_AVAILABLE:
                print("🎨 Initializing icon generator...")
                self.icon_generator = IconGenerator()
                print("✅ Icon generator ready")
            
            if EXTENSION_BUILDER_AVAILABLE:
                print("🔨 Initializing extension builder...")
                self.extension_builder = AutoExtensionBuilder()
                print("✅ Extension builder ready")
            
            if GITHUB_PAGES_AVAILABLE:
                print("🌐 Initializing GitHub Pages...")
                self.github_pages = GitHubPagesApp(
                    memory_system=self.memory_system,
                    learning_system=self.learning_system,
                    content_generator=self.content_generator
                )
                print("✅ GitHub Pages ready")
            
            print("=" * 50)
            print("🎉 ALL SYSTEMS INITIALIZED SUCCESSFULLY!")
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start_complete_system(self):
        """Start the complete AI system"""
        if not self.initialize_systems():
            return False
        
        self.is_running = True
        print("\n🚀 STARTING COMPLETE RAWA-CREATOR SYSTEM")
        print("=" * 60)
        
        try:
            # Step 1: Generate browser extension icons
            if self.icon_generator:
                print("🎨 Step 1: Generating browser extension icons...")
                icons = self.icon_generator.generate_browser_extension_icons()
                print(f"✅ Generated {len(icons)} icons")
            else:
                print("⚠️  Icon generation: No module named 'icon_generator'")
            
            # Step 2: Build browser extension
            if self.extension_builder:
                print("🔨 Step 2: Building browser extension...")
                build_result = self.extension_builder.build_complete_extension()
                if build_result['status'] == 'success':
                    print("✅ Browser extension built successfully!")
                    
                    # Install extension
                    install_result = self.extension_builder.install_extension()
                    if install_result['status'] == 'success':
                        print("📥 Extension installation instructions ready!")
                else:
                    print("❌ Extension build failed")
            else:
                print("⚠️  Extension build: No module named 'auto_extension_builder'")
            
            # Step 3: Start GitHub Pages
            if self.github_pages:
                print("🌐 Step 3: Starting GitHub Pages interface...")
                if self.github_pages.start_server():
                    print("✅ GitHub Pages server started")
                    
                    # Open in browser
                    print("🖥️ Step 4: Opening GitHub Pages in browser...")
                    self.github_pages.open_in_browser()
                    print("✅ GitHub Pages opened in browser")
                else:
                    print("❌ GitHub Pages failed to start")
            else:
                print("❌ GitHub Pages failed: No module named 'github_pages.app'")
            
            # Step 4: Start continuous learning
            print("📚 Step 5: Starting continuous learning...")
            if hasattr(self.learning_system, 'start_continuous_learning'):
                self.learning_system.start_continuous_learning()
                print("✅ Continuous learning started")
            else:
                print("⚠️  Continuous learning not available in this version")
            
            # Step 5: Start file watcher
            print("👀 Step 6: Starting file watcher...")
            if hasattr(self.file_watcher, 'start_watching'):
                self.file_watcher.start_watching()
                print("✅ File watcher started")
            else:
                print("⚠️  File watcher not available")
            
            # Step 6: Scan existing files
            print("📁 Step 7: Scanning existing training data...")
            if hasattr(self.file_watcher, 'scan_existing_files'):
                scan_result = self.file_watcher.scan_existing_files()
                print(f"✅ Scanned {scan_result['processed']} files")
            else:
                print("⚠️  File scanning not available")
            
            # Step 7: Start interactive interface
            print("💬 Step 8: Starting interactive interface...")
            self._start_interactive_interface()
            
            return True
            
        except Exception as e:
            print(f"❌ System startup failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _start_interactive_interface(self):
        """Start the interactive command line interface"""
        print("\n" + "=" * 60)
        print("🤖 RAWAI-CREATOR INTERACTIVE INTERFACE")
        print("=" * 60)
        print("Commands:")
        print("  story  - Start story creation wizard")
        print("  status - Show system status")
        print("  train  - Manually trigger training data scan")
        print("  stats  - Show learning statistics")
        print("  voice  - Test voice narration system")
        print("  content - Show available content types")
        print("  exit   - Shutdown system")
        print("=" * 60)
        
        while self.is_running:
            try:
                command = input("\n🎯 Enter command: ").strip().lower()
                
                if command == 'story':
                    self._start_story_creation()
                elif command == 'status':
                    self._show_system_status()
                elif command == 'train':
                    self._manual_training_scan()
                elif command == 'stats':
                    self._show_learning_stats()
                elif command == 'voice':
                    self._test_voice_system()
                elif command == 'content':
                    self._show_content_types()
                elif command == 'exit':
                    self.shutdown()
                    break
                elif command == '':
                    continue
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested...")
                self.shutdown()
                break
            except Exception as e:
                print(f"❌ Command error: {e}")
    
    def _start_story_creation(self):
        """Start interactive story creation"""
        if self.content_generator:
            self.content_generator.start_story_creation()
        else:
            print("❌ Content generator not available")
    
    def _show_system_status(self):
        """Show current system status"""
        status = {
            'System': 'RawAI-Creator',
            'Status': 'Running' if self.is_running else 'Stopped',
            'Timestamp': datetime.now().isoformat(),
            'Memory Entries': len(self.memory_system.conversation_history) if self.memory_system else 0,
            'Learning Files': len(self.learning_system.processed_files) if self.learning_system else 0,
            'Advanced Tools': len(self.learning_system.penetration_tools) if hasattr(self.learning_system, 'penetration_tools') else 0,
            'Voice Profiles': len(self.learning_system.voice_profiles) if hasattr(self.learning_system, 'voice_profiles') else 0,
            'File Watcher': 'Active' if self.file_watcher and hasattr(self.file_watcher, 'is_watching') and self.file_watcher.is_watching else 'Inactive',
            'GitHub Pages': 'Active' if self.github_pages and hasattr(self.github_pages, 'is_running') and self.github_pages.is_running else 'Inactive'
        }
        
        print("\n📊 SYSTEM STATUS:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    def _manual_training_scan(self):
        """Manually trigger training data scan"""
        if self.file_watcher and hasattr(self.file_watcher, 'scan_existing_files'):
            print("📁 Manual training data scan started...")
            result = self.file_watcher.scan_existing_files()
            print(f"✅ Scan complete: {result['processed']} processed, {result['errors']} errors")
        else:
            print("❌ File watcher not available")
    
    def _show_learning_stats(self):
        """Show learning statistics"""
        if self.learning_system:
            if hasattr(self.learning_system, 'get_comprehensive_stats'):
                stats = self.learning_system.get_comprehensive_stats()
                print("\n📚 ADVANCED LEARNING STATISTICS:")
                for key, value in stats.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for subkey, subvalue in value.items():
                            print(f"    {subkey}: {subvalue}")
                    else:
                        print(f"  {key}: {value}")
            elif hasattr(self.learning_system, 'get_knowledge_base_stats'):
                stats = self.learning_system.get_knowledge_base_stats()
                print("\n📚 LEARNING STATISTICS:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
            else:
                print("❌ Learning statistics not available")
        else:
            print("❌ Learning system not available")
    
    def _test_voice_system(self):
        """Test the voice narration system"""
        if hasattr(self.learning_system, 'text_to_speech'):
            print("🎤 Testing voice system...")
            test_text = "Hello, this is a test of the advanced voice narration system."
            
            # Test male voice
            print("🔊 Testing male voice...")
            male_audio = self.learning_system.text_to_speech(test_text, self.learning_system.VoiceType.MALE)
            if male_audio:
                print("✅ Male voice test successful!")
            
            # Test female voice
            print("🔊 Testing female voice...")
            female_audio = self.learning_system.text_to_speech(test_text, self.learning_system.VoiceType.FEMALE)
            if female_audio:
                print("✅ Female voice test successful!")
            
            print("🎉 Voice system test complete!")
        else:
            print("❌ Voice system not available in learning system")
    
    def _show_content_types(self):
        """Show available content types"""
        if hasattr(self.learning_system, 'ContentType'):
            print("\n🎨 AVAILABLE CONTENT TYPES:")
            for content_type in self.learning_system.ContentType:
                print(f"  {content_type.value}: {content_type.name}")
        else:
            print("❌ Content types not available")
    
    def shutdown(self):
        """Shutdown the complete system"""
        print("\n🛑 SHUTTING DOWN RAWAI-CREATOR...")
        
        self.is_running = False
        
        # Stop continuous learning
        if self.learning_system and hasattr(self.learning_system, 'stop_continuous_learning'):
            self.learning_system.stop_continuous_learning()
            print("✅ Continuous learning stopped")
        
        # Stop file watcher
        if self.file_watcher and hasattr(self.file_watcher, 'stop_watching'):
            self.file_watcher.stop_watching()
            print("✅ File watcher stopped")
        
        # Save memory
        if self.memory_system:
            self.memory_system.save_memory()
            print("✅ Memory saved")
        
        print("🎉 RawAI-Creator shutdown complete!")

def main():
    """Main entry point"""
    ai_system = RawAICreator()
    
    try:
        # Start the complete system
        success = ai_system.start_complete_system()
        
        if success:
            print("\n🎊 RAWAI-CREATOR IS NOW OPERATIONAL!")
            print("💡 Use the interactive interface to create content")
            print("🎭 Advanced content generation with voice narration")
            print("🔧 Penetration testing and reconnaissance tools")
            print("🌐 Multiple content types supported")
            print("📚 Continuous learning is active")
        else:
            print("\n❌ Failed to start RawAI-Creator system")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown by user")
        ai_system.shutdown()
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        ai_system.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main()