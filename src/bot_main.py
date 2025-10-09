"""
🤖 BOT CRIPTO - Alertas de Preço em REAIS - ARB CORRIGIDO!
"""

import os
import sys
import yfinance as yf
from datetime import datetime
import time
import pytz
import requests

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(__file__))

from telegram_client import TelegramClient
from config import CRIPTO_ALERTAS, SETTINGS

class CriptoAlertas:
    def __init__(self):
        self.telegram = TelegramClient()
        self.alertas_enviados = set()
        self.fuso_brasil = pytz.timezone('America/Sao_Paulo')
    
    def obter_taxa_dolar_real(self) -> float:
        """Obtém a taxa atual do dólar para real"""
        try:
            ticker = yf.Ticker("USDBRL=X")
            info = ticker.history(period="1d", interval="1m")
            
            if not info.empty:
                taxa = info['Close'].iloc[-1]
                print(f"💵 Taxa USD/BRL: R$ {taxa:.2f}")
                return round(float(taxa), 2)
            else:
                print("⚠️  Usando taxa fixa USD/BRL: 5.38")
                return SETTINGS['dolar_para_real']
                
        except Exception as e:
            print(f"❌ Erro ao buscar taxa dólar: {e}")
            print("⚠️  Usando taxa fixa USD/BRL: 5.38")
            return SETTINGS['dolar_para_real']
    
    def obter_preco_arbitrum_binance(self) -> float:
        """Obtém preço do Arbitrum direto da Binance API"""
        try:
            print("🔍 Buscando ARB na Binance...")
            url = "https://api.binance.com/api/v3/ticker/price"
            params = {"symbol": "ARBUSDT"}  # ARB/USDT na Binance
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                preco_usd = float(data['price'])
                print(f"✅ ARB Binance: ${preco_usd:.4f}")
                return preco_usd
            else:
                print(f"❌ Erro Binance API: {response.status_code}")
                return 0.0
                
        except Exception as e:
            print(f"❌ Erro ao buscar ARB: {e}")
            return 0.0
    
    def obter_preco_cripto_brl(self, simbolo: str, corretor: str = "yfinance") -> float:
        """Obtém preço atual da criptomoeda em REAIS"""
        try:
            if corretor == "binance":
                # Para Arbitrum - usa Binance
                preco_usd = self.obter_preco_arbitrum_binance()
            else:
                # Para outras - usa Yahoo Finance
                ticker = yf.Ticker(simbolo)
                info = ticker.history(period="1d", interval="1m")
                
                if not info.empty:
                    preco_usd = info['Close'].iloc[-1]
                else:
                    return 0.0
            
            if preco_usd > 0:
                # Converte para BRL
                taxa_cambio = self.obter_taxa_dolar_real()
                preco_brl = preco_usd * taxa_cambio
                return round(float(preco_brl), 3)
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
        
        taxa_cambio = self.obter_taxa_dolar_real()
        
        alertas_ativos = []
        relatorio = "📊 **RELATÓRIO CRIPTO - PREÇOS EM REAIS** 🇧🇷\n"
        relatorio += f"🕐 {self.obter_hora_brasil()} (BRT)\n"
        relatorio += f"💵 Taxa USD/BRL: R$ {taxa_cambio:.2f}\n\n"
        
        for nome, info in CRIPTO_ALERTAS.items():
            simbolo = info["simbolo"]
            preco_alvo_brl = info["preco_alvo"]
            emoji = info["emoji"]
            corretor = info.get("corretor", "yfinance")
            
            preco_atual_brl = self.obter_preco_cripto_brl(simbolo, corretor)
            
            if preco_atual_brl > 0:
                # Status atual
                if preco_atual_brl >= preco_alvo_brl:
                    status = "🎯 ATINGIU ALVO!"
                    status_emoji = "🚨"
                else:
                    status = "📉 ABAIXO DO ALVO" 
                    status_emoji = "⏳"
                
                variacao = ((preco_atual_brl - preco_alvo_brl) / preco_alvo_brl) * 100
                
                relatorio += f"{emoji} **{nome}**: R$ {preco_atual_brl:,.3f}\n"
                relatorio += f"   {status_emoji} Alvo: R$ {preco_alvo_brl:,.2f}\n"
                relatorio += f"   📊 Status: {status}\n"
                relatorio += f"   📈 Variação: {variacao:+.2f}%\n\n"
                
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
            
            time.sleep(1)
        
        # Envia alertas
        for alerta in alertas_ativos:
            print(f"📤 Enviando alerta...")
            self.telegram.enviar_mensagem(alerta)
            time.sleep(2)
        
        # Relatório final
        if alertas_ativos:
            relatorio += f"🔔 **{len(alertas_ativos)} ALERTA(S) ATIVADO(S)!**\n"
        else:
            relatorio += "📉 **Nenhum alvo atingido no momento**\n"
        
        relatorio += f"\n🎯 Monitorando {len(CRIPTO_ALERTAS)} alvos"
        
        # Envia relatório
        sucesso = self.telegram.enviar_mensagem(relatorio)
        
        if sucesso:
            print("✅ Relatório enviado!")
        else:
            print("❌ Falha ao enviar")
        
        return len(alertas_ativos)

def main():
    """Função principal"""
    monitor = CriptoAlertas()
    monitor.verificar_alertas()

if __name__ == "__main__":
    main()
