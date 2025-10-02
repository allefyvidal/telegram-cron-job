"""
🤖 BOT ECONÔMICO - FRED API
Dados oficiais do Federal Reserve
"""

import os
import requests
from datetime import datetime

# Configurações
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
FRED_API_KEY = os.getenv('FRED_API_KEY')

# Séries do FRED (verificadas e funcionais)
SERIES_FRED = {
    "Dólar": "DEXBZUS",           # USD/BRL
    "Bitcoin": "CBBTCUSD",        # Bitcoin USD
    "Selic": "SELIC",             # Taxa Selic
    "IPCA": "CPIALTT01BRM659N",   # Inflação
    "PIB Brasil": "BRALOCOSTORSTM", # PIB
}

def buscar_dados_fred():
    """Busca dados econômicos no FRED"""
    resultados = []
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    
    for nome, serie_id in SERIES_FRED.items():
        try:
            print(f"🔍 Buscando {nome}...")
            
            params = {
                'series_id': serie_id,
                'api_key': FRED_API_KEY,
                'file_type': 'json',
                'sort_order': 'desc',
                'limit': 1
            }
            
            response = requests.get(base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                observations = data.get('observations', [])
                
                if observations:
                    ultimo_valor = observations[0].get('value')
                    data_obs = observations[0].get('date')
                    
                    if ultimo_valor and ultimo_valor != '.':
                        resultados.append({
                            'nome': nome,
                            'valor': float(ultimo_valor),
                            'data': data_obs,
                            'serie': serie_id
                        })
                        print(f"   ✅ {nome}: {ultimo_valor}")
                    else:
                        print(f"   ⚠️  {nome}: Sem dados recentes")
                else:
                    print(f"   ❌ {nome}: Nenhum dado encontrado")
            else:
                print(f"   ❌ {nome}: Erro API {response.status_code}")
                
        except Exception as e:
            print(f"   💥 Erro em {nome}: {e}")
    
    return resultados

def formatar_mensagem(dados_fred):
    """Formata mensagem para Telegram"""
    if not dados_fred:
        return "❌ Nenhum dado econômico encontrado hoje"
    
    mensagem = "📊 **DADOS ECONÔMICOS - FRED**\n"
    mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    
    for item in dados_fred:
        if item['nome'] == 'Dólar':
            mensagem += f"💵 **Dólar**: R$ {item['valor']:.2f}\n"
        elif item['nome'] == 'Bitcoin':
            mensagem += f"₿ **Bitcoin**: US$ {item['valor']:,.0f}\n"
        elif item['nome'] == 'Selic':
            mensagem += f"🏦 **Selic**: {item['valor']:.2f}%\n"
        elif item['nome'] == 'IPCA':
            mensagem += f"📈 **IPCA**: {item['valor']:.2f}%\n"
        else:
            mensagem += f"📊 **{item['nome']}**: {item['valor']}\n"
    
    mensagem += f"\n🔗 Fonte: Federal Reserve Bank of St. Louis"
    return mensagem

def enviar_telegram(mensagem):
    """Envia mensagem para Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro Telegram: {e}")
        return False

def main():
    print("🚀 Iniciando bot FRED...")
    
    if not FRED_API_KEY:
        print("❌ FRED_API_KEY não configurada!")
        return
    
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Telegram não configurado!")
        return
    
    # Busca dados
    print("📈 Buscando dados FRED...")
    dados_fred = buscar_dados_fred()
    
    print(f"✅ {len(dados_fred)} indicadores encontrados")
    
    # Formata e envia
    mensagem = formatar_mensagem(dados_fred)
    
    print("📤 Enviando para Telegram...")
    sucesso = enviar_telegram(mensagem)
    
    if sucesso:
        print("✅ Mensagem enviada com sucesso!")
    else:
        print("❌ Falha ao enviar mensagem")

if __name__ == "__main__":
    main()
