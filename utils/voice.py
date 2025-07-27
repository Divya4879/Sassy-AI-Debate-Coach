import os
import requests
import pyttsx3
import threading
import time
import tempfile
from typing import Optional

# Try to import AssemblyAI with fallback
try:
    import assemblyai as aai
    from assemblyai.streaming.v3 import (
        BeginEvent,
        StreamingClient,
        StreamingClientOptions,
        StreamingError,
        StreamingEvents,
        StreamingParameters,
        StreamingSessionParameters,
        TerminationEvent,
        TurnEvent,
    )
    ASSEMBLYAI_AVAILABLE = True
    print("✅ AssemblyAI module loaded successfully")
except ImportError as e:
    print(f"⚠️ AssemblyAI not available: {e}")
    print("💡 Run: pip install assemblyai==0.17.0")
    ASSEMBLYAI_AVAILABLE = False

# Try to import SpeechRecognition as fallback
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
    print("✅ SpeechRecognition available as fallback")
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ SpeechRecognition not available")

class VoiceManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.tts_engine = None
        self.assemblyai_available = False
        self.speech_recognition_available = SPEECH_RECOGNITION_AVAILABLE
        
        self._init_tts()
        self._init_assemblyai()
        
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
    
    def _init_assemblyai(self):
        """Initialize AssemblyAI if available"""
        if ASSEMBLYAI_AVAILABLE and self.api_keys.get('ASSEMBLYAI_API_KEY'):
            try:
                aai.settings.api_key = self.api_keys['ASSEMBLYAI_API_KEY']
                self.assemblyai_available = True
                print("✅ AssemblyAI initialized successfully")
            except Exception as e:
                print(f"⚠️ AssemblyAI initialization failed: {e}")
                self.assemblyai_available = False
        else:
            if not ASSEMBLYAI_AVAILABLE:
                print("⚠️ AssemblyAI module not installed")
            else:
                print("⚠️ AssemblyAI API key not provided")
            self.assemblyai_available = False
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using AssemblyAI or fallback methods"""
        
        # Try AssemblyAI first
        if self.assemblyai_available:
            try:
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(audio_file_path)
                
                if transcript.status == "completed":
                    print("✅ AssemblyAI transcription successful")
                    return transcript.text
                else:
                    print(f"⚠️ AssemblyAI transcription failed with status: {transcript.status}")
            except Exception as e:
                print(f"⚠️ AssemblyAI transcription error: {e}")
        
        # Try SpeechRecognition as fallback
        if self.speech_recognition_available:
            try:
                r = sr.Recognizer()
                with sr.AudioFile(audio_file_path) as source:
                    audio = r.record(source)
                    text = r.recognize_google(audio)
                    print("✅ Google Speech Recognition successful")
                    return text
            except Exception as e:
                print(f"⚠️ Speech Recognition error: {e}")
        
        # If all methods fail
        return "Transcription failed. Please type your argument instead."
    
    def transcribe_audio_with_assemblyai_api(self, audio_file_path: str) -> str:
        """Direct API call to AssemblyAI as another fallback"""
        if not self.api_keys.get('ASSEMBLYAI_API_KEY'):
            return "AssemblyAI API key not configured"
        
        try:
            # Upload audio file
            headers = {'authorization': self.api_keys['ASSEMBLYAI_API_KEY']}
            
            with open(audio_file_path, 'rb') as f:
                response = requests.post(
                    'https://api.assemblyai.com/v2/upload',
                    headers=headers,
                    files={'file': f}
                )
            
            if response.status_code != 200:
                return f"Upload failed: {response.status_code}"
            
            upload_url = response.json()['upload_url']
            
            # Request transcription
            data = {
                'audio_url': upload_url,
                'speaker_labels': False,
                'auto_highlights': False
            }
            
            response = requests.post(
                'https://api.assemblyai.com/v2/transcript',
                headers={**headers, 'content-type': 'application/json'},
                json=data
            )
            
            if response.status_code != 200:
                return f"Transcription request failed: {response.status_code}"
            
            transcript_id = response.json()['id']
            
            # Poll for completion
            url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'
            
            for _ in range(30):  # Max 30 attempts (60 seconds)
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result['status']
                    
                    if status == 'completed':
                        print("✅ AssemblyAI API transcription successful")
                        return result['text']
                    elif status == 'error':
                        return f"Transcription error: {result.get('error')}"
                
                time.sleep(2)
            
            return "Transcription timeout"
            
        except Exception as e:
            print(f"⚠️ AssemblyAI API error: {e}")
            return f"API transcription error: {str(e)}"
    
    def start_realtime_transcription(self, callback):
        """Start real-time transcription using AssemblyAI streaming API"""
        if not self.assemblyai_available:
            callback("AssemblyAI not available for real-time transcription")
            return None
            
        try:
            client = StreamingClient(
                StreamingClientOptions(
                    api_key=self.api_keys['ASSEMBLYAI_API_KEY'],
                    api_host="streaming.assemblyai.com",
                )
            )
            
            def on_begin(self, event: BeginEvent):
                print(f"🎤 Transcription session started: {event.id}")
            
            def on_turn(self, event: TurnEvent):
                transcript = event.transcript
                is_partial = not event.end_of_turn
                
                if is_partial:
                    if len(transcript) >= 4:
                        print(f"👂 Partial: {transcript}")
                        callback(transcript, is_partial=True)
                else:
                    print(f"🗣️ Complete: {transcript}")
                    callback(transcript, is_partial=False)
            
            def on_terminated(self, event: TerminationEvent):
                print(f"🏁 Transcription session ended: {event.audio_duration_seconds:.2f} seconds")
            
            def on_error(self, error: StreamingError):
                print(f"💥 Error occurred: {error}")
                callback(f"Error: {error}", is_error=True)
            
            client.on(StreamingEvents.Begin, on_begin)
            client.on(StreamingEvents.Turn, on_turn)
            client.on(StreamingEvents.Termination, on_terminated)
            client.on(StreamingEvents.Error, on_error)
            
            # Optimized streaming parameters for lower latency
            client.connect(
                StreamingParameters(
                    sample_rate=16000,
                    format_turns=True,
                    end_of_turn_confidence_threshold=0.5,
                    min_end_of_turn_silence_when_confident=100,
                    max_turn_silence=1500,
                )
            )
            
            return client
            
        except Exception as e:
            print(f"⚠️ Real-time transcription error: {e}")
            callback(f"Error starting transcription: {str(e)}", is_error=True)
            return None
    
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
    
    def get_voice_status(self):
        """Get status of voice features"""
        return {
            'tts_available': self.tts_engine is not None,
            'assemblyai_available': self.assemblyai_available,
            'speech_recognition_available': self.speech_recognition_available,
            'voice_recording_available': self.assemblyai_available or self.speech_recognition_available
        }