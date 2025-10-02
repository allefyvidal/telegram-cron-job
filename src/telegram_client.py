"""
📱 CLIENTE TELEGRAM
"""

import requests
from src.config import BOT_CONFIG

class TelegramClient:
    def __init__(self):
        self.token = BOT_CONFIG['token']
        self.chat_id = BOT_CONFIG['chat_id']
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def enviar_mensagem(self, mensagem: str) -> bool:
        """Envia mensagem para o Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": mensagem,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Erro Telegram: {e}")
            return False
