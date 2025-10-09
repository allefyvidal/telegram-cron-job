"""
🤖 BOT CRIPTO - Versão Simplificada
"""

import os

# Telegram
BOT_CONFIG = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
}

# Criptomoedas para monitorar
CRIPTO_MONITORAR = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD", 
    "Solana": "SOL-USD",
    "Cardano": "ADA-USD",
    "Polygon": "MATIC-USD",
    "Binance Coin": "BNB-USD",
}

# Configurações
SETTINGS = {
    'timeout': 15,
    'variacao_alerta': 3,  # % para alerta de variação
}
