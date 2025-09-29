import yfinance as yf
import json
import os
import requests
from datetime import datetime

def enviar_telegram(mensagem):
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': mensagem, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

def verificar_alertas():
    with open('alertas_config.json', 'r') as f:
        config = json.load(f)
    
    alertas_acionados = []
    
    for ativo_config in config['alertas']:
        try:
            ticker = yf.Ticker(ativo_config['ativo'])
            historico = ticker.history(period='1d')
            
            if not historico.empty:
                preco_atual = historico['Close'].iloc[-1]
                nome = ativo_config['nome']
                
                if preco_atual <= ativo_config['alerta_compra']:
                    alertas_acionados.append(f"🟢 **COMPRA**: {nome} caiu para R$ {preco_atual:.2f}")
                elif preco_atual >= ativo_config['alerta_venda']:
                    alertas_acionados.append(f"🔴 **VENDA**: {nome} subiu para R$ {preco_atual:.2f}")
                    
        except Exception as e:
            print(f"Erro em {ativo_config['nome']}: {e}")
    
    return alertas_acionados

def main():
    alertas = verificar_alertas()
    if alertas:
        mensagem = "🚨 **ALERTAS**\n\n" + "\n".join(alertas)
        enviar_telegram(mensagem)

if __name__ == "__main__":
    main()
