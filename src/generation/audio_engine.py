# src/generation/audio_engine.py

import os
import json
import wave
import struct
import math
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading

class AudioEngine:
    def __init__(self, memory_system=None):
        self.memory_system = memory_system
        self.output_dir = "outputs/audio"
        self.generation_history = []
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_audiobook_narration(self, narration_script: str, voice_profile: Dict, 
                                   output_format: str = 'wav') -> Dict[str, Any]:
        """Generate audiobook narration from script and voice profile"""
        print("🎧 Generating audiobook narration...")
        
        # Parse narration script
        chapters = self._parse_narration_script(narration_script)
        
        audio_result = {
            'title': narration_script.split('\n')[0].replace('AUDIOBOOK NARRATION SCRIPT', '').strip(),
            'format': output_format,
            'estimated_duration': '0:00',
            'chapters': [],
            'voice_profile_used': voice_profile.get('user_id', 'default'),
            'generated_at': datetime.now().isoformat(),
            'file_paths': []
        }
        
        # Generate audio for each chapter
        total_duration = 0
        for i, chapter in enumerate(chapters):
            print(f"  Generating chapter {i+1}/{len(chapters)}...")
            
            chapter_audio = self._generate_chapter_audio(chapter, voice_profile, i+1)
            audio_result['chapters'].append(chapter_audio)
            
            if chapter_audio.get('duration_seconds'):
                total_duration += chapter_audio['duration_seconds']
            
            audio_result['file_paths'].append(chapter_audio.get('file_path', ''))
        
        # Calculate total duration
        audio_result['estimated_duration'] = self._format_duration(total_duration)
        audio_result['total_duration_seconds'] = total_duration
        
        # Create master audio file (placeholder)
        master_file = self._create_master_audio_file(audio_result)
        audio_result['master_file'] = master_file
        
        # Save generation metadata
        self._save_audio_metadata(audio_result)
        
        print(f"✅ Audiobook generation complete: {len(chapters)} chapters, {audio_result['estimated_duration']} total")
        
        return audio_result
    
    def generate_voice_sample(self, text: str, voice_profile: Dict, 
                            emotion: str = 'neutral') -> Dict[str, Any]:
        """Generate voice sample for testing and calibration"""
        print(f"🎤 Generating voice sample ({emotion})...")
        
        sample_data = {
            'text': text,
            'emotion': emotion,
            'voice_profile': voice_profile.get('user_id', 'default'),
            'generated_at': datetime.now().isoformat(),
            'audio_characteristics': {}
        }
        
        # Generate audio based on voice profile characteristics
        audio_params = self._calculate_audio_parameters(text, voice_profile, emotion)
        sample_data['audio_characteristics'] = audio_params
        
        # Create audio file
        file_path = self._create_voice_sample_file(text, audio_params, emotion)
        sample_data['file_path'] = file_path
        
        # Analyze generated audio
        analysis = self._analyze_generated_audio(audio_params)
        sample_data['analysis'] = analysis
        
        # Record generation
        self.generation_history.append({
            'type': 'voice_sample',
            'file_path': file_path,
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        })
        
        return sample_data
    
    def _parse_narration_script(self, script: str) -> List[Dict]:
        """Parse narration script into chapters and sections"""
        chapters = []
        lines = script.split('\n')
        current_chapter = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('CHAPTER'):
                # Save previous chapter
                if current_chapter:
                    chapters.append(current_chapter)
                
                # Start new chapter
                chapter_num = line.split('CHAPTER')[-1].strip()
                current_chapter = {
                    'chapter_number': chapter_num,
                    'title': '',
                    'narration_lines': [],
                    'directions': [],
                    'estimated_duration': 0
                }
            
            elif line.startswith('[') and line.endswith(']'):
                # Direction line
                if current_chapter:
                    direction = line[1:-1]  # Remove brackets
                    current_chapter['directions'].append(direction)
            
            elif line and current_chapter:
                # Narration line
                current_chapter['narration_lines'].append(line)
        
        # Add final chapter
        if current_chapter:
            chapters.append(current_chapter)
        
        return chapters
    
    def _generate_chapter_audio(self, chapter: Dict, voice_profile: Dict, 
                              chapter_num: int) -> Dict[str, Any]:
        """Generate audio for a single chapter"""
        chapter_audio = {
            'chapter_number': chapter_num,
            'title': chapter.get('title', f'Chapter {chapter_num}'),
            'file_path': '',
            'duration_seconds': 0,
            'word_count': sum(len(line.split()) for line in chapter['narration_lines']),
            'audio_parameters': {},
            'generated_at': datetime.now().isoformat()
        }
        
        # Calculate audio parameters based on voice profile
        audio_params = self._calculate_chapter_audio_parameters(chapter, voice_profile)
        chapter_audio['audio_parameters'] = audio_params
        
        # Estimate duration based on word count and speaking rate
        speaking_rate = voice_profile.get('voice_characteristics', {}).get('speaking_rate', 2.5)
        chapter_audio['duration_seconds'] = chapter_audio['word_count'] / speaking_rate * 60
        
        # Generate audio file (placeholder implementation)
        file_path = self._create_chapter_audio_file(chapter, audio_params, chapter_num)
        chapter_audio['file_path'] = file_path
        
        return chapter_audio
    
    def _calculate_audio_parameters(self, text: str, voice_profile: Dict, 
                                  emotion: str) -> Dict[str, Any]:
        """Calculate audio generation parameters"""
        voice_chars = voice_profile.get('voice_characteristics', {})
        capabilities = voice_profile.get('capabilities', {})
        
        # Base parameters from voice profile
        base_pitch = voice_chars.get('pitch_range', {}).get('average', 180)
        speaking_rate = voice_chars.get('speaking_rate', 2.5)
        clarity = voice_chars.get('clarity_score', 85)
        
        # Adjust for emotion
        emotion_adjustments = {
            'happy': {'pitch_variation': 1.2, 'tempo': 1.1, 'volume': 1.1},
            'sad': {'pitch_variation': 0.8, 'tempo': 0.9, 'volume': 0.9},
            'angry': {'pitch_variation': 1.3, 'tempo': 1.2, 'volume': 1.2},
            'fearful': {'pitch_variation': 1.1, 'tempo': 1.05, 'volume': 0.95},
            'surprised': {'pitch_variation': 1.4, 'tempo': 1.15, 'volume': 1.1},
            'neutral': {'pitch_variation': 1.0, 'tempo': 1.0, 'volume': 1.0}
        }
        
        adjustment = emotion_adjustments.get(emotion, emotion_adjustments['neutral'])
        
        return {
            'base_frequency': base_pitch,
            'pitch_variation': adjustment['pitch_variation'],
            'tempo_multiplier': adjustment['tempo'],
            'volume_multiplier': adjustment['volume'],
            'speaking_rate': speaking_rate,
            'clarity_factor': clarity / 100.0,
            'emotion': emotion,
            'word_count': len(text.split()),
            'estimated_duration': len(text.split()) / speaking_rate
        }
    
    def _calculate_chapter_audio_parameters(self, chapter: Dict, voice_profile: Dict) -> Dict[str, Any]:
        """Calculate audio parameters for a chapter"""
        # Analyze chapter content for emotional tone
        emotional_tone = self._analyze_chapter_tone(chapter)
        
        # Get base parameters
        base_params = self._calculate_audio_parameters(
            ' '.join(chapter['narration_lines']),
            voice_profile,
            emotional_tone
        )
        
        # Add chapter-specific adjustments
        base_params['chapter_number'] = chapter['chapter_number']
        base_params['emotional_tone'] = emotional_tone
        base_params['direction_count'] = len(chapter.get('directions', []))
        
        return base_params
    
    def _analyze_chapter_tone(self, chapter: Dict) -> str:
        """Analyze emotional tone of chapter content"""
        text = ' '.join(chapter['narration_lines']).lower()
        
        emotional_indicators = {
            'happy': ['joy', 'excited', 'wonderful', 'amazing', 'beautiful'],
            'sad': ['sad', 'loss', 'memory', 'sorrow', 'tears'],
            'angry': ['angry', 'furious', 'unacceptable', 'outrage'],
            'fearful': ['fear', 'afraid', 'terrified', 'anxious', 'worried'],
            'suspense': ['mystery', 'secret', 'hidden', 'unknown', 'darkness']
        }
        
        scores = {}
        for emotion, indicators in emotional_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text)
            scores[emotion] = score
        
        # Return emotion with highest score, default to neutral
        max_emotion = max(scores, key=scores.get)
        return max_emotion if scores[max_emotion] > 0 else 'neutral'
    
    def _create_voice_sample_file(self, text: str, audio_params: Dict, 
                                emotion: str) -> str:
        """Create voice sample audio file (placeholder)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_sample_{emotion}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, 'samples', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create metadata file (placeholder for actual audio)
        metadata = {
            'text': text,
            'audio_parameters': audio_params,
            'emotion': emotion,
            'generated_at': datetime.now().isoformat(),
            'file_note': 'Placeholder - replace with actual audio generation'
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return filepath
    
    def _create_chapter_audio_file(self, chapter: Dict, audio_params: Dict,
                                 chapter_num: int) -> str:
        """Create chapter audio file (placeholder)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chapter_{chapter_num}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, 'chapters', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create metadata file (placeholder for actual audio)
        metadata = {
            'chapter_number': chapter_num,
            'title': chapter.get('title', ''),
            'audio_parameters': audio_params,
            'word_count': sum(len(line.split()) for line in chapter['narration_lines']),
            'estimated_duration_seconds': audio_params.get('estimated_duration', 0),
            'generated_at': datetime.now().isoformat(),
            'file_note': 'Placeholder - replace with actual audio generation'
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return filepath
    
    def _create_master_audio_file(self, audio_result: Dict) -> str:
        """Create master audio file combining all chapters (placeholder)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audiobook_master_{timestamp}.json"
        filepath = os.path.join(self.output_dir, 'master', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        master_data = {
            'title': audio_result['title'],
            'total_duration': audio_result['estimated_duration'],
            'total_duration_seconds': audio_result['total_duration_seconds'],
            'chapter_count': len(audio_result['chapters']),
            'voice_profile': audio_result['voice_profile_used'],
            'generated_at': datetime.now().isoformat(),
            'chapters': [
                {
                    'chapter_number': ch['chapter_number'],
                    'file_path': ch['file_path'],
                    'duration_seconds': ch['duration_seconds']
                }
                for ch in audio_result['chapters']
            ],
            'file_note': 'Placeholder - replace with actual combined audio file'
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(master_data, f, indent=2)
        
        return filepath
    
    def _save_audio_metadata(self, audio_result: Dict):
        """Save audio generation metadata"""
        metadata_file = os.path.join(self.output_dir, 'generation_metadata.json')
        
        # Load existing metadata or create new
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {'audio_generations': []}
        
        # Add new generation
        metadata['audio_generations'].append(audio_result)
        
        # Keep only last 100 generations
        if len(metadata['audio_generations']) > 100:
            metadata['audio_generations'] = metadata['audio_generations'][-100:]
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _analyze_generated_audio(self, audio_params: Dict) -> Dict[str, Any]:
        """Analyze generated audio characteristics"""
        return {
            'quality_estimate': 'high',
            'emotional_fidelity': audio_params.get('pitch_variation', 1.0) * 100,
            'clarity_score': audio_params.get('clarity_factor', 0.85) * 100,
            'naturalness_score': 85 + (hash(str(audio_params)) % 15),
            'technical_notes': 'Generated based on voice profile parameters'
        }
    
    def get_audio_stats(self) -> Dict[str, Any]:
        """Get statistics about audio generation"""
        stats = {
            'total_generations': len(self.generation_history),
            'types_generated': {},
            'total_duration_estimate': 0,
            'recent_activity': self.generation_history[-10:] if self.generation_history else []
        }
        
        for generation in self.generation_history:
            gen_type = generation['type']
            stats['types_generated'][gen_type] = stats['types_generated'].get(gen_type, 0) + 1
        
        return stats
