# 🎯 Debate Master

**Transform Your Arguments into Masterpieces Through AI-Powered Intellectual Combat**

An advanced, open-source debate training platform featuring intelligent AI opponents with distinct personalities, real-time voice transcription, dynamic text-to-speech, and comprehensive argument analysis. Built for developers, debaters, and anyone passionate about the art of persuasion.

---

## 🌟 About The Project

Debate Master revolutionizes how we practice and perfect the art of argumentation. Unlike static debate tools, this platform provides dynamic, personality-driven AI opponents that adapt to your arguments, challenge your reasoning, and help you develop stronger persuasive skills.

Whether you're a student preparing for competitions, a professional honing presentation skills, or simply someone who loves intellectual discourse, Debate Master offers an immersive experience that makes learning argumentation engaging and effective.

### Why Debate Master?

- **9 Unique AI Personalities**: From supportive friends to ruthless critics
- **Real-time Voice Processing**: Speak naturally, get instant transcription
- **Adaptive Learning**: AI remembers context and builds on previous arguments
- **Professional Grade APIs**: Powered by Groq, Google Gemini, and AssemblyAI
- **Open Source**: Fully customizable and community-driven

---

## ✨ Features

### 🎭 AI Personalities
- **Sassy Coach**: Witty roasts with humor and attitude
- **Ruthless Veteran**: Cold logic that destroys weak arguments  
- **Sweet Friend**: Kind, supportive, constructive feedback
- **Sweet Angel**: Innocent, lets you win when you're right
- **Your Bestie**: Casual, fun, supports good arguments
- **Charming Rival**: Flirty, seductive, playful banter
- **Objective AI**: Pure logic, no emotion, just facts
- **Strict Teacher**: Grades performance with detailed feedback
- **Deep Philosopher**: Questions everything, explores deeper meaning

### 🎤 Voice Features
- Real-time speech-to-text transcription
- Theme-specific text-to-speech voices
- Hold-to-record interface
- Multi-language support via AssemblyAI

### 🧠 Intelligence
- Context-aware conversations
- Argument history tracking
- Fallback API system for reliability
- Mock responses when APIs unavailable

### 🎨 User Experience
- Beautiful dark theme with glass morphism
- Responsive design for all devices
- Smooth animations and transitions
- Intuitive debate flow

---

## 📁 Project Structure

\`\`\`
debate-master/
├── app.py                          # Main Flask application
├── debate_engine.py                # AI personality and response logic
├── requirements_python313.txt      # Python dependencies
├── static/
│   ├── app.js                     # Frontend JavaScript logic
│   └── audio/                     # Generated TTS audio files
├── templates/
│   └── index.html                 # Main UI template
├── utils/
│   ├── api_keys.py               # API key management
│   ├── api_keys_config.py        # Your API keys (create this)
│   ├── api_keys_config_template.py # API key template
│   └── voice_python313.py        # Voice processing manager
├── scripts/
│   ├── ULTIMATE_FIX.bat          # Windows setup automation
│   └── setup_windows.bat         # Alternative Windows setup
└── README.md                      # This file
\`\`\`

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Python 3.13 fully supported)
- Git
- Microphone (optional, for voice features)
- Modern web browser (Chrome, Firefox, Safari)

### 1. Fork & Clone
\`\`\`bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/debate-master.git
cd debate-master
\`\`\`

### 2. Environment Setup
\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements_python313.txt
\`\`\`

### 4. Configure API Keys
\`\`\`bash
# Copy template
cp utils/api_keys_config_template.py utils/api_keys_config.py

# Edit with your API keys
# Get keys from:
# - Groq: https://console.groq.com/keys
# - Google Gemini: https://makersuite.google.com/app/apikey
# - AssemblyAI: https://www.assemblyai.com/dashboard/signup
\`\`\`

### 5. Run Application
\`\`\`bash
python app.py
\`\`\`

### 6. Open Browser
Navigate to `http://localhost:5000`

---

## 🔧 Core Code Functions

### 1. Voice Manager Initialization
```python
def __init__(self, api_keys):
    self.api_keys = api_keys
    self.tts_engine = None
    self.assemblyai_available = False
    self.available_voices = {}
    
    self._init_tts()
    self._init_assemblyai()
```

