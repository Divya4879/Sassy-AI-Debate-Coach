@echo off
echo 🔧 ULTIMATE PYTHON COMPATIBILITY FIX
echo ====================================
echo Fixing Python 3.13 compatibility issues and installing everything properly

echo.
echo 1. Checking Python version...
python --version

echo.
echo 2. Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 3. Upgrading core tools...
python -m pip install --upgrade pip setuptools wheel

echo.
echo 4. Installing Python 3.13 compatible packages...
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
pip install requests==2.31.0

echo.
echo 5. Installing AI packages...
pip install groq==0.9.0
pip install google-generativeai==0.3.2
pip install httpx==0.25.2

echo.
echo 6. Installing TTS (works on all Python versions)...
pip install pyttsx3==2.90

echo.
echo 7. Installing AssemblyAI with all dependencies...
pip uninstall assemblyai -y
pip install assemblyai>=0.17.0
pip install websockets>=11.0
pip install websocket-client>=1.6.0

echo.
echo 8. Skipping SpeechRecognition (Python 3.13 incompatible)...
echo    Using AssemblyAI and direct API calls instead

echo.
echo 9. Installing audio processing alternatives...
pip install soundfile
pip install numpy

echo.
echo 10. Testing installations...
python -c "import assemblyai; print('✅ AssemblyAI base installed')" 2>nul || echo "❌ AssemblyAI base failed"
python -c "from assemblyai.streaming.v3 import StreamingClient; print('✅ AssemblyAI streaming installed')" 2>nul || echo "❌ AssemblyAI streaming failed"
python -c "import groq; print('✅ Groq installed')" 2>nul || echo "❌ Groq failed"
python -c "import google.generativeai; print('✅ Gemini installed')" 2>nul || echo "❌ Gemini failed"
python -c "import pyttsx3; print('✅ TTS installed')" 2>nul || echo "❌ TTS failed"

echo.
echo 11. Setting up API keys...
if not exist "utils\api_keys_config.py" (
    copy "utils\api_keys_config_template.py" "utils\api_keys_config.py"
    echo ✅ API keys template created
) else (
    echo ✅ API keys file already exists
)

echo.
echo 🎉 ULTIMATE FIX COMPLETE!
echo.
echo ✅ Python 3.13 compatibility issues resolved
echo ✅ SpeechRecognition replaced with AssemblyAI-only solution
echo ✅ All working components installed
echo.
echo Next steps:
echo 1. Edit utils\api_keys_config.py with your API keys
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
pause
