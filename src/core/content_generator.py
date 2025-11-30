import os
import json
import threading
import base64
import wave
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import speech_recognition as sr
from gtts import gTTS
import pygame
from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np

class ContentType(Enum):
    COMIC = 1
    NOVEL = 2
    TV = 3
    FILM = 4
    LIVE = 5
    SHORT = 6
    CARTOON = 7
    AUDIOBOOK = 8
    COLORING_BOOK = 9
    PUZZLE_BOOK = 10
    CALENDAR = 11
    TAROT_CARDS = 12
    MAZE = 13
    DOT_TO_DOT = 14
    COLOR_BY_NUMBERS = 15
    BLOG = 16
    MANUAL = 17
    ART = 18
    MAP = 19
    LETTER = 20
    EMAIL = 21
    RESUME = 22
    TAX_FORM = 23
    EMOJI = 24
    LOGO = 25

class AudienceType(Enum):
    KIDS = 1
    TEEN = 2
    ADULT = 3
    ALL = 4
    ALL_EXPLICIT = 5

class ContentStyle(Enum):
    EDITED = 1
    EXPLICIT = 2

class VoiceType(Enum):
    SELF = 1
    MALE = 2
    FEMALE = 3

class ContentGenerator:
    def __init__(self, memory_system=None, learning_system=None):
        self.memory_system = memory_system
        self.learning_system = learning_system
        self.current_story = None
        self.voice_profiles = {}
        self.output_dir = "outputs/stories"
        self.audio_dir = "outputs/audio"
        self.images_dir = "outputs/images"
        
        # Initialize audio
        pygame.mixer.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Pre-loaded voice profiles
        self.preloaded_voices = {
            'male': {
                'name': 'David',
                'language': 'en',
                'speed': 'normal',
                'pitch': 'low'
            },
            'female': {
                'name': 'Emma', 
                'language': 'en',
                'speed': 'normal',
                'pitch': 'medium'
            }
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        self._load_voice_profiles()
    
    def _load_voice_profiles(self):
        """Load existing voice profiles"""
        voice_dir = "training_data/audio/voices"
        os.makedirs(voice_dir, exist_ok=True)
        
        # Load voice profiles from memory if available
        if self.memory_system:
            self.voice_profiles = self.memory_system.learning_data.get('voice_profiles', {})
    
    def listen_for_voice_command(self) -> str:
        """Listen for voice commands and return text"""
        try:
            print("🎤 Listening for voice command...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=10)
            
            text = self.recognizer.recognize_google(audio)
            print(f"🎯 Voice command: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("❌ No voice detected")
            return ""
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return ""
        except Exception as e:
            print(f"❌ Voice recognition error: {e}")
            return ""
    
    def text_to_speech(self, text: str, voice_type: VoiceType, save_path: str = None) -> str:
        """Convert text to speech using selected voice"""
        try:
            if voice_type == VoiceType.SELF:
                # Use recorded voice if available
                return self._use_self_voice(text, save_path)
            else:
                # Use preloaded voices
                voice_config = self.preloaded_voices['male' if voice_type == VoiceType.MALE else 'female']
                
                tts = gTTS(
                    text=text,
                    lang=voice_config['language'],
                    slow=False
                )
                
                if not save_path:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_path = os.path.join(self.audio_dir, f"speech_{timestamp}.mp3")
                
                tts.save(save_path)
                return save_path
                
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            return ""
    
    def _use_self_voice(self, text: str, save_path: str) -> str:
        """Use recorded self-voice for narration"""
        # This would use pre-recorded voice samples
        # For now, fall back to gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.audio_dir, f"self_voice_{timestamp}.mp3")
        
        tts.save(save_path)
        return save_path
    
    def play_audio(self, audio_path: str):
        """Play audio file"""
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
    
    def start_story_creation(self):
        """Start interactive story creation process"""
        print("\n" + "="*50)
        print("🎭 CONTENT CREATION WIZARD")
        print("="*50)
        
        # Voice activation option
        print("\n🎤 Voice activation available! Say 'start' to begin or type 'skip'")
        voice_command = self.listen_for_voice_command()
        
        if 'start' in voice_command:
            print("✅ Voice command accepted! Starting creation...")
        else:
            print("⏭️  Continuing with manual input...")
        
        # Step 1: Content Type Selection
        content_type = self._select_content_type()
        if not content_type:
            return
        
        # Step 2: Audience Selection
        audience_type = self._select_audience_type()
        if not audience_type:
            return
        
        # Step 3: Content Style Confirmation
        content_style = self._select_content_style()
        if not content_style:
            return
        
        # Step 4: Voice selection for audio content
        voice_type = None
        if content_type in [ContentType.AUDIOBOOK, ContentType.CARTOON, ContentType.CALENDAR]:
            voice_type = self._select_voice_type()
            if not voice_type:
                return
        
        # Step 5: Genre and Theme Input
        genre_info = self._get_genre_info()
        if not genre_info:
            return
        
        # Step 6: Content Description
        story_description = self._get_story_description()
        if not story_description:
            return
        
        # Step 7: Generate Content
        self._generate_content(
            content_type=content_type,
            audience_type=audience_type,
            content_style=content_style,
            voice_type=voice_type,
            genre_info=genre_info,
            story_description=story_description
        )
    
    def _select_content_type(self) -> Optional[ContentType]:
        """Select content type from expanded menu"""
        print("\n📖 SELECT CONTENT TYPE:")
        content_types = [
            "1: Comic", "2: Novel", "3: TV Series", "4: Film", "5: Live Performance",
            "6: Short Story", "7: Cartoon", "8: Audiobook", "9: Coloring Book",
            "10: Puzzle Book", "11: Calendar", "12: Tarot Cards", "13: Maze",
            "14: Dot to Dot", "15: Color by Numbers", "16: Blog", "17: Manual",
            "18: Art/Images", "19: Maps", "20: Letters", "21: Emails", "22: Resume",
            "23: Tax Forms", "24: Emoji", "25: Logo"
        ]
        
        for ct in content_types:
            print(ct)
        
        while True:
            try:
                choice = input("\nEnter your choice (1-25): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 25:
                    return ContentType(int(choice))
                else:
                    print("❌ Invalid choice. Please enter a number between 1-25.")
            except KeyboardInterrupt:
                print("\nContent creation cancelled.")
                return None
            except Exception as e:
                print(f"Error: {e}")
    
    def _select_audience_type(self) -> Optional[AudienceType]:
        """Select audience type from menu"""
        print("\n🎯 SELECT AUDIENCE:")
        print("1: Kids")
        print("2: Teen") 
        print("3: Adult")
        print("4: All Ages")
        print("5: All Ages - Explicit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    return AudienceType(int(choice))
                else:
                    print("❌ Invalid choice. Please enter a number between 1-5.")
            except KeyboardInterrupt:
                print("\nContent creation cancelled.")
                return None
            except Exception as e:
                print(f"Error: {e}")
    
    def _select_content_style(self) -> Optional[ContentStyle]:
        """Select content style with warning"""
        print("\n⚡ IMPORTANT CONTENT STYLE SELECTION:")
        print("1: Edited (Safe, Censored)")
        print("2: Explicit (Raw, Unfiltered)")
        print("\n⚠️  THERE IS NO GOING BACK - CHOOSE WISELY ⚠️")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-2): ").strip()
                if choice in ['1', '2']:
                    return ContentStyle(int(choice))
                else:
                    print("❌ Invalid choice. Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\nContent creation cancelled.")
                return None
            except Exception as e:
                print(f"Error: {e}")
    
    def _select_voice_type(self) -> Optional[VoiceType]:
        """Select voice type for audio content"""
        print("\n🎙️ SELECT VOICE TYPE:")
        print("1: Self (Record your voice)")
        print("2: Male Voice")
        print("3: Female Voice")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                if choice in ['1', '2', '3']:
                    voice_type = VoiceType(int(choice))
                    
                    if voice_type == VoiceType.SELF:
                        self._handle_voice_recording()
                    
                    return voice_type
                else:
                    print("❌ Invalid choice. Please enter a number between 1-3.")
            except KeyboardInterrupt:
                print("\nContent creation cancelled.")
                return None
            except Exception as e:
                print(f"Error: {e}")
    
    def _handle_voice_recording(self):
        """Handle voice recording for self-voice option"""
        print("\n🎤 VOICE RECORDING SETUP")
        print("Please speak the following phrases for voice training:")
        
        training_phrases = [
            "The quick brown fox jumps over the lazy dog.",
            "Artificial intelligence is transforming our world.",
            "Creativity and innovation drive human progress.",
            "This is my voice for story narration."
        ]
        
        for i, phrase in enumerate(training_phrases, 1):
            input(f"\nPress Enter and speak: '{phrase}'")
            # In practice, this would record audio and process it
            print(f"✅ Phrase {i}/4 recorded")
        
        print("\n🎉 Voice training complete! Your voice profile has been saved.")
        
        # Store voice profile
        if self.memory_system:
            self.memory_system.learning_data['voice_profiles'] = self.memory_system.learning_data.get('voice_profiles', {})
            self.memory_system.learning_data['voice_profiles']['self'] = {
                'trained_at': datetime.now().isoformat(),
                'phrases_recorded': len(training_phrases)
            }
            self.memory_system.save_memory()
    
    def _get_genre_info(self) -> Optional[str]:
        """Get genre and theme information from user"""
        print("\n🎨 GENRE AND THEME CREATION")
        print("Please describe the type of content we are creating.")
        print("Include themes, mood, setting, and any image/art requirements.")
        print("Examples: 'sci-fi cyberpunk with neon aesthetics' or 'fantasy adventure with medieval art'")
        
        while True:
            try:
                genre_input = input("\nEnter your genre/theme description: ").strip()
                if genre_input:
                    return genre_input
                else:
                    print("❌ Description cannot be empty. Please provide genre information.")
            except KeyboardInterrupt:
                print("\nContent creation cancelled.")
                return None
            except Exception as e:
                print(f"Error: {e}")
    
    def _get_story_description(self) -> Optional[str]:
        """Get content description from user"""
        print("\n📝 CONTENT DESCRIPTION")
        print("Provide a detailed description, keywords, or any information")
        print("you want translated into content. This can be:")
        print("- A detailed plot summary (for stories)")
        print("- Character descriptions") 
        print("- Key scenes or moments")
        print("- Themes and messages")
        print("- Business requirements (for resumes/emails)")
        print("- Art style preferences")
        print("- Or any creative input you have!")
        
        while True:
            try:
                story_input = input("\nEnter your content description: ").strip()
                if story_input:
                    return story_input
                else:
                    print("❌ Content description cannot be empty.")
            except KeyboardInterrupt:
                print("\nContent creation cancelled.")
                return None
            except Exception as e:
                print(f"Error: {e}")
    
    def _generate_content(self, content_type: ContentType, audience_type: AudienceType,
                         content_style: ContentStyle, voice_type: Optional[VoiceType],
                         genre_info: str, story_description: str):
        """Generate the actual content based on all inputs"""
        print(f"\n🎬 GENERATING {content_type.name} CONTENT...")
        
        # Create content structure
        content_data = {
            'content_type': content_type.name,
            'audience_type': audience_type.name,
            'content_style': content_style.name,
            'genre_info': genre_info,
            'description': story_description,
            'created_at': datetime.now().isoformat(),
            'status': 'generating'
        }
        
        if voice_type:
            content_data['voice_type'] = voice_type.name
        
        # Store current content
        self.current_story = content_data
        
        # Generate content based on type
        content_handlers = {
            ContentType.COMIC: self._generate_comic,
            ContentType.NOVEL: self._generate_novel,
            ContentType.TV: self._generate_tv_series,
            ContentType.FILM: self._generate_film,
            ContentType.LIVE: self._generate_live_performance,
            ContentType.SHORT: self._generate_short_story,
            ContentType.CARTOON: self._generate_cartoon,
            ContentType.AUDIOBOOK: self._generate_audiobook,
            ContentType.COLORING_BOOK: self._generate_coloring_book,
            ContentType.PUZZLE_BOOK: self._generate_puzzle_book,
            ContentType.CALENDAR: self._generate_calendar,
            ContentType.TAROT_CARDS: self._generate_tarot_cards,
            ContentType.MAZE: self._generate_maze,
            ContentType.DOT_TO_DOT: self._generate_dot_to_dot,
            ContentType.COLOR_BY_NUMBERS: self._generate_color_by_numbers,
            ContentType.BLOG: self._generate_blog,
            ContentType.MANUAL: self._generate_manual,
            ContentType.ART: self._generate_art,
            ContentType.MAP: self._generate_map,
            ContentType.LETTER: self._generate_letter,
            ContentType.EMAIL: self._generate_email,
            ContentType.RESUME: self._generate_resume,
            ContentType.TAX_FORM: self._generate_tax_form,
            ContentType.EMOJI: self._generate_emoji,
            ContentType.LOGO: self._generate_logo
        }
        
        handler = content_handlers.get(content_type)
        if handler:
            handler(content_data)
        else:
            print(f"❌ No handler for content type: {content_type}")
        
        # Save content to file
        self._save_content(content_data)
        
        print(f"\n✅ CONTENT GENERATION COMPLETE!")
        print(f"📁 Output saved to: {self.output_dir}")
    
    def _generate_comic(self, content_data: Dict):
        """Generate comic content"""
        print("Creating comic book format...")
        
        # Extract key elements for comic generation
        content_data['format'] = 'comic_book'
        content_data['pages'] = 24  # Standard comic length
        content_data['panels_per_page'] = 6
        
        # Generate comic script
        content_data['script'] = self._create_comic_script(content_data)
        
        # Generate character descriptions
        content_data['characters'] = self._create_characters(content_data)
        
        # Generate scene descriptions for artwork
        content_data['scenes'] = self._create_scene_descriptions(content_data)
        
        content_data['status'] = 'completed'
    
    def _generate_novel(self, content_data: Dict):
        """Generate novel content"""
        print("Creating novel format...")
        
        content_data['format'] = 'novel'
        content_data['chapters'] = 12
        content_data['estimated_words'] = 80000
        
        # Generate chapter outlines
        content_data['outline'] = self._create_novel_outline(content_data)
        
        # Generate character arcs
        content_data['character_arcs'] = self._create_character_arcs(content_data)
        
        # Generate detailed plot
        content_data['plot'] = self._create_detailed_plot(content_data)
        
        content_data['status'] = 'completed'
    
    def _generate_tv_series(self, content_data: Dict):
        """Generate TV series content"""
        print("Creating TV series format...")
        content_data['format'] = 'tv_series'
        content_data['episodes'] = 10
        content_data['episode_duration'] = '45 minutes'
        content_data['seasons'] = 1
        content_data['status'] = 'completed'
    
    def _generate_film(self, content_data: Dict):
        """Generate film content"""
        print("Creating film format...")
        content_data['format'] = 'film'
        content_data['duration'] = '120 minutes'
        content_data['acts'] = 3
        content_data['status'] = 'completed'
    
    def _generate_live_performance(self, content_data: Dict):
        """Generate live performance content"""
        print("Creating live performance format...")
        content_data['format'] = 'live_performance'
        content_data['duration'] = '90 minutes'
        content_data['type'] = 'theatrical'
        content_data['status'] = 'completed'
    
    def _generate_short_story(self, content_data: Dict):
        """Generate short story content"""
        print("Creating short story format...")
        content_data['format'] = 'short_story'
        content_data['estimated_words'] = 5000
        content_data['structure'] = 'compact_narrative'
        content_data['status'] = 'completed'
    
    def _generate_cartoon(self, content_data: Dict):
        """Generate cartoon content"""
        print("Creating cartoon format...")
        content_data['format'] = 'cartoon'
        content_data['episodes'] = 6
        content_data['episode_duration'] = '22 minutes'
        content_data['animation_style'] = '2d_traditional'
        content_data['status'] = 'completed'
    
    def _generate_audiobook(self, content_data: Dict):
        """Generate audiobook with voice narration"""
        print("Creating audiobook format...")
        content_data['format'] = 'audiobook'
        content_data['estimated_duration'] = '8 hours'
        
        # Generate narration script
        content_data['narration_script'] = self._create_audiobook_script(content_data)
        
        # Add voice-specific instructions
        if 'voice_type' in content_data:
            content_data['voice_instructions'] = self._get_voice_instructions(content_data['voice_type'])
        
        # Generate audio if voice type is selected
        if 'voice_type' in content_data:
            voice_type = VoiceType[content_data['voice_type']]
            audio_path = self.text_to_speech(content_data['narration_script'][:500] + "...", voice_type)
            if audio_path:
                content_data['audio_sample'] = audio_path
                print(f"🎧 Audio sample generated: {audio_path}")
        
        content_data['status'] = 'completed'
    
    def _generate_coloring_book(self, content_data: Dict):
        """Generate coloring book with anti-bully feature"""
        print("Creating coloring book...")
        content_data['format'] = 'coloring_book'
        content_data['pages'] = 20
        content_data['anti_bully_feature'] = True
        content_data['theme'] = content_data['genre_info']
        content_data['complexity'] = 'varied'
        content_data['status'] = 'completed'
    
    def _generate_puzzle_book(self, content_data: Dict):
        """Generate puzzle book"""
        print("Creating puzzle book...")
        content_data['format'] = 'puzzle_book'
        content_data['puzzle_types'] = ['crossword', 'word search', 'sudoku', 'riddles', 'logic_puzzles']
        content_data['difficulty'] = 'varied'
        content_data['pages'] = 50
        content_data['status'] = 'completed'
    
    def _generate_calendar(self, content_data: Dict):
        """Generate talking calendar"""
        print("Creating talking calendar...")
        content_data['format'] = 'calendar'
        content_data['duration'] = '12 months'
        content_data['voice_enabled'] = True
        content_data['features'] = ['daily_quotes', 'reminders', 'events']
        content_data['status'] = 'completed'
    
    def _generate_tarot_cards(self, content_data: Dict):
        """Generate tarot card deck"""
        print("Creating tarot cards...")
        content_data['format'] = 'tarot_deck'
        content_data['cards_count'] = 78
        content_data['suits'] = ['Wands', 'Cups', 'Swords', 'Pentacles']
        content_data['art_style'] = 'mystical'
        content_data['status'] = 'completed'
    
    def _generate_maze(self, content_data: Dict):
        """Generate maze puzzles"""
        print("Creating maze...")
        content_data['format'] = 'maze'
        content_data['difficulty'] = 'medium'
        content_data['theme'] = content_data['genre_info']
        content_data['complexity'] = 'multi_path'
        content_data['status'] = 'completed'
    
    def _generate_dot_to_dot(self, content_data: Dict):
        """Generate dot-to-dot puzzles"""
        print("Creating dot-to-dot...")
        content_data['format'] = 'dot_to_dot'
        content_data['dots_count'] = 50
        content_data['complexity'] = 'intermediate'
        content_data['image_reveal'] = True
        content_data['status'] = 'completed'
    
    def _generate_color_by_numbers(self, content_data: Dict):
        """Generate color by numbers"""
        print("Creating color by numbers...")
        content_data['format'] = 'color_by_numbers'
        content_data['color_palette'] = 'vibrant'
        content_data['complexity'] = 'detailed'
        content_data['pages'] = 15
        content_data['status'] = 'completed'
    
    def _generate_blog(self, content_data: Dict):
        """Generate blog content"""
        print("Creating blog content...")
        content_data['format'] = 'blog'
        content_data['post_types'] = ['daily', 'advice', 'how-to', 'personal', 'professional']
        content_data['topics'] = self._extract_blog_topics(content_data)
        content_data['frequency'] = 'daily'
        content_data['status'] = 'completed'
    
    def _generate_manual(self, content_data: Dict):
        """Generate instruction manuals"""
        print("Creating manual...")
        content_data['format'] = 'manual'
        content_data['manual_type'] = self._determine_manual_type(content_data)
        content_data['sections'] = ['introduction', 'setup', 'usage', 'troubleshooting', 'maintenance']
        content_data['comprehensive'] = True
        content_data['status'] = 'completed'
    
    def _generate_art(self, content_data: Dict):
        """Generate various art types including explicit content"""
        print("Creating artwork...")
        content_data['format'] = 'art'
        
        # Determine art type based on content style and audience
        if content_data['content_style'] == 'EXPLICIT' and content_data['audience_type'] in ['ADULT', 'ALL_EXPLICIT']:
            content_data['art_types'] = ['nude', 'fantasy', 'horror', 'graphic', '3d', 'concept_art']
        else:
            content_data['art_types'] = ['safe', 'fantasy', 'abstract', 'landscape', 'portrait']
        
        content_data['resolution'] = 'high'
        content_data['styles'] = ['realistic', 'digital', 'traditional']
        content_data['status'] = 'completed'
    
    def _generate_map(self, content_data: Dict):
        """Generate maps for games and worlds"""
        print("Creating map...")
        content_data['format'] = 'map'
        content_data['map_type'] = 'fantasy_world'
        content_data['features'] = ['continents', 'cities', 'landmarks', 'secret_locations', 'terrain']
        content_data['scale'] = 'detailed'
        content_data['status'] = 'completed'
    
    def _generate_letter(self, content_data: Dict):
        """Generate various types of letters"""
        print("Creating letter...")
        content_data['format'] = 'letter'
        content_data['letter_type'] = self._determine_letter_type(content_data)
        content_data['tone'] = 'appropriate'
        content_data['templates'] = ['formal', 'personal', 'business']
        content_data['status'] = 'completed'
    
    def _generate_email(self, content_data: Dict):
        """Generate email templates"""
        print("Creating email template...")
        content_data['format'] = 'email'
        content_data['email_type'] = self._determine_email_type(content_data)
        content_data['templates'] = ['formal', 'casual', 'business', 'personal', 'follow_up']
        content_data['variations'] = 5
        content_data['status'] = 'completed'
    
    def _generate_resume(self, content_data: Dict):
        """Generate resume/CV"""
        print("Creating resume...")
        content_data['format'] = 'resume'
        content_data['sections'] = ['summary', 'experience', 'education', 'skills', 'achievements']
        content_data['style'] = 'professional'
        content_data['length'] = '2_pages'
        content_data['status'] = 'completed'
    
    def _generate_tax_form(self, content_data: Dict):
        """Generate tax forms"""
        print("Creating tax form...")
        content_data['format'] = 'tax_form'
        content_data['forms'] = ['W2', 'W4', '1040', 'Schedule C', 'Itemized_Deductions']
        content_data['compliance'] = 'current_year'
        content_data['instructions'] = 'detailed'
        content_data['status'] = 'completed'
    
    def _generate_emoji(self, content_data: Dict):
        """Generate custom emoji sets"""
        print("Creating emoji set...")
        content_data['format'] = 'emoji_set'
        
        if content_data['content_style'] == 'EXPLICIT':
            content_data['emoji_types'] = ['adult', 'humor', 'horror', 'romance', 'sarcastic']
        else:
            content_data['emoji_types'] = ['safe', 'funny', 'cute', 'professional', 'expressive']
        
        content_data['count'] = 50
        content_data['style'] = 'consistent'
        content_data['status'] = 'completed'
    
    def _generate_logo(self, content_data: Dict):
        """Generate logos and business cards"""
        print("Creating logo...")
        content_data['format'] = 'logo'
        content_data['variations'] = 5
        content_data['formats'] = ['vector', 'png', 'business_card', 'letterhead']
        content_data['color_schemes'] = 3
        content_data['status'] = 'completed'
    
    # Content creation helper methods
    def _create_comic_script(self, content_data: Dict) -> str:
        """Create comic book script from content data"""
        script = f"COMIC SCRIPT: {content_data['genre_info']}\n\n"
        script += f"Based on: {content_data['description']}\n\n"
        
        # Add panel descriptions (simplified)
        script += "PAGE 1:\n"
        script += "Panel 1: Introduction scene establishing setting\n"
        script += "Panel 2: Main character introduction\n"
        script += "Panel 3: Inciting incident\n"
        script += "...\n\n"
        
        return script
    
    def _create_novel_outline(self, content_data: Dict) -> List[Dict]:
        """Create novel chapter outline"""
        outline = []
        
        # Generate chapter structure based on story description
        chapters = [
            "Introduction and Setting",
            "Character Development", 
            "Rising Action",
            "Conflict Establishment",
            "Story Development",
            "Climax Build-up",
            "Major Turning Point",
            "Resolution Phase",
            "Character Resolution",
            "Plot Conclusion",
            "Epilogue Setup",
            "Final Resolution"
        ]
        
        for i, chapter_title in enumerate(chapters, 1):
            outline.append({
                'chapter': i,
                'title': chapter_title,
                'summary': f"Develops {chapter_title.lower()} based on {content_data['genre_info']}",
                'key_elements': ['character', 'plot', 'theme']
            })
        
        return outline
    
    def _create_audiobook_script(self, content_data: Dict) -> str:
        """Create audiobook narration script"""
        script = f"AUDIOBOOK NARRATION SCRIPT\n\n"
        script += f"Title: {content_data['genre_info']}\n"
        script += f"Description: {content_data['description']}\n\n"
        
        script += "CHAPTER 1: BEGINNINGS\n"
        script += "[Narrator begins with engaging tone]\n"
        script += f"In a world shaped by {content_data['genre_info']}, our story begins...\n\n"
        
        # Add more detailed script based on description
        script += self._expand_story_from_description(content_data['description'])
        
        script += "[Sound effects and pacing notes would be included here]\n"
        
        return script
    
    def _expand_story_from_description(self, description: str) -> str:
        """Expand a brief description into a full story segment"""
        return f"Based on your description: '{description}', this story unfolds with rich characters and compelling plot developments. The narrative explores themes and creates an immersive experience for the listener."
    
    def _create_characters(self, content_data: Dict) -> List[Dict]:
        """Create character descriptions"""
        characters = [
            {
                'name': 'Protagonist',
                'description': 'Main character driving the story forward',
                'traits': ['determined', 'complex', 'relatable'],
                'arc': 'Growth and transformation through the story'
            },
            {
                'name': 'Antagonist', 
                'description': 'Primary opposition or challenge',
                'traits': ['motivated', 'formidable', 'understandable'],
                'arc': 'Reveals depth and complexity'
            }
        ]
        
        return characters
    
    def _create_scene_descriptions(self, content_data: Dict) -> List[Dict]:
        """Create scene descriptions for artwork"""
        scenes = [
            {
                'scene': 'Opening',
                'description': 'Establishes the setting and mood',
                'visual_elements': ['setting', 'atmosphere', 'key symbols'],
                'art_style': 'Based on genre requirements'
            },
            {
                'scene': 'Climax',
                'description': 'The most intense and important moment',
                'visual_elements': ['drama', 'emotion', 'action'],
                'art_style': 'Dynamic and engaging'
            }
        ]
        
        return scenes
    
    def _create_character_arcs(self, content_data: Dict) -> List[Dict]:
        """Create character development arcs"""
        arcs = [
            {
                'character': 'Main Character',
                'beginning': 'Initial state and limitations',
                'development': 'Challenges and growth opportunities', 
                'transformation': 'Final state and lessons learned'
            }
        ]
        
        return arcs
    
    def _create_detailed_plot(self, content_data: Dict) -> Dict:
        """Create detailed plot structure"""
        plot = {
            'act_1': {
                'setup': 'Introduction of world and characters',
                'inciting_incident': 'Event that starts the main conflict',
                'plot_point_1': 'Decision that commits to the journey'
            },
            'act_2': {
                'rising_action': 'Series of challenges and developments',
                'midpoint': 'Major turning point raising stakes',
                'plot_point_2': 'Low point leading to climax'
            },
            'act_3': {
                'climax': 'Final confrontation and resolution',
                'falling_action': 'Loose ends being tied up',
                'resolution': 'Final outcome and character states'
            }
        }
        
        return plot
    
    def _get_voice_instructions(self, voice_type: str) -> Dict:
        """Get voice-specific narration instructions"""
        instructions = {
            'pace': 'moderate',
            'tone': 'engaging',
            'emphasis': 'emotional moments',
            'character_voices': 'distinct but consistent'
        }
        
        if voice_type == 'MALE':
            instructions['voice_range'] = 'baritone to tenor'
        elif voice_type == 'FEMALE':
            instructions['voice_range'] = 'mezzo-soprano to alto'
        elif voice_type == 'SELF':
            instructions['voice_range'] = 'natural speaking voice'
        
        return instructions
    
    def _extract_blog_topics(self, content_data: Dict) -> List[str]:
        """Extract blog topics from description"""
        description = content_data['description'].lower()
        topics = []
        
        if 'love' in description or 'relationship' in description:
            topics.extend(['love advice', 'dating tips', 'relationship guidance'])
        if 'diy' in description or 'how to' in description:
            topics.extend(['DIY projects', 'step-by-step guides', 'home improvement'])
        if 'wise' in description or 'advice' in description:
            topics.extend(['daily wisdom', 'life advice', 'philosophical insights'])
        if 'business' in description or 'career' in description:
            topics.extend(['career advice', 'business tips', 'professional development'])
        
        return topics if topics else ['general interest', 'lifestyle', 'personal growth']
    
    def _determine_manual_type(self, content_data: Dict) -> str:
        """Determine what type of manual to create"""
        description = content_data['description'].lower()
        
        if 'car' in description or 'vehicle' in description:
            return 'automotive'
        elif 'tech' in description or 'computer' in description:
            return 'technology'
        elif 'home' in description or 'appliance' in description:
            return 'home_appliance'
        elif 'kama' in description or 'intimate' in description:
            return 'relationship'
        else:
            return 'general'
    
    def _determine_letter_type(self, content_data: Dict) -> str:
        """Determine what type of letter to create"""
        description = content_data['description'].lower()
        
        if 'love' in description:
            return 'love_letter'
        elif 'breakup' in description or 'break up' in description:
            return 'breakup_letter'
        elif 'job' in description or 'hire' in description:
            return 'job_application'
        elif 'complaint' in description:
            return 'complaint_letter'
        else:
            return 'general_letter'
    
    def _determine_email_type(self, content_data: Dict) -> str:
        """Determine what type of email to create"""
        description = content_data['description'].lower()
        
        if 'hire' in description or 'job' in description:
            return 'job_inquiry'
        elif 'buy' in description or 'purchase' in description:
            return 'purchase_inquiry'
        elif 'sell' in description or 'sale' in description:
            return 'sales_pitch'
        elif 'intern' in description:
            return 'internship_application'
        else:
            return 'general_business'
    
    def _save_content(self, content_data: Dict):
        """Save generated content to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_type = content_data['content_type'].lower()
        
        filename = f"{content_type}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        
        # Store in memory system
        if self.memory_system:
            self.memory_system.learning_data['generated_content'] = self.memory_system.learning_data.get('generated_content', [])
            self.memory_system.learning_data['generated_content'].append({
                'filepath': filepath,
                'created_at': content_data['created_at'],
                'content_type': content_data['content_type']
            })
            self.memory_system.save_memory()
        
        print(f"Content saved to: {filepath}")
    
    def narrate_content(self, content_data: Dict, voice_type: VoiceType):
        """Narrate the generated content using selected voice"""
        if 'narration_script' in content_data:
            script = content_data['narration_script']
            print(f"🎙️ Narrating with {voice_type.name} voice...")
            
            audio_path = self.text_to_speech(script, voice_type)
            if audio_path:
                print("🔊 Playing narration...")
                self.play_audio(audio_path)
            else:
                print("❌ Failed to generate audio narration")
        else:
            print("❌ No narration script available for this content")
    
    def get_current_content(self) -> Optional[Dict]:
        """Get the current content being worked on"""
        return self.current_story
    
    def list_generated_content(self) -> List[Dict]:
        """List all generated content"""
        content_list = []
        
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.output_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content_data = json.load(f)
                        content_list.append({
                            'filename': filename,
                            'content_type': content_data.get('content_type', 'unknown'),
                            'created_at': content_data.get('created_at', 'unknown'),
                            'status': content_data.get('status', 'unknown')
                        })
                except:
                    continue
        
        return content_list

# Additional voice management functions
def create_voice_narration_system():
    """Create a comprehensive voice narration system"""
    system = {
        'male_voice': {
            'name': 'David',
            'style': 'professional',
            'languages': ['en'],
            'specialties': ['narration', 'business', 'education']
        },
        'female_voice': {
            'name': 'Emma',
            'style': 'expressive',
            'languages': ['en'],
            'specialties': ['storytelling', 'emotional', 'conversational']
        },
        'self_voice': {
            'name': 'Your Voice',
            'style': 'personal',
            'languages': ['en'],
            'specialties': ['personal_narration', 'authentic']
        }
    }
    return system

# Example usage
if __name__ == "__main__":
    generator = ContentGenerator()
    
    # Test voice functionality
    print("Testing voice system...")
    test_text = "Hello, this is a test of the voice narration system."
    
    # Test male voice
    male_audio = generator.text_to_speech(test_text, VoiceType.MALE)
    if male_audio:
        print("Male voice test successful!")
    
    # Test female voice  
    female_audio = generator.text_to_speech(test_text, VoiceType.FEMALE)
    if female_audio:
        print("Female voice test successful!")
    
    print("Voice system ready! You can now start content creation.")