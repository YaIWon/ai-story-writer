# github_pages/app.py

import os
import json
import threading
from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime

app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

class GitHubPagesApp:
    def __init__(self, memory_system=None, learning_system=None, content_generator=None):
        self.memory_system = memory_system
        self.learning_system = learning_system
        self.content_generator = content_generator
        self.conversation_history = []
        self.is_running = False
        
    def start_server(self, host='0.0.0.0', port=5000):
        """Start the GitHub Pages Flask server"""
        print(f"🌐 Starting GitHub Pages interface on port {port}...")
        
        try:
            # Set up routes
            self._setup_routes()
            
            # Start in background thread
            server_thread = threading.Thread(
                target=lambda: app.run(
                    host=host, 
                    port=port, 
                    debug=False, 
                    use_reloader=False
                )
            )
            server_thread.daemon = True
            server_thread.start()
            
            self.is_running = True
            print(f"✅ GitHub Pages server started at http://{host}:{port}")
            return True
            
        except Exception as e:
            print(f"❌ GitHub Pages failed: {e}")
            return False

    def _setup_routes(self):
        """Set up all Flask routes"""
        
        @app.route('/')
        def index():
            """Main interface page"""
            return render_template('index.html')
        
        @app.route('/api/status')
        def api_status():
            """API status endpoint"""
            return jsonify({
                'status': 'running',
                'service': 'RawAI GitHub Pages',
                'timestamp': datetime.now().isoformat(),
                'memory_entries': len(self.memory_system.conversation_history) if self.memory_system else 0,
                'learning_files': len(self.learning_system.knowledge_base) if self.learning_system else 0
            })
        
        @app.route('/api/sync', methods=['POST'])
        def api_sync():
            """Sync data from browser extension"""
            try:
                data = request.get_json()
                print(f"📥 Received sync data: {data.get('type', 'unknown')}")
                
                if self.memory_system:
                    self.memory_system.store_interaction(
                        user_input=f"Extension sync: {data.get('type', 'unknown')}",
                        ai_response="Data received and processed",
                        metadata=data
                    )
                
                return jsonify({'status': 'success', 'message': 'Data synced'})
                
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @app.route('/api/generate', methods=['POST'])
        def api_generate():
            """Generate content via API"""
            try:
                data = request.get_json()
                prompt = data.get('prompt', '')
                content_type = data.get('type', 'text')
                
                print(f"🎨 Generation request: {content_type}")
                
                # Store in memory
                if self.memory_system:
                    self.memory_system.store_interaction(
                        user_input=f"API generation: {prompt}",
                        ai_response=f"Generating {content_type} content",
                        metadata=data
                    )
                
                # Generate content based on type
                if content_type == 'story':
                    result = self._generate_story_content(prompt, data)
                elif content_type == 'code':
                    result = self._generate_code_content(prompt, data)
                else:
                    result = self._generate_text_content(prompt, data)
                
                return jsonify({'status': 'success', 'result': result})
                
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @app.route('/api/analyze', methods=['POST'])
        def api_analyze():
            """Analyze content via API"""
            try:
                data = request.get_json()
                content = data.get('content', '')
                analysis_type = data.get('analysis_type', 'general')
                
                print(f"🔍 Analysis request: {analysis_type}")
                
                analysis_result = self._analyze_content(content, analysis_type)
                
                return jsonify({'status': 'success', 'analysis': analysis_result})
                
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @app.route('/api/training/data', methods=['GET'])
        def api_training_data():
            """Get training data statistics"""
            try:
                if self.learning_system:
                    stats = self.learning_system.get_knowledge_base_stats()
                    return jsonify({'status': 'success', 'stats': stats})
                else:
                    return jsonify({'status': 'error', 'message': 'Learning system not available'})
                    
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @app.route('/api/conversation/history', methods=['GET'])
        def api_conversation_history():
            """Get conversation history"""
            try:
                if self.memory_system:
                    history = self.memory_system.get_conversation_context(50)
                    return jsonify({'status': 'success', 'history': history})
                else:
                    return jsonify({'status': 'error', 'message': 'Memory system not available'})
                    
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @app.route('/api/extension/status', methods=['GET'])
        def api_extension_status():
            """Get browser extension status"""
            return jsonify({
                'status': 'connected',
                'extension': 'RawAI Creator',
                'version': '1.0.0',
                'timestamp': datetime.now().isoformat()
            })
        
        # Static file serving
        @app.route('/static/<path:filename>')
        def static_files(filename):
            return send_from_directory(app.static_folder, filename)

    def _generate_story_content(self, prompt: str, data: dict) -> dict:
        """Generate story content"""
        story_data = {
            'genre_info': data.get('genre', 'fantasy'),
            'story_description': prompt,
            'content_type': 'NOVEL',
            'audience_type': data.get('audience', 'ALL'),
            'content_style': data.get('style', 'EDITED')
        }
        
        if self.content_generator:
            result = self.content_generator.generate_novel_content(story_data)
            return {
                'type': 'story',
                'content': result,
                'word_count': result['metadata']['word_count'],
                'chapter_count': result['metadata']['chapter_count']
            }
        else:
            return {
                'type': 'story',
                'content': f"Story based on: {prompt}",
                'word_count': len(prompt.split()),
                'chapter_count': 1,
                'note': 'Content generator not available - placeholder content'
            }

    def _generate_code_content(self, prompt: str, data: dict) -> dict:
        """Generate code content"""
        return {
            'type': 'code',
            'language': data.get('language', 'python'),
            'content': f"# Code generated from: {prompt}\n\ndef generated_function():\n    \"\"\"Auto-generated code\"\"\"\n    return \"Implementation based on: {prompt}\"",
            'lines': 5,
            'complexity': 'medium'
        }

    def _generate_text_content(self, prompt: str, data: dict) -> dict:
        """Generate general text content"""
        return {
            'type': 'text',
            'content': f"Generated content based on your request: {prompt}\n\nThis is AI-generated content created by the RawAI system.",
            'word_count': len(prompt.split()) + 10,
            'tone': data.get('tone', 'professional')
        }

    def _analyze_content(self, content: str, analysis_type: str) -> dict:
        """Analyze content"""
        word_count = len(content.split())
        char_count = len(content)
        
        analysis = {
            'word_count': word_count,
            'character_count': char_count,
            'analysis_type': analysis_type,
            'timestamp': datetime.now().isoformat()
        }
        
        if analysis_type == 'sentiment':
            analysis['sentiment'] = 'neutral'
            analysis['confidence'] = 0.8
            
        elif analysis_type == 'complexity':
            analysis['readability'] = 'medium'
            analysis['grade_level'] = 'high_school'
            
        elif analysis_type == 'topics':
            analysis['topics'] = ['ai', 'content', 'generation']
            analysis['key_phrases'] = content.split()[:5]
            
        return analysis

    def open_in_browser(self, port=5000):
        """Open GitHub Pages in browser"""
        import webbrowser
        url = f"http://localhost:{port}"
        print(f"🔗 Opening GitHub Pages: {url}")
        webbrowser.open(url)

# Global instance
github_pages_app = GitHubPagesApp()

if __name__ == '__main__':
    # For direct execution
    github_pages_app.start_server()
    github_pages_app.open_in_browser()
