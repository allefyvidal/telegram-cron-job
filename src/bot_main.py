"""
🤖 BOT CRIPTO - Versão Simplificada
"""

import os
import yfinance as yf
from datetime import datetime
from telegram_client import TelegramClient

class BotCripto:
    def __init__(self):
        self.telegram_client = TelegramClient()
        self.criptos = {
            "Bitcoin": "BTC-USD",
            "Ethereum": "ETH-USD", 
            "Solana": "SOL-USD",
            "Cardano": "ADA-USD",
        }
    
    def buscar_criptos(self):
        """Busca cotações das criptomoedas"""
        print("🪙 Buscando criptomoedas...")
        
        dados = []
        for nome, ticker in self.criptos.items():
            try:
                crypto = yf.Ticker(ticker)
                historico = crypto.history(period='2d')
                
                if len(historico) >= 2:
                    preco_atual = historico['Close'].iloc[-1]
                    preco_anterior = historico['Close'].iloc[-2]
                    variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
                    
                    dados.append({
                        'nome': nome,
                        'preco': preco_atual,
                        'variacao': variacao
                    })
                    print(f"✅ {nome}: US$ {preco_atual:.2f} ({variacao:+.2f}%)")
                    
            except Exception as e:
                print(f"❌ Erro em {nome}: {e}")
        
        return dados
    
    def formatar_mensagem(self, dados):
        """Formata mensagem para Telegram"""
        if not dados:
            return "❌ Nenhuma criptomoeda encontrada"
        
        mensagem = "🪙 **CRIPTOMOEDAS**\n"
        mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        for crypto in dados:
            emoji = "🟢" if crypto['variacao'] > 0 else "🔴" if crypto['variacao'] < 0 else "⚪"
            mensagem += f"{emoji} **{crypto['nome']}**: US$ {crypto['preco']:,.2f} "
            mensagem += f"({crypto['variacao']:+.2f}%)\n"
        
        mensagem += f"\n💰 {len(dados)} criptos monitoradas"
        return mensagem
    
    def executar(self):
        """Executa o bot completo"""
        print("🚀 Iniciando Bot Cripto...")
        
        if not all([self.telegram_client.token, self.telegram_client.chat_id]):
            print("❌ Telegram não configurado!")
            return
        
        dados = self.buscar_criptos()
        mensagem = self.formatar_mensagem(dados)
        
        print("📤 Enviando para Telegram...")
        sucesso = self.telegram_client.enviar_mensagem(mensagem)
        
        if sucesso:
            print("✅ Mensagem enviada com sucesso!")
        else:
            print("❌ Falha ao enviar mensagem")

def main():
    bot = BotCripto()
    bot.executar()

if __name__ == "__main__":
    main()
