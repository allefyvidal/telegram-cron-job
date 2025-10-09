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
        "simbolo": "ARB-USD",  
        "preco_alvo": 2.40,    # EM REAIS
        "emoji": "🔵",
        "corretor": "binance"  # Vamos usar API diferente para ARB
    },
    "Cosmos": {
        "simbolo": "ATOM-USD", 
        "preco_alvo": 24.86,   # EM REAIS
        "emoji": "⚛️",
        "corretor": "yfinance"
    },
    "Cardano": {
        "simbolo": "ADA-USD",
        "preco_alvo": 4.70,    # EM REAIS
        "emoji": "🔷",
        "corretor": "yfinance"
    }
}

# Configurações
SETTINGS = {
    'timeout': 15,
    'check_interval': 60,
    'dolar_para_real': 5.38,  # Taxa atual que funcionou
}
