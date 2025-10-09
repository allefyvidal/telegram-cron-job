"""
💎💎💎💎💎 CRIPTO 💎💎💎💎💎💎💎
"""
import os

# Telegram
BOT_CONFIG = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
}

# Criptomoedas com preços-alvo específicos EM REAIS
CRIPTO_ALERTAS = {
    "Arbitrum": {
        "simbolo": "ARB-BRL",  # Mudei para BRL direto!
        "preco_alvo": 2.40,    # EM REAIS
        "emoji": "🔵"
    },
    "Cosmos": {
        "simbolo": "ATOM-BRL",  # Mudei para BRL direto!
        "preco_alvo": 24.86,   # EM REAIS
        "emoji": "⚛️"
    },
    "Cardano": {
        "simbolo": "ADA-BRL",   # Mudei para BRL direto!
        "preco_alvo": 4.70,    # EM REAIS
        "emoji": "🔷"
    }
}

# Configurações
SETTINGS = {
    'timeout': 15,
    'check_interval': 60,
}
