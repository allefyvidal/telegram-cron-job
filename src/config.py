"""
📋 CONFIGURAÇÕES DO BOT
"""

import os

# Telegram (usa environment variables)
BOT_CONFIG = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
}

# APIs
API_KEYS = {
    'fred': os.getenv('FRED_API_KEY', ''),
}

# Séries para monitorar
FRED_SERIES = {
    "Dólar": "DEXBZUS",
    "Bitcoin": "CBBTCUSD", 
    "Selic": "SELIC",
    "IPCA": "CPIALTT01BRM659N",
    "PIB Brasil": "BRALOCOSTORSTM",
}

# Configurações gerais
SETTINGS = {
    'timeout': 15,
    'retry_attempts': 3,
}
