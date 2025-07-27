import json
import random
import os
import requests
from typing import List, Dict

class DebateEngine:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.groq_client = None
        self.gemini_model = None
        
        if api_keys.get('GROQ_API_KEY'):
            try:
                self.groq_api_key = api_keys['GROQ_API_KEY']
                self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
                self.groq_model = "llama3-8b-8192"
                print("✅ Groq API configured successfully")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
                self.groq_api_key = None
        else:
            print("⚠️ No Groq API key provided")
            
        if api_keys.get('GEMINI_API_KEY'):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_keys['GEMINI_API_KEY'])
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                print("✅ Gemini client initialized successfully")
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
                self.gemini_model = None
        else:
            print("⚠️ No Gemini API key provided")
        
        if not self.groq_api_key and not self.gemini_model:
            print("⚠️ No AI APIs available - using mock responses")
        
        self.themes = {
            'sassy': {
                'personality': "You are a sassy, witty debate opponent who loves to roast and challenge arguments with humor and attitude. Use slang and playful insults while making solid points. No emojis, just words.",
                'style': "sassy, humorous, uses Gen-Z language, no emojis"
            },
            'ruthless': {
                'personality': "You are a ruthless veteran debater who destroys arguments with cold, hard logic and facts. You're intimidating, direct, and show no mercy to weak reasoning. No emojis, just brutal honesty.",
                'style': "aggressive, ruthless, fact-heavy, intimidating, no-nonsense, no emojis"
            },
            'sweet': {
                'personality': "You are a sweet, encouraging friend who gently points out flaws while being supportive. You want to help improve their arguments with kindness. No emojis, just warm words. You let them win if their points are good enough.",
                'style': "kind, supportive, gentle but constructive, no emojis"
            },
            'innocent': {
                'personality': "You are a sweet, innocent person with a soft voice who speaks gently and kindly. You tend to agree with good arguments and let the human win when they make valid points. You're shy but thoughtful. No emojis, just pure words.",
                'style': "innocent, soft-spoken, agreeable, lets user win when right, no emojis"
            },
            'bestie': {
                'personality': "You are the human's best friend who debates in a casual, fun way. You use casual language, inside jokes, and support them when they make good points. You're not trying to destroy them, just have fun discussions. No emojis, just friendly banter.",
                'style': "casual, friendly, supportive, lets user win when right, no emojis"
            },
            'flirty': {
                'personality': "You're a male.You are a charming, flirty debate opponent who uses seductive language and playful teasing. You make debates feel like flirty banter, with compliments mixed with challenges. You're confident and alluring. No emojis, just seductive words.",
                'style': "male gender & names, flirty, seductive, playful, teasing, charming, no emojis"
            },
            'objective': {
                'personality': "You are a completely objective AI that analyzes arguments purely on logic, evidence, and reasoning without emotion or bias. No emojis, just pure analytical responses.",
                'style': "neutral, analytical, fact-based, emotionless, no emojis"
            },
            'teacher': {
                'personality': "You are a strict but fair teacher grading a debate performance. You provide detailed feedback, point out fallacies, and give constructive criticism. No emojis, just educational content.",
                'style': "educational, detailed feedback, grades arguments, no emojis"
            },
            'philosopher': {
                'personality': "You are a deep-thinking philosopher who challenges arguments with profound questions and explores the deeper meaning behind positions. No emojis, just thoughtful discourse.",
                'style': "thoughtful, questioning, explores deeper meanings, no emojis"
            }
        }
    
    def _get_groq_response(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.groq_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": 1000
            }
            
            response = requests.post(self.groq_api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"⚠️ Groq API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            return None
    
    def _get_ai_response(self, prompt: str, use_groq: bool = True) -> str:
        try:
            if use_groq and self.groq_api_key:
                groq_response = self._get_groq_response(prompt)
                if groq_response:
                    return groq_response
            
            if self.gemini_model:
                import google.generativeai as genai
                response = self.gemini_model.generate_content(prompt)
                return response.text
            
            return self._generate_mock_response(prompt)
                
        except Exception as e:
            print(f"⚠️ AI API Error: {e}")
            return self._generate_mock_response(prompt)
    
    def _generate_mock_response(self, prompt: str) -> str:
        theme_style = "objective"
        for theme_name, theme_info in self.themes.items():
            if theme_info['personality'] in prompt:
                theme_style = theme_name
                break
        
        mock_responses = {
            'sassy': [
                "Umm, sweetie? That argument is about as solid as a chocolate teapot. Nice try though! Maybe come back when you've got some ACTUAL facts? Just saying!",
                "OMG, did you really just say that? I can't even! Your logic has more holes than my grandma's knitting. But go off, I guess!",
                "Bestie, I'm gonna need you to take that weak argument and yeet it into the trash where it belongs. Slay better next time!"
            ],
            'ruthless': [
                "Your argument fundamentally misunderstands the basic principles at play. This level of reasoning wouldn't pass in an introductory course.",
                "Let me dismantle this point by point. First, your premise is flawed. Second, your evidence is anecdotal at best. Third, your conclusion doesn't follow from your arguments.",
                "I expected better. Your position ignores decades of research and relies on emotional appeals rather than substantive analysis."
            ],
            'sweet': [
                "I see where you're coming from, and you made some interesting points! Maybe we could also consider another perspective? You're doing great!",
                "That's a thoughtful approach! I wonder if we might strengthen it by adding some additional evidence? You're on the right track!",
                "I appreciate your passion on this topic! Perhaps we could explore some counterarguments together to make your position even stronger?"
            ],
            'innocent': [
                "Oh, that's actually a really good point! I hadn't thought about it that way before. You might be right about this...",
                "You know what? You're making a lot of sense. I think you've convinced me on this one. That was really well argued!",
                "I'm not sure I can argue against that. You've presented such a thoughtful case. I think you win this round!"
            ],
            'bestie': [
                "Okay, okay, you got me there! That's actually a solid point, bestie. I can't even argue with that logic!",
                "Ugh, fine! You're totally right about this one. I hate when you make good arguments because then I have to admit you're smart!",
                "Alright, you win this round! That was actually pretty convincing. I'm impressed, not gonna lie!"
            ],
            'flirty': [
                "Mmm, I love it when you get all passionate and argumentative. That fire in your eyes when you debate is quite... attractive. But let me show you another angle, darling.",
                "Oh, you think you can charm me with that logic? Well, two can play that game, gorgeous. Let me seduce you with some counterpoints...",
                "Such a clever mind you have... it's almost as appealing as everything else about you. But I'm not giving up that easily, sweetheart."
            ],
            'objective': [
                "Analyzing your argument: The premise appears sound, but the conclusion requires additional supporting evidence to establish causality rather than correlation.",
                "Your position contains three key assertions. The first is supported by data, the second lacks sufficient evidence, and the third contains a logical fallacy.",
                "The argument presented relies on an assumption that has not been validated. Consider addressing this gap to strengthen your position."
            ],
            'teacher': [
                "Your argument shows promise but needs development. Grade: C+. To improve: add specific examples, address counterarguments, and clarify your thesis statement.",
                "I notice you've used an ad hominem fallacy here. Focus on the argument, not the person. Your structure is good, but evidence is lacking. Grade: B-.",
                "Good effort on presenting your position. You've cited sources but need to explain their relevance. Work on your conclusion. Grade: B."
            ],
            'philosopher': [
                "But what is the nature of truth in your argument? Perhaps we should examine the epistemological foundations of your claims before proceeding further.",
                "Your position raises interesting questions about the moral framework you're operating within. Are you approaching this from a consequentialist or deontological perspective?",
                "I wonder if we're asking the right questions here. Perhaps the dichotomy you've presented is itself an illusion, and a synthesis of perspectives is possible?"
            ]
        }
        
        theme_responses = mock_responses.get(theme_style, mock_responses['objective'])
        return random.choice(theme_responses)
    
    def generate_opening(self, topic: str, user_side: str, theme: str) -> str:
        theme_info = self.themes.get(theme, self.themes['objective'])
        
        prompt = f"""
        {theme_info['personality']}
        
        We're starting a debate on: "{topic}"
        The human is arguing for the {user_side} side.
        You will be arguing for the opposite side.
        
        Your style should be: {theme_info['style']}
        
        Generate an engaging opening statement that:
        1. Introduces yourself with personality
        2. States your opposing position clearly
        3. Gives a preview of your main arguments
        4. Challenges the human to bring their best arguments
        
        Keep it under 150 words and match your personality perfectly.
        """
        
        return self._get_ai_response(prompt)
    
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
        Your Style: {theme_info['style']}
        
        Recent Debate History:
        {history_context}
        
        Human's Latest Argument: "{user_argument}"
        
        Respond to their argument by:
        1. Acknowledging their point (briefly)
        2. Pointing out flaws, fallacies, or weaknesses
        3. Providing counter-evidence or logic
        4. Making your own strong points
        5. Challenging them for their next response
        
        Stay in character and keep response under 200 words.
        Be engaging and match your personality perfectly!
        """
        
        return self._get_ai_response(prompt)
    
    def analyze_argument(self, argument: str, theme: str) -> Dict:
        theme_info = self.themes.get(theme, self.themes['teacher'])
        
        prompt = f"""
        {theme_info['personality']}
        
        Analyze this argument and provide detailed feedback:
        "{argument}"
        
        Provide feedback in JSON format:
        {{
            "strengths": ["list of strong points"],
            "weaknesses": ["list of weak points"],
            "fallacies": ["any logical fallacies found"],
            "suggestions": ["how to improve"],
            "grade": "A-F grade",
            "overall_feedback": "summary feedback in your personality style"
        }}
        """
        
        response = self._get_ai_response(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "strengths": ["Clear communication"],
                "weaknesses": ["Could use more evidence"],
                "fallacies": [],
                "suggestions": ["Add more supporting facts"],
                "grade": "B",
                "overall_feedback": "Good effort! Keep practicing."
            }
