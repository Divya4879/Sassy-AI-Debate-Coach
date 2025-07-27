from flask import Flask, render_template, request, jsonify, session
import os
import json
import threading
import time
import sys
import ssl
from datetime import datetime
from debate_engine import DebateEngine

print(f"🐍 Python Version: {sys.version}")
print(f"🐍 Python Version Info: {sys.version_info}")

try:
    from utils.voice_python313 import VoiceManagerPython313 as VoiceManager
    VOICE_MODULE_AVAILABLE = True
    print("✅ Python 3.13 compatible voice module imported successfully")
except ImportError as e:
    print(f"❌ Voice module import failed: {e}")
    from utils.voice_fallback import VoiceManagerFallback as VoiceManager
    VOICE_MODULE_AVAILABLE = False

from utils.api_keys import get_api_keys

app = Flask(__name__)
app.secret_key = 'debate_coach_secret_key_2024'

print("🔄 Initializing components...")
api_keys = get_api_keys()
debate_engine = DebateEngine(api_keys)
voice_manager = VoiceManager(api_keys)

if VOICE_MODULE_AVAILABLE:
    voice_status = voice_manager.get_voice_status()
    print("🎤 FINAL VOICE STATUS:")
    for feature, available in voice_status.items():
        status = "✅" if available else "❌"
        print(f"   {feature}: {status}")
else:
    print("❌ Voice features running in fallback mode")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice_status')
def voice_status_endpoint():
    if VOICE_MODULE_AVAILABLE:
        return jsonify(voice_manager.get_voice_status())
    else:
        return jsonify({
            'tts_available': False,
            'theme_voices_available': False,
            'assemblyai_available': False,
            'assemblyai_streaming_available': False,
            'voice_recording_available': False,
            'realtime_available': False,
            'python_version_compatible': False
        })

@app.route('/start_debate', methods=['POST'])
def start_debate():
    data = request.json
    
    session['debate_topic'] = data.get('topic')
    session['user_side'] = data.get('side')
    session['ai_theme'] = data.get('theme')
    session['debate_history'] = []
    session['debate_id'] = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    opening_response = debate_engine.generate_opening(
        topic=session['debate_topic'],
        user_side=session['user_side'],
        theme=session['ai_theme']
    )
    
    session['debate_history'].append({
        'speaker': 'ai',
        'message': opening_response,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'success': True,
        'ai_response': opening_response,
        'debate_id': session['debate_id'],
        'theme': session['ai_theme']
    })

@app.route('/submit_argument', methods=['POST'])
def submit_argument():
    data = request.json
    user_argument = data.get('argument', '').strip()
    
    if not user_argument:
        return jsonify({'error': 'No argument provided'}), 400
    
    session['debate_history'].append({
        'speaker': 'user',
        'message': user_argument,
        'timestamp': datetime.now().isoformat()
    })
    
    ai_response = debate_engine.generate_response(
        user_argument=user_argument,
        topic=session['debate_topic'],
        user_side=session['user_side'],
        theme=session['ai_theme'],
        debate_history=session['debate_history']
    )
    
    session['debate_history'].append({
        'speaker': 'ai',
        'message': ai_response,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'success': True,
        'ai_response': ai_response,
        'theme': session['ai_theme']
    })

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file provided'}), 400
        
        temp_path = f"temp_audio_{session.get('debate_id', 'unknown')}.wav"
        audio_file.save(temp_path)
        
        print(f"🔄 Starting transcription of {temp_path}")
        
        transcription = voice_manager.transcribe_audio(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        print(f"✅ Transcription result: {transcription[:100]}...")
        
        return jsonify({
            'success': True,
            'transcription': transcription
        })
    
    except Exception as e:
        print(f"❌ Transcription endpoint error: {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.json
        text = data.get('text', '')
        theme = data.get('theme', 'objective')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        audio_path = voice_manager.text_to_speech(
            text, 
            session.get('debate_id', 'unknown'),
            theme
        )
        
        return jsonify({
            'success': True,
            'audio_path': audio_path
        })
    
    except Exception as e:
        return jsonify({'error': f'TTS failed: {str(e)}'}), 500

@app.route('/get_debate_history')
def get_debate_history():
    return jsonify({
        'history': session.get('debate_history', []),
        'topic': session.get('debate_topic', ''),
        'user_side': session.get('user_side', ''),
        'theme': session.get('ai_theme', '')
    })

@app.route('/reset_debate', methods=['POST'])
def reset_debate():
    session.clear()
    return jsonify({'success': True})

def create_self_signed_cert():
    """Create a self-signed certificate for HTTPS"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Debate Coach"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write certificate and key to files
        with open("cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open("key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Self-signed certificate created")
        return True
        
    except ImportError:
        print("❌ cryptography package not available for HTTPS")
        return False
    except Exception as e:
        print(f"❌ Failed to create certificate: {e}")
        return False

if __name__ == '__main__':
    os.makedirs('static/audio', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    
    print("\n🎯 RHETORIC ARENA - AI DEBATE COMPANION")
    print(f"🐍 Python {sys.version_info.major}.{sys.version_info.minor} Compatible")
    
    # Try to run with HTTPS for microphone access
    use_https = False
    if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
        print("🔒 Creating self-signed certificate for HTTPS...")
        use_https = create_self_signed_cert()
    else:
        use_https = True
    
    if use_https:
        print("🔒 Starting with HTTPS for microphone access")
        print("🌐 Open https://localhost:5000 in your browser")
        print("⚠️  You'll see a security warning - click 'Advanced' then 'Proceed to localhost'")
        print("=" * 70)
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        
        app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=context)
    else:
        print("🌐 Starting with HTTP - microphone may not work on network IPs")
        print("🌐 For microphone access, use: http://localhost:5000")
        print("⚠️  Do NOT use IP addresses like 172.15.1.51 - use localhost only")
        print("=" * 70)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