**Purpose**: Initializes the voice processing system with text-to-speech engine and AssemblyAI transcription. Sets up theme-specific voices for different AI personalities and handles graceful fallbacks when services are unavailable.

### 2. AssemblyAI Audio Transcription

```python
def transcribe_audio(self, audio_file_path: str) -> str:
    if self.assemblyai_available:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path)
        
        if transcript.status == "completed":
            return transcript.text
    
    return self._transcribe_with_api(audio_file_path)
```

**Purpose**: Converts recorded audio to text using AssemblyAI's advanced speech recognition. Includes fallback to direct API calls and comprehensive error handling for robust voice-to-text conversion.

### 3. Emoji Removal for TTS

```python
def _remove_emojis(self, text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map
                               u"\U0001F1E0-\U0001F1FF"  # flags
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
```

**Purpose**: Strips emojis from AI responses before text-to-speech conversion to prevent TTS engines from reading emoji names aloud. Ensures clean, natural-sounding voice output.

### 4. Theme-Specific Voice Assignment

```python
def text_to_speech(self, text: str, debate_id: str, theme: str = None) -> str:
    clean_text = self._remove_emojis(text)
    
    if theme and theme in self.available_voices:
        voice_id = self.available_voices[theme]
        self.tts_engine.setProperty('voice', voice_id)
    
    audio_filename = f"ai_response_{debate_id}_{int(time.time())}.wav"
    audio_path = os.path.join('static', 'audio', audio_filename)
    
    self.tts_engine.save_to_file(clean_text, audio_path)
    self.tts_engine.runAndWait()
    
    return f"/static/audio/{audio_filename}"
```

**Purpose**: Generates speech with personality-specific voices. Maps AI themes to appropriate voice characteristics (male/female, tone) and creates audio files for web playback.

### 5. AI Personality System

```python
def generate_response(self, user_argument: str, topic: str, user_side: str, theme: str, debate_history: List[Dict]) -> str:
    theme_info = self.themes.get(theme, self.themes['objective'])
    
    history_context = ""
    for entry in debate_history[-4:]:
        speaker = "Human" if entry['speaker'] == 'user' else "AI"
        history_context += f"{speaker}: {entry['message']}\n"
    
    prompt = f"""
    {theme_info['personality']}
    
    Debate Topic: "{topic}"
    Human's Position: {user_side}
    Your Position: Opposite of {user_side}
    
    Recent Debate History:
    {history_context}
    
    Human's Latest Argument: "{user_argument}"
    
    Respond in character matching your personality perfectly!
    """
    
    return self._get_ai_response(prompt)
```

**Purpose**: Creates dynamic AI responses based on selected persona. Each theme has unique personality traits and debate styles. Maintains conversation context for coherent, engaging debates.

### 6. Multi-API Fallback System

```python
def _get_ai_response(self, prompt: str, use_groq: bool = True) -> str:
    try:
        if use_groq and self.groq_api_key:
            groq_response = self._get_groq_response(prompt)
            if groq_response:
                return groq_response
        
        if self.gemini_model:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        
        return self._generate_mock_response(prompt)
    except Exception as e:
        return self._generate_mock_response(prompt)
```

**Purpose**: Ensures application reliability through cascading API fallbacks. Tries Groq first for speed, falls back to Gemini for reliability, and provides themed mock responses if all APIs fail.

### 7. Real-time Audio Streaming

```python
def start_realtime_transcription(self, callback: Callable):
    client = StreamingClient(
        StreamingClientOptions(
            api_key=self.api_keys['ASSEMBLYAI_API_KEY'],
            api_host="streaming.assemblyai.com",
        )
    )
    
    def on_turn(self, event: TurnEvent):
        transcript = event.transcript
        is_partial = not event.end_of_turn
        
        if is_partial and len(transcript) >= 4:
            callback(transcript, is_partial=True)
        elif not is_partial:
            callback(transcript, is_partial=False)
    
    client.connect(StreamingParameters(sample_rate=16000, format_turns=True))
```

**Purpose**: Enables live speech-to-text conversion during debates. Provides immediate feedback with partial transcriptions for responsive user experience and natural conversation flow.

### 8. Debate Session Management

```python
@app.route('/start_debate', methods=['POST'])
def start_debate():
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
    
    return jsonify({
        'success': True,
        'ai_response': opening_response,
        'debate_id': session['debate_id'],
        'theme': session['ai_theme']
    })
```

