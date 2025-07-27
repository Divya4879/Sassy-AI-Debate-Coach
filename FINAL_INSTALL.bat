@echo off
echo 🔧 FINAL COMPREHENSIVE INSTALLATION
echo ===================================
echo This will install EVERYTHING needed for the debate coach app

echo.
echo 1. Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 2. Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

echo.
echo 3. Installing core Flask dependencies...
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
pip install requests==2.31.0

echo.
echo 4. Installing AI dependencies...
pip install groq==0.9.0
pip install google-generativeai==0.3.2
pip install httpx==0.25.2

echo.
echo 5. Installing TTS dependencies...
pip install pyttsx3==2.90

echo.
echo 6. Installing ALL AssemblyAI dependencies...
pip uninstall assemblyai -y
pip install --upgrade assemblyai
pip install assemblyai[streaming]
pip install assemblyai[extras]
pip install websockets
pip install websocket-client

echo.
echo 7. Installing Speech Recognition fallback...
pip install SpeechRecognition==3.10.0
pip install pyaudio-wheel

echo.
echo 8. Installing additional audio dependencies...
pip install soundfile
pip install librosa

echo.
echo 9. Testing ALL installations...
python -c "import assemblyai; print('✅ AssemblyAI base installed')" 2>nul || echo "❌ AssemblyAI base failed"
python -c "from assemblyai.streaming.v3 import StreamingClient; print('✅ AssemblyAI streaming installed')" 2>nul || echo "❌ AssemblyAI streaming failed"
python -c "import speech_recognition; print('✅ SpeechRecognition installed')" 2>nul || echo "❌ SpeechRecognition failed"
python -c "import groq; print('✅ Groq installed')" 2>nul || echo "❌ Groq failed"
python -c "import google.generativeai; print('✅ Gemini installed')" 2>nul || echo "❌ Gemini failed"
python -c "import pyttsx3; print('✅ TTS installed')" 2>nul || echo "❌ TTS failed"

echo.
echo 10. Setting up API keys...
if not exist "utils\api_keys_config.py" (
    copy "utils\api_keys_config_template.py" "utils\api_keys_config.py"
    echo ✅ API keys template created
) else (
    echo ✅ API keys file already exists
)

echo.
echo 🎉 FINAL INSTALLATION COMPLETE!
echo.
echo If you see any ❌ above, run these manual commands:
echo pip install --force-reinstall assemblyai
echo pip install --force-reinstall assemblyai[streaming]
echo.
echo Next steps:
echo 1. Edit utils\api_keys_config.py with your API keys
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
pause
