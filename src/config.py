"""
🤖 BOT CRIPTO - Alertas de Preço Personalizados
"""

import os

# Telegram
BOT_CONFIG = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
}

# Criptomoedas com preços-alvo específicos
CRIPTO_ALERTAS = {
    "Arbitrum": {
        "simbolo": "ARB-USD",
        "preco_alvo": 2.40,
        "emoji": "🔵"
    },
    "Cosmos": {
        "simbolo": "ATOM-USD", 
        "preco_alvo": 24.86,
        "emoji": "⚛️"
    },
    "Cardano": {
        "simbolo": "ADA-USD",
        "preco_alvo": 4.70,
        "emoji": "🔷"
    }
}

# Configurações
SETTINGS = {
    'timeout': 15,
    'check_interval': 60,  # Verificar a cada 60 segundos
}
