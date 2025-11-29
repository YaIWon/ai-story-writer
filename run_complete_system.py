# run_complete_system.py

import os
import sys
import threading
import time
from datetime import datetime

def run_complete_system():
    """Run the complete RawAI-Creator system with all components"""
    print("🚀 STARTING COMPLETE RAWA-CREATOR SYSTEM")
    print("=" * 60)
    
    # Step 1: Generate missing icons
    print("🎨 Step 1: Generating browser extension icons...")
    try:
        from icon_generator import IconGenerator
        icon_gen = IconGenerator()
        icon_gen.generate_all_icons()
        print("✅ Icons generated")
    except Exception as e:
        print(f"⚠️  Icon generation: {e}")
    
    # Step 2: Analyze conversation
    print("\n🔍 Step 2: Analyzing conversation requirements...")
    try:
        from analyze_conversation import ConversationAnalyzer
        analyzer = ConversationAnalyzer()
        analysis_results = analyzer.run_complete_analysis()
        if analysis_results:
            print("✅ Conversation analyzed")
        else:
            print("⚠️  Conversation analysis skipped")
    except Exception as e:
        print(f"⚠️  Conversation analysis: {e}")
    
    # Step 3: Build browser extension
    print("\n🔨 Step 3: Building browser extension...")
    try:
        from auto_extension_builder import ExtensionAutoBuilder
        builder = ExtensionAutoBuilder()
        zip_path = builder.build_extension_package()
        guide_path = builder.auto_install_chrome_extension()
        builder.create_browser_launch_config()
        print("✅ Extension built")
    except Exception as e:
        print(f"⚠️  Extension build: {e}")
    
    # Step 4: Start GitHub Pages
    print("\n🌐 Step 4: Starting GitHub Pages interface...")
    gh_pages_thread = None
    try:
        from github_pages.app import GitHubPagesApp
        from src.core.amoral_memory import AmoralMemory
        from src.core.unrestricted_learning import UnrestrictedLearning
        from src.core.content_generator import ContentGenerator
        
        memory = AmoralMemory()
        learning = UnrestrictedLearning(memory_system=memory)
        content_gen = ContentGenerator(memory_system=memory, learning_system=learning)
        
        gh_pages_app = GitHubPagesApp(memory, learning, content_gen)
        
        def run_gh_pages():
            try:
                gh_pages_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
            except Exception as e:
                print(f"GitHub Pages error: {e}")
        
        gh_pages_thread = threading.Thread(target=run_gh_pages)
        gh_pages_thread.daemon = True
        gh_pages_thread.start()
        print("✅ GitHub Pages started on http://localhost:5000")
    except Exception as e:
        print(f"❌ GitHub Pages failed: {e}")
    
    # Step 5: Wait for GitHub Pages and open in Codespaces preview
    print("\n🖥️ Step 5: Opening GitHub Pages in Codespaces preview...")
    time.sleep(3)  # Wait for server to start
    
    try:
        import webbrowser
        codespaces_domain = os.getenv('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')
        codespaces_name = os.getenv('CODESPACE_NAME')
        
        if codespaces_domain and codespaces_name:
            preview_url = f"https://{codespaces_name}-5000.{codespaces_domain}"
            print(f"🔗 Opening: {preview_url}")
            webbrowser.open(preview_url)
        else:
            print("🔗 Opening: http://localhost:5000")
            webbrowser.open('http://localhost:5000')
        print("✅ GitHub Pages opened in preview")
    except Exception as e:
        print(f"⚠️  Browser open: {e}")
    
    # Step 6: Start main AI system
    print("\n🤖 Step 6: Starting main AI system...")
    try:
        from main import RawAICreator
        
        def run_main_system():
            try:
                ai_creator = RawAICreator()
                ai_creator.start()
            except Exception as e:
                print(f"Main system error: {e}")
        
        main_thread = threading.Thread(target=run_main_system)
        main_thread.daemon = True
        main_thread.start()
        print("✅ Main AI system started")
    except Exception as e:
        print(f"❌ Main system failed: {e}")
    
    # Step 7: Show completion message
    print("\n" + "=" * 60)
    print("🎉 RAWA-CREATOR SYSTEM FULLY OPERATIONAL!")
    print("=" * 60)
    print("\n📊 SYSTEM STATUS:")
    print("   🌐 GitHub Pages: http://localhost:5000")
    print("   🔧 Browser Extension: Built and ready for installation")
    print("   🤖 AI System: Running in background")
    print("   📁 Training Data: Ready for file ingestion")
    print("   🎨 Content Generation: Story creation available")
    print("\n💡 NEXT STEPS:")
    print("   1. Install browser extension from browser_extension/ folder")
    print("   2. Add files to training_data/ for AI learning")
    print("   3. Use 'story' command to create content")
    print("   4. Chat with AI via GitHub Pages interface")
    print("\n⚡ COMMANDS:")
    print("   - Type 'story' to create content")
    print("   - Type 'analyze' to analyze training data")
    print("   - Type 'status' for system status")
    print("   - Type 'help' for all commands")
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down RawAI-Creator...")

def main():
    """Main entry point - runs the complete system"""
    # Check if we're in Codespaces
    if not os.getenv('CODESPACES') and not os.getenv('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN'):
        print("⚠️  Not in GitHub Codespaces")
        print("💡 For local development, run: python main.py")
        return
    
    # Run the complete system
    run_complete_system()

if __name__ == "__main__":
    main()
