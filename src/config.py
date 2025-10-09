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
        "simbolo": "ARB-USD",  # VOLTEI para USD mas convertemos!
        "preco_alvo": 2.40,    # EM REAIS
        "emoji": "🔵"
    },
    "Cosmos": {
        "simbolo": "ATOM-USD", # VOLTEI para USD mas convertemos!
        "preco_alvo": 24.86,   # EM REAIS
        "emoji": "⚛️"
    },
    "Cardano": {
        "simbolo": "ADA-USD",  # VOLTEI para USD mas convertemos!
        "preco_alvo": 4.70,    # EM REAIS
        "emoji": "🔷"
    }
}

# Configurações
SETTINGS = {
    'timeout': 15,
    'check_interval': 60,
    'dolar_para_real': 5.37,  # Taxa fixa que funcionou
}
