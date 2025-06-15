import os
from dotenv import load_dotenv

load_dotenv('config.env')

class APIManager:
    """Quản lý các API providers và keys"""
    
    def __init__(self):
        self.load_api_keys()
        self.load_provider_preferences()
    
    def load_api_keys(self):
        """Load tất cả API keys từ environment"""
        self.api_keys = {
            # AI Content Generation
            'openai': os.getenv('OPENAI_API_KEY'),
            'claude': os.getenv('CLAUDE_API_KEY'),
            'deepseek': os.getenv('DEEPSEEK_API_KEY'),
            
            # Image Generation
            'midjourney': os.getenv('MIDJOURNEY_API_KEY'),
            'stability_ai': os.getenv('STABILITY_AI_KEY'),
            
            # Text-to-Speech
            'elevenlabs': os.getenv('ELEVENLABS_API_KEY'),
            'google_tts': os.getenv('GOOGLE_TTS_API_KEY'),
            'azure_speech': os.getenv('AZURE_SPEECH_KEY'),
            'azure_region': os.getenv('AZURE_SPEECH_REGION', 'eastus')
        }
    
    def load_provider_preferences(self):
        """Load provider preferences từ config"""
        self.providers = {
            'content': os.getenv('CONTENT_PROVIDER', 'OpenAI GPT-4'),
            'image': os.getenv('IMAGE_PROVIDER', 'DALL-E (OpenAI)'),
            'tts': os.getenv('TTS_PROVIDER', 'Google TTS (Free)')
        }
    
    def get_available_content_providers(self):
        """Lấy danh sách content providers có API key"""
        available = []
        
        if self.is_api_key_valid('openai'):
            available.append('OpenAI GPT-4')
        if self.is_api_key_valid('claude'):
            available.append('Claude (Anthropic)')
        if self.is_api_key_valid('deepseek'):
            available.append('DeepSeek')
        
        if available:
            available.append('Auto (thử theo thứ tự)')
        
        return available or ['Chưa cấu hình API key']
    
    def get_available_image_providers(self):
        """Lấy danh sách image providers có API key"""
        available = []
        
        if self.is_api_key_valid('openai'):
            available.append('DALL-E (OpenAI)')
        if self.is_api_key_valid('midjourney'):
            available.append('Midjourney')
        if self.is_api_key_valid('stability_ai'):
            available.append('Stable Diffusion')
        
        if available:
            available.append('Auto (thử theo thứ tự)')
        
        return available or ['Chưa cấu hình API key']
    
    def get_available_tts_providers(self):
        """Lấy danh sách TTS providers có API key"""
        available = ['Google TTS (Free)']  # Google TTS free không cần key
        
        if self.is_api_key_valid('elevenlabs'):
            available.append('ElevenLabs')
        if self.is_api_key_valid('azure_speech'):
            available.append('Azure Speech')
        
        available.append('Auto (thử theo thứ tự)')
        return available
    
    def is_api_key_valid(self, provider):
        """Kiểm tra API key có hợp lệ không"""
        key = self.api_keys.get(provider)
        if not key:
            return False
        
        # Kiểm tra format cơ bản
        invalid_keys = ['your_', 'test_', 'sk-test-', 'sk_test_']
        return not any(key.startswith(invalid) for invalid in invalid_keys)
    
    def get_api_key(self, provider):
        """Lấy API key cho provider"""
        return self.api_keys.get(provider)
    
    def get_provider_config(self, service_type):
        """Lấy provider được chọn cho service"""
        return self.providers.get(service_type)
    
    def update_provider_preference(self, service_type, provider):
        """Cập nhật provider preference"""
        self.providers[service_type] = provider
        # TODO: Lưu vào file config
    
    def get_provider_status(self):
        """Lấy trạng thái tất cả providers"""
        status = {
            'content_providers': {
                'OpenAI GPT-4': self.is_api_key_valid('openai'),
                'Claude (Anthropic)': self.is_api_key_valid('claude'),
                'DeepSeek': self.is_api_key_valid('deepseek')
            },
            'image_providers': {
                'DALL-E (OpenAI)': self.is_api_key_valid('openai'),
                'Midjourney': self.is_api_key_valid('midjourney'),
                'Stable Diffusion': self.is_api_key_valid('stability_ai')
            },
            'tts_providers': {
                'Google TTS (Free)': True,  # Always available
                'ElevenLabs': self.is_api_key_valid('elevenlabs'),
                'Azure Speech': self.is_api_key_valid('azure_speech')
            }
        }
        return status
    
    def get_fallback_provider(self, service_type):
        """Lấy provider fallback khi provider chính không khả dụng"""
        fallbacks = {
            'content': ['OpenAI GPT-4', 'Claude (Anthropic)', 'DeepSeek'],
            'image': ['DALL-E (OpenAI)', 'Stable Diffusion', 'Midjourney'],
            'tts': ['Google TTS (Free)', 'ElevenLabs', 'Azure Speech']
        }
        
        available_providers = []
        for provider in fallbacks.get(service_type, []):
            if service_type == 'content':
                provider_key = provider.split()[0].lower()
            elif service_type == 'image':
                if 'DALL-E' in provider:
                    provider_key = 'openai'
                elif 'Stable' in provider:
                    provider_key = 'stability_ai'
                else:
                    provider_key = 'midjourney'
            else:  # tts
                if 'Google' in provider:
                    available_providers.append(provider)
                    continue
                elif 'ElevenLabs' in provider:
                    provider_key = 'elevenlabs'
                else:
                    provider_key = 'azure_speech'
            
            if service_type != 'tts' or 'Google' not in provider:
                if self.is_api_key_valid(provider_key):
                    available_providers.append(provider)
        
        return available_providers[0] if available_providers else None 