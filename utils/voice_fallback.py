"""
Fallback voice manager for systems without PyAudio
"""
import os
import requests
import pyttsx3
import threading
import time
from typing import Optional

class VoiceManagerFallback:
    """Voice manager that works without PyAudio - TTS only"""
    
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.tts_engine = None
        self._init_tts()
        
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            # Configure voice settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to use a female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
            print("✅ TTS engine initialized successfully")
            
        except Exception as e:
            print(f"⚠️ TTS initialization error: {e}")
            self.tts_engine = None
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Fallback transcription - returns message about missing PyAudio"""
        return "Voice transcription unavailable - AssemblyAI not configured. Please type your argument instead."
    
    def text_to_speech(self, text: str, debate_id: str) -> str:
        """Convert text to speech and save as audio file"""
        try:
            if not self.tts_engine:
                return "TTS engine not available"
            
            # Create audio filename
            audio_filename = f"ai_response_{debate_id}_{int(time.time())}.wav"
            audio_path = os.path.join('static', 'audio', audio_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            # Save to file
            self.tts_engine.save_to_file(text, audio_path)
            self.tts_engine.runAndWait()
            
            return f"/static/audio/{audio_filename}"
            
        except Exception as e:
            print(f"⚠️ TTS error: {e}")
            return "TTS failed"
    
    def speak_text(self, text: str):
        """Speak text directly (for real-time audio)"""
        try:
            if self.tts_engine:
                def speak():
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                
                # Run in separate thread to avoid blocking
                thread = threading.Thread(target=speak)
                thread.daemon = True
                thread.start()
                
        except Exception as e:
            print(f"⚠️ Direct speech error: {e}")