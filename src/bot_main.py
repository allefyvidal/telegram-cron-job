"""
💎💎💎💎💎 CRIPTO 💎💎💎💎💎💎💎
"""

import os
import sys
import yfinance as yf
from datetime import datetime
import time
import pytz  # Adicione esta linha!

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(__file__))

from telegram_client import TelegramClient
from config import CRIPTO_ALERTAS, SETTINGS

class CriptoAlertas:
    def __init__(self):
        self.telegram = TelegramClient()
        self.alertas_enviados = set()
        self.fuso_brasil = pytz.timezone('America/Sao_Paulo')  # Fuso horário correto
    
    def obter_preco_cripto_brl(self, simbolo: str) -> float:
        """Obtém preço atual da criptomoeda em REAIS direto"""
        try:
            ticker = yf.Ticker(simbolo)
            info = ticker.history(period="1d", interval="1m")
            
            if not info.empty:
                preco_brl = info['Close'].iloc[-1]
                return round(float(preco_brl), 3)  # 3 casas decimais para valores baixos
            return 0.0
            
        except Exception as e:
            print(f"❌ Erro ao buscar {simbolo}: {e}")
            return 0.0
    
    def obter_hora_brasil(self):
        """Obtém a hora atual no fuso do Brasil"""
        agora = datetime.now(self.fuso_brasil)
        return agora.strftime('%d/%m/%Y %H:%M')
    
    def verificar_alertas(self):
        """Verifica se algum preço atingiu o alvo EM REAIS"""
        print(f"🔍 Verificando alertas para {len(CRIPTO_ALERTAS)} criptomoedas...")
        
        alertas_ativos = []
        relatorio = "📊 **RELATÓRIO CRIPTO - PREÇOS EM REAIS** 🇧🇷\n"
        relatorio += f"🕐 {self.obter_hora_brasil()} (BRT)\n\n"
        
        for nome, info in CRIPTO_ALERTAS.items():
            simbolo = info["simbolo"]
            preco_alvo_brl = info["preco_alvo"]
            emoji = info["emoji"]
            
            preco_atual_brl = self.obter_preco_cripto_brl(simbolo)
            
            if preco_atual_brl > 0:
                # Status atual - CORRIGIDO os emojis!
                if preco_atual_brl >= preco_alvo_brl:
                    status = "🚨 ATINGIU ALVO!"
                    status_emoji = "🎯"
                else:
                    status = "⏳ ABAIXO DO ALVO"
                    status_emoji = "📉"
                
                variacao = ((preco_atual_brl - preco_alvo_brl) / preco_alvo_brl) * 100
                
                relatorio += f"{emoji} **{nome}**: R$ {preco_atual_brl:,.3f}\n"
                relatorio += f"   {status_emoji} Alvo: R$ {preco_alvo_brl:,.2f}\n"
                relatorio += f"   📊 Status: {status}\n"
                relatorio += f"   📈 Variação do alvo: {variacao:+.2f}%\n\n"
                
                # Verifica se atingiu o alvo
                if preco_atual_brl >= preco_alvo_brl:
                    chave_alerta = f"{nome}_{preco_alvo_brl}"
                    if chave_alerta not in self.alertas_enviados:
                        alerta_msg = (
                            f"🎯 **ALERTA ATINGIDO!** 🎯\n\n"
                            f"{emoji} **{nome}** atingiu R$ {preco_atual_brl:,.3f}\n"
                            f"💰 **Preço alvo**: R$ {preco_alvo_brl:,.2f}\n"
                            f"📈 **Variação**: {variacao:+.2f}%\n\n"
                            f"💡 _Hora de considerar realizar lucros!_ 💰"
                        )
                        alertas_ativos.append(alerta_msg)
                        self.alertas_enviados.add(chave_alerta)
                
            else:
                relatorio += f"❌ **{nome}**: Erro ao buscar preço\n\n"
            
            # Delay para não sobrecarregar a API
            time.sleep(1)
        
        # Envia alertas individuais (mais visíveis)
        for alerta in alertas_ativos:
            print(f"📤 Enviando alerta para {alerta.split()[3]}...")
            self.telegram.enviar_mensagem(alerta)
            time.sleep(2)
        
        # Envia relatório completo
        if alertas_ativos:
            relatorio += f"🔔 **{len(alertas_ativos)} ALERTA(S) ATIVADO(S)!**\n"
        else:
            relatorio += "📉 **Nenhum alvo atingido no momento**\n"
        
        relatorio += f"\n🎯 Monitorando {len(CRIPTO_ALERTAS)} alvos de preço em REAIS"
        
        # Envia relatório
        sucesso = self.telegram.enviar_mensagem(relatorio)
        
        if sucesso:
            print("✅ Relatório enviado com sucesso!")
        else:
            print("❌ Falha ao enviar relatório")
        
        return len(alertas_ativos)

def main():
    """Função principal"""
    monitor = CriptoAlertas()
    monitor.verificar_alertas()

if __name__ == "__main__":
    main()
