"""
📋 CONFIGURAÇÕES DO BOT - VERSÃO MELHORADA
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

# Séries FRED - VERSÃO MELHORADA 🇧🇷
FRED_SERIES = {
    # ... (todo o seu conteúdo atual permanece igual)
}

# Configurações gerais
SETTINGS = {
    'timeout': 15,
    'retry_attempts': 3,
}

# ✅ NOVO: Criptomoedas para monitorar
CRIPTO_MONITORAR = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD", 
    "Solana": "SOL-USD",
    "Cardano": "ADA-USD",
}

# ✅ NOVO: Configurações de cripto
CRIPTO_CONFIG = {
    'alertas_24h': True,
    'variacao_alerta': 5,  # % para disparar alerta
}
