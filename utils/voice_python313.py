import os
import requests
import pyttsx3
import threading
import time
import tempfile
import re
from typing import Optional, Callable

ASSEMBLYAI_AVAILABLE = False
ASSEMBLYAI_STREAMING_AVAILABLE = False

try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
    print("✅ AssemblyAI base module loaded")
except ImportError as e:
    print(f"❌ AssemblyAI base not available: {e}")

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

class VoiceManagerPython313:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.tts_engine = None
        self.assemblyai_available = False
        self.assemblyai_streaming_available = False
        self.available_voices = {}
        
        self._init_tts()
        self._init_assemblyai()
        self._print_status()
        
    def _init_tts(self):
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            
            default_voice = voices[0].id if voices else None
            
            theme_voice_map = {
                'sassy': ['female', 'zira', 'hazel'],
                'ruthless': ['male', 'david', 'mark'],
                'sweet': ['female', 'zira', 'hazel'],
                'innocent': ['female', 'zira', 'hazel'],
                'bestie': ['female', 'zira', 'hazel'],
                'flirty': ['male', 'david', 'mark'],
                'objective': ['male', 'david'],
                'teacher': ['female', 'zira'],
                'philosopher': ['male', 'david']
            }
            
            if voices:
                print(f"✅ Found {len(voices)} voices")
                
                for theme, keywords in theme_voice_map.items():
                    for voice in voices:
                        voice_name = voice.name.lower()
                        if any(keyword in voice_name for keyword in keywords):
                            self.available_voices[theme] = voice.id
                            print(f"✅ Assigned voice '{voice.name}' to theme '{theme}'")
                            break
                    
                    if theme not in self.available_voices:
                        self.available_voices[theme] = default_voice
                        print(f"⚠️ Using default voice for theme '{theme}'")
            
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.9)
            print("✅ TTS engine initialized successfully")
            
        except Exception as e:
            print(f"❌ TTS initialization error: {e}")
            self.tts_engine = None
    
    def _init_assemblyai(self):
        if ASSEMBLYAI_AVAILABLE and self.api_keys.get('ASSEMBLYAI_API_KEY'):
            try:
                aai.settings.api_key = self.api_keys['ASSEMBLYAI_API_KEY']
                self.assemblyai_available = True
                print("✅ AssemblyAI base initialized successfully")
                
                if ASSEMBLYAI_STREAMING_AVAILABLE:
                    self.assemblyai_streaming_available = True
                    print("✅ AssemblyAI streaming initialized successfully")
                    
            except Exception as e:
                print(f"❌ AssemblyAI initialization failed: {e}")
                self.assemblyai_available = False
        else:
            if not ASSEMBLYAI_AVAILABLE:
                print("❌ AssemblyAI module not installed")
            else:
                print("❌ AssemblyAI API key not provided")
    
    def _print_status(self):
        print("\n🎤 VOICE FEATURES STATUS (Python 3.13 Compatible):")
        print(f"   TTS Available: {'✅' if self.tts_engine else '❌'}")
        print(f"   Theme-specific voices: {'✅' if self.available_voices else '❌'}")
        print(f"   AssemblyAI Base: {'✅' if self.assemblyai_available else '❌'}")
        print(f"   AssemblyAI Streaming: {'✅' if self.assemblyai_streaming_available else '❌'}")
        print(f"   Voice Recording: {'✅' if self.assemblyai_available else '❌'}")
        print()
    
    def _remove_emojis(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"
                                   u"\U0001F300-\U0001F5FF"
                                   u"\U0001F680-\U0001F6FF"
                                   u"\U0001F1E0-\U0001F1FF"
                                   u"\U00002500-\U00002BEF"
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        if self.assemblyai_available:
            try:
                print("🔄 Trying AssemblyAI SDK...")
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(audio_file_path)
                
                if transcript.status == "completed":
                    print("✅ AssemblyAI SDK transcription successful")
                    return transcript.text
                elif transcript.status == "error":
                    print(f"❌ AssemblyAI SDK error: {transcript.error}")
                else:
                    print(f"⚠️ AssemblyAI SDK status: {transcript.status}")
            except Exception as e:
                print(f"❌ AssemblyAI SDK error: {e}")
        
        if self.api_keys.get('ASSEMBLYAI_API_KEY'):
            try:
                print("🔄 Trying AssemblyAI Direct API...")
                result = self._transcribe_with_api(audio_file_path)
                if result and not result.startswith("❌") and not result.startswith("Error"):
                    print("✅ AssemblyAI API transcription successful")
                    return result
                else:
                    print(f"❌ AssemblyAI API failed: {result}")
            except Exception as e:
                print(f"❌ AssemblyAI API error: {e}")
        
        return "❌ Transcription failed. AssemblyAI API key may be missing or invalid. Please type your argument instead."
    
    def _transcribe_with_api(self, audio_file_path: str) -> str:
        try:
            headers = {'authorization': self.api_keys['ASSEMBLYAI_API_KEY']}
            
            print("📤 Uploading audio file...")
            with open(audio_file_path, 'rb') as f:
                response = requests.post(
                    'https://api.assemblyai.com/v2/upload',
                    headers=headers,
                    files={'file': f},
                    timeout=60
                )
            
            if response.status_code != 200:
                return f"❌ Upload failed: {response.status_code} - {response.text}"
            
            upload_url = response.json()['upload_url']
            print(f"✅ File uploaded: {upload_url}")
            
            print("🔄 Requesting transcription...")
            data = {
                'audio_url': upload_url,
                'language_detection': True,
                'punctuate': True,
                'format_text': True
            }
            
            response = requests.post(
                'https://api.assemblyai.com/v2/transcript',
                headers={**headers, 'content-type': 'application/json'},
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"❌ Transcription request failed: {response.status_code} - {response.text}"
            
            transcript_id = response.json()['id']
            print(f"🔄 Transcription ID: {transcript_id}")
            
            url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'
            
            for attempt in range(60):
                print(f"🔄 Checking status... (attempt {attempt + 1}/60)")
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result['status']
                    
                    if status == 'completed':
                        text = result.get('text', '')
                        if text:
                            return text
                        else:
                            return "❌ No text in transcription result"
                    elif status == 'error':
                        error_msg = result.get('error', 'Unknown error')
                        return f"❌ Transcription error: {error_msg}"
                    elif status in ['queued', 'processing']:
                        print(f"⏳ Status: {status}")
                    else:
                        print(f"⚠️ Unknown status: {status}")
                else:
                    print(f"⚠️ Status check failed: {response.status_code}")
                
                time.sleep(2)
            
            return "❌ Transcription timeout (2 minutes exceeded)"
            
        except requests.exceptions.Timeout:
            return "❌ Request timeout - check your internet connection"
        except requests.exceptions.RequestException as e:
            return f"❌ Network error: {str(e)}"
        except Exception as e:
            return f"❌ API error: {str(e)}"
    
    def start_realtime_transcription(self, callback: Callable):
        if not self.assemblyai_streaming_available:
            callback("❌ Real-time transcription not available", is_error=True)
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
    
    def text_to_speech(self, text: str, debate_id: str, theme: str = None) -> str:
        try:
            if not self.tts_engine:
                return "❌ TTS engine not available"
            
            clean_text = self._remove_emojis(text)
            
            if theme and theme in self.available_voices:
                voice_id = self.available_voices[theme]
                self.tts_engine.setProperty('voice', voice_id)
                print(f"🎤 Using voice for theme '{theme}'")
            
            audio_filename = f"ai_response_{debate_id}_{int(time.time())}.wav"
            audio_path = os.path.join('static', 'audio', audio_filename)
            
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            self.tts_engine.save_to_file(clean_text, audio_path)
            self.tts_engine.runAndWait()
            
            return f"/static/audio/{audio_filename}"
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return "❌ TTS failed"
    
    def speak_text(self, text: str, theme: str = None):
        try:
            if self.tts_engine:
                clean_text = self._remove_emojis(text)
                
                if theme and theme in self.available_voices:
                    voice_id = self.available_voices[theme]
                    self.tts_engine.setProperty('voice', voice_id)
                
                def speak():
                    self.tts_engine.say(clean_text)
                    self.tts_engine.runAndWait()
                
                thread = threading.Thread(target=speak)
                thread.daemon = True
                thread.start()
                
        except Exception as e:
            print(f"❌ Direct speech error: {e}")
    
    def get_voice_status(self):
        return {
            'tts_available': self.tts_engine is not None,
            'theme_voices_available': len(self.available_voices) > 0,
            'assemblyai_available': self.assemblyai_available,
            'assemblyai_streaming_available': self.assemblyai_streaming_available,
            'voice_recording_available': self.assemblyai_available,
            'realtime_available': self.assemblyai_streaming_available,
            'python_version_compatible': True
        }

VoiceManager = VoiceManagerPython313

