"""
Ultra-robust voice manager with multiple fallbacks and comprehensive error handling
"""
import os
import requests
import pyttsx3
import threading
import time
import tempfile
from typing import Optional, Callable

# Import with comprehensive error handling
ASSEMBLYAI_AVAILABLE = False
ASSEMBLYAI_STREAMING_AVAILABLE = False
SPEECH_RECOGNITION_AVAILABLE = False

# Try AssemblyAI base
try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
    print("✅ AssemblyAI base module loaded")
except ImportError as e:
    print(f"❌ AssemblyAI base not available: {e}")

# Try AssemblyAI streaming
try:
    from assemblyai.streaming.v3 import (
        BeginEvent,
        StreamingClient,
        StreamingClientOptions,
        StreamingError,
        StreamingEvents,
        StreamingParameters,
        TerminationEvent,
        TurnEvent,
    )
    ASSEMBLYAI_STREAMING_AVAILABLE = True
    print("✅ AssemblyAI streaming module loaded")
except ImportError as e:
    print(f"❌ AssemblyAI streaming not available: {e}")

# Try SpeechRecognition
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
    print("✅ SpeechRecognition module loaded")
except ImportError as e:
    print(f"❌ SpeechRecognition not available: {e}")

class VoiceManagerRobust:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.tts_engine = None
        self.assemblyai_available = False
        self.assemblyai_streaming_available = False
        self.speech_recognition_available = SPEECH_RECOGNITION_AVAILABLE
        
        self._init_tts()
        self._init_assemblyai()
        self._print_status()
        
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.9)
            print("✅ TTS engine initialized successfully")
            
        except Exception as e:
            print(f"❌ TTS initialization error: {e}")
            self.tts_engine = None
    
    def _init_assemblyai(self):
        """Initialize AssemblyAI with comprehensive checks"""
        if ASSEMBLYAI_AVAILABLE and self.api_keys.get('ASSEMBLYAI_API_KEY'):
            try:
                aai.settings.api_key = self.api_keys['ASSEMBLYAI_API_KEY']
                self.assemblyai_available = True
                print("✅ AssemblyAI base initialized successfully")
                
                if ASSEMBLYAI_STREAMING_AVAILABLE:
                    self.assemblyai_streaming_available = True
                    print("✅ AssemblyAI streaming initialized successfully")
                else:
                    print("⚠️ AssemblyAI streaming not available")
                    
            except Exception as e:
                print(f"❌ AssemblyAI initialization failed: {e}")
                self.assemblyai_available = False
        else:
            if not ASSEMBLYAI_AVAILABLE:
                print("❌ AssemblyAI module not installed")
            else:
                print("❌ AssemblyAI API key not provided")
    
    def _print_status(self):
        """Print comprehensive status of all voice features"""
        print("\n🎤 VOICE FEATURES STATUS:")
        print(f"   TTS Available: {'✅' if self.tts_engine else '❌'}")
        print(f"   AssemblyAI Base: {'✅' if self.assemblyai_available else '❌'}")
        print(f"   AssemblyAI Streaming: {'✅' if self.assemblyai_streaming_available else '❌'}")
        print(f"   Speech Recognition: {'✅' if self.speech_recognition_available else '❌'}")
        print(f"   Voice Recording: {'✅' if (self.assemblyai_available or self.speech_recognition_available) else '❌'}")
        print()
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using all available methods"""
        
        # Method 1: AssemblyAI SDK
        if self.assemblyai_available:
            try:
                print("🔄 Trying AssemblyAI SDK...")
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(audio_file_path)
                
                if transcript.status == "completed":
                    print("✅ AssemblyAI SDK transcription successful")
                    return transcript.text
                else:
                    print(f"⚠️ AssemblyAI SDK failed with status: {transcript.status}")
            except Exception as e:
                print(f"❌ AssemblyAI SDK error: {e}")
        
        # Method 2: AssemblyAI Direct API
        if self.api_keys.get('ASSEMBLYAI_API_KEY'):
            try:
                print("🔄 Trying AssemblyAI Direct API...")
                result = self._transcribe_with_api(audio_file_path)
                if result and "error" not in result.lower():
                    print("✅ AssemblyAI API transcription successful")
                    return result
                else:
                    print(f"⚠️ AssemblyAI API failed: {result}")
            except Exception as e:
                print(f"❌ AssemblyAI API error: {e}")
        
        # Method 3: Google Speech Recognition
        if self.speech_recognition_available:
            try:
                print("🔄 Trying Google Speech Recognition...")
                r = sr.Recognizer()
                with sr.AudioFile(audio_file_path) as source:
                    audio = r.record(source)
                    text = r.recognize_google(audio)
                    print("✅ Google Speech Recognition successful")
                    return text
            except Exception as e:
                print(f"❌ Speech Recognition error: {e}")
        
        # All methods failed
        return "❌ All transcription methods failed. Please type your argument instead."
    
    def _transcribe_with_api(self, audio_file_path: str) -> str:
        """Direct API call to AssemblyAI"""
        try:
            headers = {'authorization': self.api_keys['ASSEMBLYAI_API_KEY']}
            
            # Upload file
            with open(audio_file_path, 'rb') as f:
                response = requests.post(
                    'https://api.assemblyai.com/v2/upload',
                    headers=headers,
                    files={'file': f},
                    timeout=30
                )
            
            if response.status_code != 200:
                return f"Upload failed: {response.status_code}"
            
            upload_url = response.json()['upload_url']
            
            # Request transcription
            data = {'audio_url': upload_url}
            response = requests.post(
                'https://api.assemblyai.com/v2/transcript',
                headers={**headers, 'content-type': 'application/json'},
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"Transcription request failed: {response.status_code}"
            
            transcript_id = response.json()['id']
            
            # Poll for completion
            url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'
            
            for attempt in range(30):  # 60 seconds max
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result['status']
                    
                    if status == 'completed':
                        return result['text']
                    elif status == 'error':
                        return f"Transcription error: {result.get('error')}"
                
                time.sleep(2)
            
            return "Transcription timeout"
            
        except Exception as e:
            return f"API error: {str(e)}"
    
    def start_realtime_transcription(self, callback: Callable):
        """Start real-time transcription if streaming is available"""
        if not self.assemblyai_streaming_available:
            callback("Real-time transcription not available", is_error=True)
            return None
            
        try:
            client = StreamingClient(
                StreamingClientOptions(
                    api_key=self.api_keys['ASSEMBLYAI_API_KEY'],
                    api_host="streaming.assemblyai.com",
                )
            )
            
            def on_begin(self, event: BeginEvent):
                print(f"🎤 Real-time session started: {event.id}")
            
            def on_turn(self, event: TurnEvent):
                transcript = event.transcript
                is_partial = not event.end_of_turn
                
                if is_partial and len(transcript) >= 4:
                    callback(transcript, is_partial=True)
                elif not is_partial:
                    callback(transcript, is_partial=False)
            
            def on_terminated(self, event: TerminationEvent):
                print(f"🏁 Real-time session ended: {event.audio_duration_seconds:.2f}s")
            
            def on_error(self, error: StreamingError):
                print(f"❌ Real-time error: {error}")
                callback(f"Error: {error}", is_error=True)
            
            client.on(StreamingEvents.Begin, on_begin)
            client.on(StreamingEvents.Turn, on_turn)
            client.on(StreamingEvents.Termination, on_terminated)
            client.on(StreamingEvents.Error, on_error)
            
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
            print(f"❌ Real-time transcription error: {e}")
            callback(f"Error starting real-time: {str(e)}", is_error=True)
            return None
    
    def text_to_speech(self, text: str, debate_id: str) -> str:
        """Convert text to speech"""
        try:
            if not self.tts_engine:
                return "TTS engine not available"
            
            audio_filename = f"ai_response_{debate_id}_{int(time.time())}.wav"
            audio_path = os.path.join('static', 'audio', audio_filename)
            
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            self.tts_engine.save_to_file(text, audio_path)
            self.tts_engine.runAndWait()
            
            return f"/static/audio/{audio_filename}"
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return "TTS failed"
    
    def speak_text(self, text: str):
        """Speak text directly"""
        try:
            if self.tts_engine:
                def speak():
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                
                thread = threading.Thread(target=speak)
                thread.daemon = True
                thread.start()
                
        except Exception as e:
            print(f"❌ Direct speech error: {e}")
    
    def get_voice_status(self):
        """Get comprehensive voice status"""
        return {
            'tts_available': self.tts_engine is not None,
            'assemblyai_available': self.assemblyai_available,
            'assemblyai_streaming_available': self.assemblyai_streaming_available,
            'speech_recognition_available': self.speech_recognition_available,
            'voice_recording_available': self.assemblyai_available or self.speech_recognition_available,
            'realtime_available': self.assemblyai_streaming_available
        }

# Alias for backward compatibility
VoiceManager = VoiceManagerRobust
