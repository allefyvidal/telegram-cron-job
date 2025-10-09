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
    # 💵 CÂMBIO
    "Dólar": "DEXBZUS",                    # Dólar em tempo real (Diário)
    "Dólar Mensal": "EXBZUS",              # Dólar mensal
    "Câmbio Real Efetivo": "RBBRBIS",      # Câmbio real efetivo
    
    # 🏦 JUROS E INFLAÇÃO  
    "Taxa Juros Brasil": "INTGSTBRM193N",  # Taxa de juros (Selic)
    "Juros Interbancário": "IRSTCI01BRM156N", # Juros overnight
    "Inflação Brasil": "FPCPITOTLZGBRA",   # Inflação anual
    
    # 📊 ECONOMIA REAL
    "PIB Real Brasil": "NGDPRSAXDCBRQ",    # PIB real trimestral
    "PIB Nominal Brasil": "NGDPSAXDCBRQ",  # PIB nominal trimestral
    "PIB per Capita": "NYGDPPCAPKDBRA",    # PIB per capita
    
    # 📈 EMPREGO E PRODUÇÃO
    "Desemprego Brasil": "LRUNTTTTBRM156S", # Taxa de desemprego mensal
    "Produção Industrial": "BRAPROINDMISMEI", # Produção industrial
    "IPCA": "CPALTT01BRM659N",             # IPCA mensal
    
    # 🌎 COMPARAÇÕES INTERNACIONAIS
    "Bitcoin": "CBBTCUSD",                 # Bitcoin em USD
    "Selic": "SELIC",                      # Taxa Selic histórica
}

# Configurações gerais
SETTINGS = {
    'timeout': 15,
    'retry_attempts': 3,
}

# Criptomoedas para monitorar
CRIPTO_MONITORAR = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD", 
    "Solana": "SOL-USD",
    "Cardano": "ADA-USD",
}

# Configurações de cripto
CRIPTO_CONFIG = {
    'alertas_24h': True,
    'variacao_alerta': 5,  # % para disparar alerta
}
