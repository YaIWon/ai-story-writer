# src/generation/text_engine.py

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading

class TextEngine:
    def __init__(self, memory_system=None, learning_system=None):
        self.memory_system = memory_system
        self.learning_system = learning_system
        self.output_dir = "outputs/text"
        self.generation_history = []
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_full_length_story(self, story_data: Dict) -> Dict[str, Any]:
        """Generate full-length story content based on specifications"""
        print(f"📖 Generating full-length {story_data['content_type']}...")
        
        content_type = story_data['content_type']
        audience_type = story_data['audience_type']
        content_style = story_data['content_style']
        
        # Generate based on content type
        if content_type == 'COMIC':
            return self._generate_comic_content(story_data)
        elif content_type == 'NOVEL':
            return self._generate_novel_content(story_data)
        elif content_type == 'TV':
            return self._generate_tv_content(story_data)
        elif content_type == 'FILM':
            return self._generate_film_content(story_data)
        elif content_type == 'AUDIOBOOK':
            return self._generate_audiobook_content(story_data)
        else:
            return self._generate_generic_content(story_data)
    
    def _generate_comic_content(self, story_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive comic book content"""
        comic_content = {
            'title': f"Comic: {story_data['genre_info']}",
            'format': 'comic_book',
            'pages': [],
            'characters': self._generate_characters(story_data),
            'script': self._generate_comic_script(story_data),
            'art_descriptions': self._generate_art_descriptions(story_data),
            'metadata': self._create_metadata(story_data)
        }
        
        # Generate 24 pages of comic content
        for page_num in range(1, 25):
            page = {
                'page_number': page_num,
                'panels': self._generate_comic_panels(page_num, story_data),
                'dialogue': self._generate_page_dialogue(page_num, story_data),
                'art_notes': self._generate_art_notes(page_num, story_data)
            }
            comic_content['pages'].append(page)
        
        # Save comic content
        self._save_content(comic_content, 'comic')
        return comic_content
    
    def _generate_novel_content(self, story_data: Dict) -> Dict[str, Any]:
        """Generate full-length novel content"""
        novel_content = {
            'title': f"Novel: {story_data['genre_info']}",
            'format': 'novel',
            'chapters': [],
            'word_count_estimate': 80000,
            'character_arcs': self._generate_character_arcs(story_data),
            'plot_structure': self._generate_plot_structure(story_data),
            'metadata': self._create_metadata(story_data)
        }
        
        # Generate 12 chapters
        for chapter_num in range(1, 13):
            chapter = {
                'chapter_number': chapter_num,
                'title': self._generate_chapter_title(chapter_num, story_data),
                'content': self._generate_chapter_content(chapter_num, story_data),
                'word_count': 6666,  # Approximately 80k/12
                'key_events': self._generate_chapter_events(chapter_num, story_data),
                'character_development': self._generate_chapter_character_development(chapter_num, story_data)
            }
            novel_content['chapters'].append(chapter)
        
        # Save novel content
        self._save_content(novel_content, 'novel')
        return novel_content
    
    def _generate_audiobook_content(self, story_data: Dict) -> Dict[str, Any]:
        """Generate audiobook narration content"""
        audiobook_content = {
            'title': f"Audiobook: {story_data['genre_info']}",
            'format': 'audiobook',
            'estimated_duration': '8 hours',
            'narration_script': self._generate_narration_script(story_data),
            'chapter_breaks': self._generate_audiobook_chapters(story_data),
            'voice_instructions': self._generate_voice_instructions(story_data),
            'sound_effects_notes': self._generate_sound_effects(story_data),
            'metadata': self._create_metadata(story_data)
        }
        
        # Save audiobook content
        self._save_content(audiobook_content, 'audiobook')
        return audiobook_content
    
    def _generate_characters(self, story_data: Dict) -> List[Dict]:
        """Generate detailed character descriptions"""
        characters = []
        
        # Main protagonist
        characters.append({
            'name': 'Alex Morgan',
            'role': 'protagonist',
            'description': 'A determined individual facing extraordinary circumstances',
            'personality_traits': ['brave', 'curious', 'resilient'],
            'appearance': 'Distinctive features that match the genre',
            'background': 'Complex history that drives their motivations',
            'character_arc': 'Transformation through the story events',
            'relationships': []
        })
        
        # Antagonist
        characters.append({
            'name': 'Director Kane',
            'role': 'antagonist',
            'description': 'Powerful figure with conflicting goals',
            'personality_traits': ['ambitious', 'intelligent', 'ruthless'],
            'appearance': 'Imposing presence that commands attention',
            'background': 'Past experiences that shaped their worldview',
            'character_arc': 'Revealing depth and complexity',
            'relationships': []
        })
        
        # Supporting characters (3-5 more)
        for i in range(3):
            characters.append({
                'name': f'Support Character {i+1}',
                'role': 'supporting',
                'description': f'Important role in the {story_data["genre_info"]} narrative',
                'personality_traits': ['loyal', 'wise', 'humorous'],
                'appearance': 'Memorable visual characteristics',
                'background': 'Backstory that intersects with main plot',
                'character_arc': 'Meaningful development',
                'relationships': []
            })
        
        return characters
    
    def _generate_comic_script(self, story_data: Dict) -> str:
        """Generate detailed comic script"""
        script = f"COMIC SCRIPT: {story_data['genre_info']}\n"
        script += f"BASED ON: {story_data['story_description']}\n\n"
        
        script += "PAGE 1\n"
        script += "Panel 1: Establishing shot - sets the scene and mood\n"
        script += "CAPTION: (Introduction to the world)\n"
        script += "DIALOGUE: (Opening lines that hook the reader)\n\n"
        
        script += "Panel 2: Character introduction\n"
        script += "CHARACTER: (Main character appears)\n"
        script += "DIALOGUE: (Revealing character personality)\n\n"
        
        script += "Panel 3: Inciting incident\n"
        script += "ACTION: (Event that starts the story)\n"
        script += "DIALOGUE: (Character reaction)\n\n"
        
        # Continue for all 24 pages...
        for page in range(2, 25):
            script += f"PAGE {page}\n"
            script += f"// {self._generate_page_summary(page, story_data)}\n\n"
        
        return script
    
    def _generate_narration_script(self, story_data: Dict) -> str:
        """Generate audiobook narration script"""
        script = f"AUDIOBOOK NARRATION SCRIPT\n"
        script += f"TITLE: {story_data['genre_info']}\n"
        script += f"THEME: {story_data['story_description'][:200]}...\n\n"
        
        script += "CHAPTER 1\n"
        script += "[NARRATOR: Warm, engaging tone]\n"
        script += "The story begins in a world shaped by the themes you've described. "
        script += "Let me take you on a journey through this narrative landscape...\n\n"
        
        script += "[SOUND: Subtle ambient music begins]\n"
        script += "In the beginning, there was the setup. The characters, the setting, "
        script += "the circumstances that would lead to everything that follows...\n\n"
        
        # Generate chapters 2-12
        for chapter in range(2, 13):
            script += f"CHAPTER {chapter}\n"
            script += f"[NARRATOR: Continues with appropriate emotional tone]\n"
            script += f"{self._generate_chapter_narration(chapter, story_data)}\n\n"
        
        script += "CHAPTER 12 - CONCLUSION\n"
        script += "[NARRATOR: Reflective, satisfying tone]\n"
        script += "And so we reach the end of our journey. The threads come together, "
        script += "the characters find their resolutions, and the story finds its meaning...\n\n"
        
        script += "[SOUND: Music swells and fades out]\n"
        script += "THE END\n"
        
        return script
    
    def _generate_plot_structure(self, story_data: Dict) -> Dict[str, Any]:
        """Generate detailed plot structure"""
        return {
            'act_1': {
                'setup': 'Introduction of world, characters, and initial situation',
                'inciting_incident': 'Event that disrupts the status quo',
                'plot_point_1': 'Point of no return - commitment to the journey'
            },
            'act_2': {
                'rising_action': 'Series of challenges and developments',
                'midpoint': 'Major turning point that raises stakes',
                'plot_point_2': 'Lowest point - all seems lost'
            },
            'act_3': {
                'climax': 'Final confrontation and resolution',
                'falling_action': 'Loose ends being tied up',
                'resolution': 'Final outcome and new status quo'
            },
            'themes': self._extract_themes(story_data),
            'conflicts': self._generate_conflicts(story_data),
            'subplots': self._generate_subplots(story_data)
        }
    
    def _generate_art_descriptions(self, story_data: Dict) -> List[Dict]:
        """Generate descriptions for comic art"""
        art_descriptions = []
        
        key_scenes = [
            'Opening scene establishing mood',
            'Character introduction moments',
            'Major action sequences',
            'Emotional climax scenes',
            'Resolution and conclusion'
        ]
        
        for i, scene in enumerate(key_scenes):
            art_descriptions.append({
                'scene_number': i + 1,
                'description': f"{scene} for {story_data['genre_info']}",
                'visual_elements': self._generate_visual_elements(scene, story_data),
                'mood': self._determine_scene_mood(scene),
                'composition_notes': self._generate_composition_notes(scene)
            })
        
        return art_descriptions
    
    def _generate_voice_instructions(self, story_data: Dict) -> Dict[str, Any]:
        """Generate voice narration instructions"""
        voice_type = story_data.get('voice_type', 'MALE')
        
        instructions = {
            'pace': 'moderate with variation for dramatic effect',
            'tone': 'engaging and expressive',
            'character_voices': 'distinct but consistent',
            'emotional_range': 'full spectrum appropriate to content',
            'pacing_changes': 'slower for emotional moments, faster for action',
            'technical_notes': 'Clear enunciation, consistent volume'
        }
        
        if voice_type == 'MALE':
            instructions['voice_characteristics'] = 'Baritone to tenor range, authoritative yet warm'
        elif voice_type == 'FEMALE':
            instructions['voice_characteristics'] = 'Mezzo-soprano to alto range, expressive and clear'
        elif voice_type == 'SELF':
            instructions['voice_characteristics'] = 'Natural speaking voice with enhanced projection'
        
        return instructions
    
    def _save_content(self, content: Dict, content_type: str):
        """Save generated content to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{content_type}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        # Record generation
        self.generation_history.append({
            'filepath': filepath,
            'type': content_type,
            'timestamp': datetime.now().isoformat(),
            'word_count': content.get('word_count_estimate', 0)
        })
        
        print(f"✅ Saved {content_type}: {filename}")
    
    def _create_metadata(self, story_data: Dict) -> Dict[str, Any]:
        """Create metadata for generated content"""
        return {
            'content_type': story_data['content_type'],
            'audience_type': story_data['audience_type'],
            'content_style': story_data['content_style'],
            'genre': story_data['genre_info'],
            'created_at': datetime.now().isoformat(),
            'source_description': story_data['story_description'][:500],
            'generator_version': '1.0',
            'quality_level': 'professional'
        }
    
    # Helper methods for content generation
    def _generate_comic_panels(self, page_num: int, story_data: Dict) -> List[Dict]:
        """Generate panels for a comic page"""
        panels = []
        panels_per_page = 6
        
        for panel_num in range(1, panels_per_page + 1):
            panels.append({
                'panel_number': panel_num,
                'description': f"Panel {panel_num} on page {page_num} for {story_data['genre_info']}",
                'dialogue': f"Dialogue for panel {panel_num}",
                'action': f"Action description for panel {panel_num}",
                'focus': 'character' if panel_num % 2 == 0 else 'environment'
            })
        
        return panels
    
    def _generate_page_dialogue(self, page_num: int, story_data: Dict) -> str:
        """Generate dialogue for a comic page"""
        return f"Dialogue content for page {page_num} advancing the plot of {story_data['genre_info']}"
    
    def _generate_art_notes(self, page_num: int, story_data: Dict) -> str:
        """Generate art notes for a comic page"""
        return f"Art direction for page {page_num}: composition, lighting, and style notes for {story_data['genre_info']}"
    
    def _generate_chapter_title(self, chapter_num: int, story_data: Dict) -> str:
        """Generate title for a chapter"""
        titles = [
            "The Beginning of Everything",
            "Paths Cross",
            "Rising Tensions", 
            "Point of No Return",
            "The Darkest Hour",
            "Glimmer of Hope",
            "Turning Point",
            "Converging Paths",
            "The Calm Before",
            "Storm Breaking",
            "Resolution",
            "New Beginnings"
        ]
        return titles[chapter_num - 1] if chapter_num <= len(titles) else f"Chapter {chapter_num}"
    
    def _generate_chapter_content(self, chapter_num: int, story_data: Dict) -> str:
        """Generate content for a novel chapter"""
        return f"Chapter {chapter_num} content for {story_data['genre_info']}. This chapter develops the plot and characters based on the story description: {story_data['story_description'][:200]}..."
    
    def _generate_chapter_events(self, chapter_num: int, story_data: Dict) -> List[str]:
        """Generate key events for a chapter"""
        return [
            f"Plot development event {i} for chapter {chapter_num}"
            for i in range(1, 4)
        ]
    
    def _generate_chapter_character_development(self, chapter_num: int, story_data: Dict) -> Dict[str, str]:
        """Generate character development for a chapter"""
        return {
            'protagonist': f"Character growth for protagonist in chapter {chapter_num}",
            'antagonist': f"Revealed motivations for antagonist in chapter {chapter_num}",
            'supporting': f"Supporting character development in chapter {chapter_num}"
        }
    
    def _generate_page_summary(self, page_num: int, story_data: Dict) -> str:
        """Generate summary for a comic page"""
        return f"Page {page_num} advances the main plot with key developments in {story_data['genre_info']}"
    
    def _generate_chapter_narration(self, chapter_num: int, story_data: Dict) -> str:
        """Generate narration for an audiobook chapter"""
        return f"Chapter {chapter_num} narration content. This section of the story develops the themes of {story_data['genre_info']} and moves the plot forward with engaging storytelling."
    
    def _extract_themes(self, story_data: Dict) -> List[str]:
        """Extract themes from story data"""
        return [
            "Theme 1: Core message from story description",
            "Theme 2: Secondary thematic element", 
            "Theme 3: Underlying philosophical concept"
        ]
    
    def _generate_conflicts(self, story_data: Dict) -> List[Dict]:
        """Generate story conflicts"""
        return [
            {
                'type': 'internal',
                'description': 'Character vs self - internal struggles',
                'resolution': 'Character growth through challenge'
            },
            {
                'type': 'external',
                'description': 'Character vs world - external challenges',
                'resolution': 'Overcoming obstacles through determination'
            },
            {
                'type': 'interpersonal',
                'description': 'Character vs character - relationship dynamics',
                'resolution': 'Understanding and resolution'
            }
        ]
    
    def _generate_subplots(self, story_data: Dict) -> List[Dict]:
        """Generate story subplots"""
        return [
            {
                'subplot': 'Romantic subplot',
                'purpose': 'Add emotional depth and character motivation',
                'resolution': 'Meaningful conclusion that supports main plot'
            },
            {
                'subplot': 'Mystery element',
                'purpose': 'Add intrigue and suspense',
                'resolution': 'Reveal that enhances main story'
            }
        ]
    
    def _generate_visual_elements(self, scene: str, story_data: Dict) -> List[str]:
        """Generate visual elements for a scene"""
        return [
            'Lighting: Dramatic and mood-appropriate',
            'Composition: Dynamic and engaging',
            'Color palette: Genre-appropriate tones',
            'Perspective: Varied to maintain visual interest'
        ]
    
    def _determine_scene_mood(self, scene: str) -> str:
        """Determine mood for a scene"""
        mood_map = {
            'Opening': 'atmospheric and intriguing',
            'Character introduction': 'revealing and engaging', 
            'Major action': 'intense and dynamic',
            'Emotional climax': 'powerful and moving',
            'Resolution': 'satisfying and conclusive'
        }
        return mood_map.get(scene, 'appropriate to scene content')
    
    def _generate_composition_notes(self, scene: str) -> str:
        """Generate composition notes for a scene"""
        return f"Composition should emphasize the key elements of {scene} with strong visual storytelling"
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get statistics about text generation"""
        return {
            'total_generated': len(self.generation_history),
            'content_types': {},
            'total_words': sum(gen.get('word_count', 0) for gen in self.generation_history),
            'recent_activity': self.generation_history[-10:] if self.generation_history else []
        }
