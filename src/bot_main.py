"""
🤖 BOT CRIPTO - CoinGecko API (FUNCIONA!)
"""

import os
import sys
import requests
from datetime import datetime
import time
import pytz

sys.path.append(os.path.dirname(__file__))

from telegram_client import TelegramClient
from config import CRIPTO_ALERTAS, SETTINGS

class CriptoAlertas:
    def __init__(self):
        self.telegram = TelegramClient()
        self.alertas_enviados = set()
        self.fuso_brasil = pytz.timezone('America/Sao_Paulo')
        self.coingecko_url = "https://api.coingecko.com/api/v3/simple/price"
    
    def obter_preco_coingecko(self, coin_id: str) -> float:
        """Obtém preço em REAIS direto da CoinGecko"""
        try:
            print(f"🔍 Buscando {coin_id}...")
            
            params = {
                'ids': coin_id,
                'vs_currencies': 'brl',
                'include_last_updated_at': 'true'
            }
            
            response = requests.get(self.coingecko_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if coin_id in data:
                    preco_brl = data[coin_id]['brl']
                    print(f"✅ {coin_id}: R$ {preco_brl:.3f}")
                    return round(float(preco_brl), 3)
                else:
                    print(f"❌ {coin_id} não encontrado")
                    return 0.0
            else:
                print(f"❌ Erro API: {response.status_code}")
                return 0.0
                
        except Exception as e:
            print(f"❌ Erro ao buscar {coin_id}: {e}")
            return 0.0
    
    def obter_hora_brasil(self):
        """Obtém a hora atual no fuso do Brasil"""
        agora = datetime.now(self.fuso_brasil)
        return agora.strftime('%d/%m/%Y %H:%M')
    
    def verificar_alertas(self):
        """Verifica se algum preço atingiu o alvo EM REAIS"""
        print(f"🔍 Verificando {len(CRIPTO_ALERTAS)} criptomoedas via CoinGecko...")
        
        alertas_ativos = []
        relatorio = "📊 **RELATÓRIO CRIPTO - PREÇOS EM REAIS** 🇧🇷\n"
        relatorio += f"🕐 {self.obter_hora_brasil()} (BRT)\n"
        relatorio += f"🔗 Fonte: CoinGecko\n\n"
        
        for nome, info in CRIPTO_ALERTAS.items():
            coin_id = info["id"]
            preco_alvo_brl = info["preco_alvo"]
            emoji = info["emoji"]
            
            preco_atual_brl = self.obter_preco_coingecko(coin_id)
            
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
                            f"🎯 **ALERTA ATINGIDO!** 🚨\n\n"
                            f"{emoji} **{nome}** atingiu R$ {preco_atual_brl:,.3f}\n"
                            f"💰 **Preço alvo**: R$ {preco_alvo_brl:,.2f}\n"
                            f"📈 **Variação**: {variacao:+.2f}%\n\n"
                            f"💡 _Hora de considerar realizar lucros!_ 💰"
                        )
                        alertas_ativos.append(alerta_msg)
                        self.alertas_enviados.add(chave_alerta)
                
            else:
                relatorio += f"❌ **{nome}**: Erro ao buscar preço\n\n"
            
            time.sleep(1)  # Respeitar rate limit
        
        # Envia alertas
        for alerta in alertas_ativos:
            print(f"📤 Enviando alerta para Telegram...")
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
