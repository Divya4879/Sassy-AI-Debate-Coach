@echo off
echo 🔧 Fixing API Setup...
echo =====================

echo.
echo 1. Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 2. Installing required packages...
pip install assemblyai==0.17.0 keyboard==0.13.5

echo.
echo 3. Setting up API keys...
if not exist "utils\api_keys_config.py" (
    copy "utils\api_keys_config_template.py" "utils\api_keys_config.py"
    echo ✅ API keys template created
    echo 📝 Please edit utils\api_keys_config.py with your actual API keys
) else (
    echo ✅ API keys file already exists
)

echo.
echo 🎉 API setup complete!
echo.
echo Next steps:
echo 1. Edit utils\api_keys_config.py with your API keys
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
pause
