"""
🤖 BOT CRIPTO - Alertas de Preço para Mitigar Perdas
"""

import os
import sys
import yfinance as yf
from datetime import datetime
import time

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(__file__))

from telegram_client import TelegramClient
from config import CRIPTO_MONITORAR, SETTINGS

class CriptoMonitor:
    def __init__(self):
        self.telegram = TelegramClient()
        self.ultimos_precos = {}
    
    def obter_preco_cripto(self, simbolo: str) -> float:
        """Obtém preço atual da criptomoeda"""
        try:
            ticker = yf.Ticker(simbolo)
            info = ticker.history(period="1d", interval="1m")
            
            if not info.empty:
                preco_atual = info['Close'].iloc[-1]
                return round(float(preco_atual), 4)
            return 0.0
            
        except Exception as e:
            print(f"❌ Erro ao buscar {simbolo}: {e}")
            return 0.0
    
    def calcular_variacao(self, simbolo: str, preco_atual: float) -> float:
        """Calcula variação percentual em relação ao último preço"""
        if simbolo in self.ultimos_precos:
            preco_anterior = self.ultimos_precos[simbolo]
            if preco_anterior > 0:
                variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
                return round(variacao, 2)
        return 0.0
    
    def monitorar_criptos(self):
        """Monitora todas as criptomoedas configuradas"""
        print(f"🔍 Monitorando {len(CRIPTO_MONITORAR)} criptomoedas...")
        
        mensagem = "📊 **RELATÓRIO CRIPTO - PREÇOS ATUAIS**\n"
        mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        alertas = []
        
        for nome, simbolo in CRIPTO_MONITORAR.items():
            preco_atual = self.obter_preco_cripto(simbolo)
            
            if preco_atual > 0:
                # Calcula variação
                variacao = self.calcular_variacao(simbolo, preco_atual)
                self.ultimos_precos[simbolo] = preco_atual
                
                # Formata mensagem
                emoji = "🟢" if variacao >= 0 else "🔴"
                mensagem += f"{emoji} **{nome}**: ${preco_atual:,.2f} "
                mensagem += f"({variacao:+.2f}%)\n"
                
                # Verifica se há alerta (aqui vamos integrar com Google Sheets depois)
                if variacao > SETTINGS['variacao_alerta']:
                    alertas.append(f"🚨 {nome} subiu {variacao}% - ${preco_atual:,.2f}")
            
            else:
                mensagem += f"❌ **{nome}**: Erro ao buscar preço\n"
            
            # Delay para não sobrecarregar a API
            time.sleep(1)
        
        # Adiciona alertas se houver
        if alertas:
            mensagem += "\n🔔 **ALERTAS ATIVOS:**\n"
            for alerta in alertas:
                mensagem += f"• {alerta}\n"
        else:
            mensagem += "\n✅ Nenhum alerta disparado no momento\n"
        
        mensagem += f"\n💡 Monitorando {len(CRIPTO_MONITORAR)} criptomoedas"
        
        return mensagem
    
    def executar_monitoramento(self):
        """Executa o monitoramento completo"""
        try:
            print("🚀 Iniciando monitoramento de criptomoedas...")
            
            mensagem = self.monitorar_criptos()
            
            # Envia para Telegram
            sucesso = self.telegram.enviar_mensagem(mensagem)
            
            if sucesso:
                print("✅ Relatório enviado com sucesso!")
            else:
                print("❌ Falha ao enviar relatório")
                
        except Exception as e:
            print(f"💥 Erro no monitoramento: {e}")

def main():
    """Função principal"""
    monitor = CriptoMonitor()
    monitor.executar_monitoramento()

if __name__ == "__main__":
    main()
