@echo off
echo 🎯 RHETORIC ARENA - ONE-CLICK SETUP
echo ===================================
echo This will install everything you need for the debate coach app
echo.

echo 1. Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    echo Make sure Python 3.8+ is installed
    pause
    exit /b 1
)

echo.
echo 2. Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 3. Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo 4. Installing all dependencies...
pip install -r requirements_python313.txt

echo.
echo 5. Setting up API keys...
if not exist "utils\api_keys_config.py" (
    copy "utils\api_keys_config_template.py" "utils\api_keys_config.py"
    echo ✅ API keys template created
    echo 📝 IMPORTANT: Edit utils\api_keys_config.py with your actual API keys
) else (
    echo ✅ API keys file already exists
)

echo.
echo 6. Testing installations...
python -c "import assemblyai; print('✅ AssemblyAI installed')" 2>nul || echo "❌ AssemblyAI failed"
python -c "import groq; print('✅ Groq installed')" 2>nul || echo "❌ Groq failed"
python -c "import google.generativeai; print('✅ Gemini installed')" 2>nul || echo "❌ Gemini failed"
python -c "import pyttsx3; print('✅ TTS installed')" 2>nul || echo "❌ TTS failed"

echo.
echo 🎉 SETUP COMPLETE!
echo.
echo NEXT STEPS:
echo 1. Edit utils\api_keys_config.py with your API keys
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000 (use localhost, NOT IP address)
echo.
echo MICROPHONE ISSUE? Use localhost:5000, not IP addresses!
echo.
pause