**Purpose**: Manages debate state across user sessions. Tracks conversation history, maintains context, and ensures consistent AI personality throughout the entire debate experience.

### 9. Browser Audio Recording

```javascript
async startRecording() {
if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
alert("Your browser doesn't support audio recording.")
return
}

```plaintext
const stream = await navigator.mediaDevices.getUserMedia({ 
    audio: {
        echoCancellation: true,
        noiseSuppression: true,
        sampleRate: 44100
    } 
})

this.mediaRecorder = new MediaRecorder(stream, {
    mimeType: 'audio/webm;codecs=opus'
})

this.mediaRecorder.start(1000)
this.isRecording = true
```

}

```plaintext
**Purpose**: Handles browser-based audio recording with optimal settings for speech recognition. Includes comprehensive error handling for microphone permissions and browser compatibility.

### 10. Dynamic UI State Management
\`\`\`javascript
selectTheme(theme) {
    this.selectedTheme = theme
    
    const themeNames = {
        sassy: "Sassy Coach",
        ruthless: "Ruthless Veteran",
        flirty: "Charming Rival",
        // ... other themes
    }
    
    document.getElementById("theme-text").textContent = themeNames[theme]
    document.getElementById("selected-theme").classList.remove("hidden")
    
    document.querySelectorAll(".theme-card").forEach((card) => {
        card.classList.remove("selected")
    })
    
    document.querySelector(`[data-theme="${theme}"]`).classList.add("selected")
}
```

**Purpose**: Manages the debate setup flow and UI state transitions. Handles theme selection, visual feedback, and progressive disclosure of debate options for intuitive user experience.

---

## Contributing

We welcome contributions from developers of all skill levels! Here's how to get involved:

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**: `git clone https://github.com/YOUR_USERNAME/debate-master.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Install dependencies**: `pip install -r requirements_python313.txt`
5. **Make your changes** and test thoroughly
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**


### Contribution Areas

- 🎭 **New AI Personalities**: Create unique debate opponents
- 🎤 **Voice Features**: Enhance audio processing capabilities
- 🎨 **UI/UX**: Improve design and user experience
- 🧠 **AI Logic**: Enhance argument analysis and responses
- 📱 **Mobile Support**: Optimize for mobile devices
- 🌐 **Internationalization**: Add multi-language support
- 🔧 **Performance**: Optimize speed and reliability
- 📚 **Documentation**: Improve guides and examples


### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Include error handling
- Write tests for new features


---

## Troubleshooting

### Common Issues

**Recording Not Working**

- Check microphone permissions in browser
- Ensure HTTPS or localhost (required for microphone access)
- Try different browsers (Chrome recommended)


**API Errors**

- Verify API keys in `utils/api_keys_config.py`
- Check API quotas and billing
- Test with mock responses (works without API keys)


**Installation Issues**

- Use Python 3.8+ (3.13 recommended)
- Try virtual environment: `python -m venv venv`
- On Windows, run `ULTIMATE_FIX.bat`


**Voice Features Disabled**

- Install AssemblyAI: `pip install assemblyai>=0.17.0`
- Check API key configuration
- Verify microphone hardware


### Getting Help

1. Check existing [GitHub Issues](https://github.com/yourusername/debate-master/issues)
2. Create a new issue with detailed error information
3. Join our community discussions
4. Review the troubleshooting scripts in `/scripts/`


---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **AssemblyAI** for advanced speech recognition
- **Groq** for lightning-fast LLM inference
- **Google** for Gemini AI capabilities
- **Flask** community for the robust web framework
- **Open Source Community** for inspiration and contributions


---

## Star History

If you find this project helpful, please consider giving it a star! ⭐

---

**Built with ❤️ by the Debate Master community**

*Transform your arguments. Master your voice. Win every debate.*

```plaintext



</CodeProject>

<Actions>
<Action name="Test recording functionality" description="Test the fixed audio recording feature in different browsers" />
<Action name="Add more AI personalities" description="Create additional unique debate opponent personalities" />
<Action name="Implement argument scoring" description="Add a scoring system to evaluate debate performance" />
<Action name="Create mobile-responsive design" description="Optimize the interface for mobile devices" />
<Action name="Add debate replay feature" description="Allow users to review and replay past debates" />
</Actions>
