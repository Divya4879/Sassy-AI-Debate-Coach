@echo off
echo 🔧 Installing All Dependencies...
echo =================================

echo.
echo 1. Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 2. Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 3. Installing core requirements...
pip install Flask==3.0.0
pip install requests==2.31.0
pip install pyttsx3==2.90
pip install Werkzeug==3.0.1

echo.
echo 4. Installing AI packages...
pip install groq==0.9.0
pip install google-generativeai==0.3.2
pip install httpx==0.25.2

echo.
echo 5. Installing voice packages...
pip install assemblyai==0.17.0
pip install SpeechRecognition==3.10.0

echo.
echo 6. Attempting PyAudio installation...
pip install pipwin
pipwin install pyaudio
if errorlevel 1 (
    echo ⚠��  PyAudio installation failed - trying alternative method...
    pip install pyaudio
    if errorlevel 1 (
        echo ⚠️  PyAudio unavailable - voice recording will be disabled
        echo 💡 Voice transcription and TTS will still work
    )
)

echo.
echo 7. Testing installations...
python -c "import assemblyai; print('✅ AssemblyAI installed')" 2>nul || echo "❌ AssemblyAI failed"
python -c "import groq; print('✅ Groq installed')" 2>nul || echo "❌ Groq failed"
python -c "import google.generativeai; print('✅ Gemini installed')" 2>nul || echo "❌ Gemini failed"
python -c "import pyttsx3; print('✅ TTS installed')" 2>nul || echo "❌ TTS failed"

echo.
echo 8. Setting up API keys...
if not exist "utils\api_keys_config.py" (
    copy "utils\api_keys_config_template.py" "utils\api_keys_config.py"
    echo ✅ API keys template created
    echo 📝 Please edit utils\api_keys_config.py with your actual API keys
) else (
    echo ✅ API keys file already exists
)

echo.
echo 🎉 Installation complete!
echo.
echo Next steps:
echo 1. Edit utils\api_keys_config.py with your API keys
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
pause
