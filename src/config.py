"""
🤖 BOT CRIPTO - Alertas de Preço em REAIS
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
        "id": "arbitrum",  # ID na CoinGecko
        "preco_alvo": 2.40,
        "emoji": "🔵"
    },
    "Cosmos": {
        "id": "cosmos", 
        "preco_alvo": 24.86,
        "emoji": "⚛️"
    },
    "Cardano": {
        "id": "cardano",
        "preco_alvo": 4.70,
        "emoji": "🔷"
    }
}

# Configurações
SETTINGS = {
    'timeout': 15,
    'check_interval': 60,
}
