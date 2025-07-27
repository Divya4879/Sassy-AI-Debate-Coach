# 🎯 Rhetoric Arena
**Speak your mind and challenge the AI, because only through resistance do your ideas sharpen and your voice truly grow.**

An advanced, open-source debate platform featuring intelligent AI opponents with distinct personalities, real-time voice transcription, dynamic text-to-speech, and comprehensive argument analysis. Built for developers, debaters, and anyone passionate about the art of persuasion.

Some project snapshots:-

<img width="1920" height="2720" alt="screencapture-localhost-5000-2025-07-28-01_09_15" src="https://github.com/user-attachments/assets/731bcf7c-973e-426d-b4a2-0581f497b01c" />

<img width="1920" height="1458" alt="screencapture-localhost-5000-2025-07-28-01_09_51" src="https://github.com/user-attachments/assets/25d8c527-506b-45f7-aba9-59a1aa78dea4" />



---

## About The Project

Rhetoric Arena revolutionizes how we practice and perfect the art of argumentation. Unlike static debate tools, this platform provides dynamic, personality-driven AI opponents that adapt to your arguments, challenge your reasoning, and help you develop stronger persuasive skills.

Whether you're a student preparing for competitions, a professional honing presentation skills, or simply someone who loves intellectual discourse, this product offers an immersive experience that makes learning argumentation engaging and effective.

### Why Rhetoric Arena?

- **9 Unique AI Personalities**: From supportive friends to ruthless critics
- **Real-time Voice Processing**: Speak naturally, get instant transcription
- **Adaptive Learning**: AI remembers context and builds on previous arguments
- **Professional Grade APIs**: Powered by Groq, Google Gemini, and AssemblyAI

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

### 🎨 User Experience
- Beautiful dark theme with glass morphism
- Responsive design for all devices
- Smooth animations and transitions
- Intuitive debate flow

---

## 📁 Project Structure

```bash
debate-master/
├── app.py                          # Main Flask application
├── debate_engine.py                # AI personality and response logic
├── requirements_python313.txt      # Python dependencies
├── static/
│   ├── app.js                      # Frontend JavaScript logic
│   └── audio/                      # Generated TTS audio files
├── templates/
│   └── index.html                  # Main UI template
├── utils/
│   ├── api_keys.py                 # API key management
│   ├── api_keys_config.py          # Your API keys (create this)
│   ├── api_keys_config_template.py # API key template
│   └── voice_python313.py          # Voice processing manager
├── scripts/
│   ├── ULTIMATE_FIX.bat            # Windows setup automation
│   └── setup_windows.bat           # Alternative Windows setup
└── README.md                       # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Python 3.13 fully supported)
- Git
- Microphone (optional, for voice features)
- Modern web browser (Chrome, Firefox, Safari)

Here’s your section, cleaned and formatted beautifully for `README.md` in Markdown:

---

### 🚀 Getting Started

#### 1. **Fork & Clone**

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/Divya4879/Sassy-AI-Debate-Coach.git
cd Sassy-AI-Debate-Coach
```

#### 2. **Environment Setup**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 3. **Install Dependencies**

```bash
pip install -r requirements_python313.txt
```

#### 4. **Configure API Keys**

```bash
# Copy the template config file
cp utils/api_keys_config_template.py utils/api_keys_config.py
```

> ✍️ Open `utils/api_keys_config.py` and paste your API keys.
> Get your keys from:

* **Groq:** [https://console.groq.com/keys](https://console.groq.com/keys)
* **Gemini:** [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
* **AssemblyAI:** [https://www.assemblyai.com/dashboard/signup](https://www.assemblyai.com/dashboard/signup)

#### 5. **Run the Application**

```bash
python app.py
```

#### 6. **Launch in Browser**

Open your browser and go to:
`http://localhost:5000`

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


---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **AssemblyAI** for advanced speech recognition
- **Groq** for lightning-fast LLM inference
- **Google** for Gemini AI capabilities
- **Flask** community for the robust web framework

---


**Built with ❤️ by the Divya for the [AssemblyAI Voice Agents Challenge](https://dev.to/challenges/assemblyai-2025-07-16) by Dev.to**
