# 🔧 Troubleshooting Guide

## PyAudio Installation Issues

### Windows
**Problem:** `Microsoft Visual C++ 14.0 or greater is required`

**Solutions (try in order):**

1. **Use pipwin (Easiest):**
   \`\`\`bash
   pip install pipwin
   pipwin install pyaudio
   \`\`\`

2. **Use pre-compiled wheel:**
   - Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
   - Download appropriate `.whl` file
   - Install: `pip install downloaded_file.whl`

3. **Use Anaconda:**
   \`\`\`bash
   conda install pyaudio
   \`\`\`

4. **Install Build Tools:**
   - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "C++ build tools"
   - Then: `pip install pyaudio`

### macOS
\`\`\`bash
brew install portaudio
pip install pyaudio
\`\`\`

### Linux (Ubuntu/Debian)
\`\`\`bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
\`\`\`

## API Key Issues

### Missing API Keys
- Copy `utils/api_keys_config_template.py` to `utils/api_keys_config.py`
- Add your actual API keys
- App works with mock responses if no keys provided

### Invalid API Keys
- Check key format and validity
- Verify account quotas
- Test keys in API documentation

## Voice Recording Issues

### Browser Permissions
- Allow microphone access when prompted
- Check browser settings for microphone permissions
- Try refreshing the page

### No Microphone Detected
- Ensure microphone is connected
- Check system audio settings
- Test microphone in other applications

### Recording Not Working
- Try different browsers (Chrome recommended)
- Check for HTTPS requirement (use localhost)
- Disable browser extensions that might interfere

## General Issues

### Port Already in Use
\`\`\`bash
# Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
\`\`\`

### Module Import Errors
\`\`\`bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall requirements
pip install -r requirements.txt
\`\`\`

### App Won't Start
1. Check Python version (3.8+ required)
2. Verify all dependencies installed
3. Check for error messages in console
4. Try running with debug: `python app.py --debug`

## Performance Issues

### Slow AI Responses
- Check internet connection
- Verify API key quotas
- Try different AI model (Groq vs Gemini)

### Audio Processing Slow
- Check AssemblyAI quota
- Ensure good microphone quality
- Try shorter audio clips

## Getting Help

If issues persist:
1. Check the console for error messages
2. Verify all setup steps completed
3. Try running the automated setup script
4. Create an issue with error details

## Running Without Voice Features

The app gracefully handles missing PyAudio:
- Voice recording will be disabled
- Text input still works perfectly
- TTS (text-to-speech) may still work
- All other features remain functional
