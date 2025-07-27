import os
from typing import Dict

def get_api_keys() -> Dict[str, str]:
    
    api_keys = {}
    
    # Try to load from environment variables first
    api_keys['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
    api_keys['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
    api_keys['ASSEMBLYAI_API_KEY'] = os.getenv('ASSEMBLYAI_API_KEY')
    
    # Try to load from api_keys.py file
    try:
        from utils.api_keys_config import GROQ_API_KEY, GEMINI_API_KEY, ASSEMBLYAI_API_KEY
        
        if not api_keys['GROQ_API_KEY']:
            api_keys['GROQ_API_KEY'] = GROQ_API_KEY
        if not api_keys['GEMINI_API_KEY']:
            api_keys['GEMINI_API_KEY'] = GEMINI_API_KEY
        if not api_keys['ASSEMBLYAI_API_KEY']:
            api_keys['ASSEMBLYAI_API_KEY'] = ASSEMBLYAI_API_KEY
            
    except ImportError:
        print("⚠️  API keys config file not found. Create utils/api_keys_config.py")
        print("📝 See utils/api_keys_config_template.py for template")
    
    # Filter out None values
    return {k: v for k, v in api_keys.items() if v}