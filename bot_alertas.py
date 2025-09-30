import yfinance as yf
import json
import os
import requests
from datetime import datetime

def enviar_telegram(mensagem):
    """Envia mensagem para Telegram"""
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }
    
    requests.post(url, json=payload)

def formatar_porcentagem(valor):
    """Formata porcentagem com cor"""
    if valor > 0:
        return f"🟢 +{valor:.2f}%"
    elif valor < 0:
        return f"🔴 {valor:.2f}%"
    else:
        return f"⚪ {valor:.2f}%"

def buscar_precos_acoes():
    """Busca preços atuais e variação"""
    with open('alertas_config.json', 'r') as f:
        config = json.load(f)
    
    relatorio = []
    
    for ativo_config in config['alertas']:
        try:
            ticker = yf.Ticker(ativo_config['ativo'])
            # Busca dados dos últimos 2 dias para calcular variação
            historico = ticker.history(period='2d')
            
            if len(historico) >= 2:
                preco_atual = historico['Close'].iloc[-1]
                preco_anterior = historico['Close'].iloc[-2]
                
                # Calcula variação percentual
                variacao_percentual = ((preco_atual - preco_anterior) / preco_anterior) * 100
                
                relatorio.append({
                    'nome': ativo_config['nome'],
                    'preco_atual': preco_atual,
                    'variacao': variacao_percentual
                })
                
                print(f"✅ {ativo_config['nome']}: R$ {preco_atual:.2f} ({variacao_percentual:+.2f}%)")
            else:
                print(f"❌ {ativo_config['nome']}: Sem dados históricos")
                    
        except Exception as e:
            print(f"❌ Erro ao buscar {ativo_config['nome']}: {e}")
    
    return relatorio

def criar_mensagem_relatorio(relatorio):
    """Cria mensagem formatada para Telegram"""
    if not relatorio:
        return "❌ Erro ao buscar dados das ações"
    
    mensagem = "📊 **BOLSA AGORA**\n"
    mensagem += f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    
    for acao in relatorio:
        mensagem += f"**{acao['nome']}**\n"
        mensagem += f"💰 R$ {acao['preco_atual']:.2f} {formatar_porcentagem(acao['variacao'])}\n\n"
    
    mensagem += "---\n"
    mensagem += "🟢 Alta | 🔴 Baixa | ⚪ Estável\n"
    mensagem += "🔄 Atualizado a cada 15min"
    
    return mensagem

def main():
    print("📈 Buscando cotações da bolsa...")
    relatorio = buscar_precos_acoes()
    
    if relatorio:
        mensagem = criar_mensagem_relatorio(relatorio)
        enviar_telegram(mensagem)
        print("✅ Relatório enviado com sucesso!")
    else:
        print("❌ Nenhum dado encontrado")

if __name__ == "__main__":
    main()
