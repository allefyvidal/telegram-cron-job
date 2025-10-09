"""
💎💎💎💎💎 CRIPTO 💎💎💎💎💎💎💎
"""

import os
import sys
import yfinance as yf
from datetime import datetime
import time

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(__file__))

from telegram_client import TelegramClient
from config import CRIPTO_ALERTAS, SETTINGS

class CriptoAlertas:
    def __init__(self):
        self.telegram = TelegramClient()
        self.alertas_enviados = set()
        self.taxa_cambio = self.obter_taxa_dolar_real()
    
    def obter_taxa_dolar_real(self) -> float:
        """Obtém a taxa atual do dólar para real"""
        try:
            # Usa o par USD-BRL do Yahoo Finance
            ticker = yf.Ticker("USDBRL=X")
            info = ticker.history(period="1d", interval="1m")
            
            if not info.empty:
                taxa = info['Close'].iloc[-1]
                print(f"💵 Taxa USD/BRL: R$ {taxa:.2f}")
                return round(float(taxa), 2)
            else:
                print("⚠️  Usando taxa padrão USD/BRL: 5.40")
                return SETTINGS['dolar_para_real']
                
        except Exception as e:
            print(f"❌ Erro ao buscar taxa dólar: {e}")
            print("⚠️  Usando taxa padrão USD/BRL: 5.40")
            return SETTINGS['dolar_para_real']
    
    def obter_preco_cripto_brl(self, simbolo: str) -> float:
        """Obtém preço atual da criptomoeda em REAIS"""
        try:
            # Obtém preço em USD
            ticker = yf.Ticker(simbolo)
            info = ticker.history(period="1d", interval="1m")
            
            if not info.empty:
                preco_usd = info['Close'].iloc[-1]
                # Converte para BRL
                preco_brl = preco_usd * self.taxa_cambio
                return round(float(preco_brl), 4)
            return 0.0
            
        except Exception as e:
            print(f"❌ Erro ao buscar {simbolo}: {e}")
            return 0.0
    
    def verificar_alertas(self):
        """Verifica se algum preço atingiu o alvo EM REAIS"""
        print(f"🔍 Verificando alertas para {len(CRIPTO_ALERTAS)} criptomoedas...")
        print(f"💵 Taxa USD/BRL atual: R$ {self.taxa_cambio:.2f}")
        
        alertas_ativos = []
        relatorio = "📊 **RELATÓRIO CRIPTO - PREÇOS EM REAIS**\n"
        relatorio += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        relatorio += f"💵 Taxa USD/BRL: R$ {self.taxa_cambio:.2f}\n\n"
        
        for nome, info in CRIPTO_ALERTAS.items():
            simbolo = info["simbolo"]
            preco_alvo_brl = info["preco_alvo"]  # Já está em BRL
            emoji = info["emoji"]
            
            preco_atual_brl = self.obter_preco_cripto_brl(simbolo)
            
            if preco_atual_brl > 0:
                # Status atual
                status = "✅ ABAIXO" if preco_atual_brl < preco_alvo_brl else "🚨 ATINGIDO"
                variacao = ((preco_atual_brl - preco_alvo_brl) / preco_alvo_brl) * 100
                
                relatorio += f"{emoji} **{nome}**: R$ {preco_atual_brl:,.2f}\n"
                relatorio += f"   🎯 Alvo: R$ {preco_alvo_brl:,.2f}\n"
                relatorio += f"   📊 Status: {status}\n"
                relatorio += f"   📈 Variação: {variacao:+.2f}%\n\n"
                
                # Verifica se atingiu o alvo
                if preco_atual_brl >= preco_alvo_brl:
                    chave_alerta = f"{nome}_{preco_alvo_brl}"
                    if chave_alerta not in self.alertas_enviados:
                        alerta_msg = (
                            f"🚨 **ALERTA ATINGIDO!** 🚨\n\n"
                            f"{emoji} **{nome}** atingiu R$ {preco_atual_brl:,.2f}\n"
                            f"🎯 **Preço alvo**: R$ {preco_alvo_brl:,.2f}\n"
                            f"📈 **Variação**: {variacao:+.2f}%\n"
                            f"💵 **USD/BRL**: R$ {self.taxa_cambio:.2f}\n\n"
                            f"💡 _Hora de considerar realizar lucros!_"
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
            relatorio += "✅ **Nenhum alerta atingido no momento**\n"
        
        relatorio += f"\n🎯 Monitorando {len(CRIPTO_ALERTAS)} alvos de preço em REAIS"
        
        # Envia relatório
        sucesso = self.telegram.enviar_mensagem(relatorio)
        
        if sucesso:
            print("✅ Relatório enviado com sucesso!")
        else:
            print("❌ Falha ao enviar relatório")
        
        return len(alertas_ativos)
    
    def executar_monitoramento_continuo(self):
        """Executa monitoramento contínuo (para teste local)"""
        print("🚀 Iniciando monitoramento contínuo de criptomoedas...")
        print("💵 Preços em REAIS (BRL)")
        print("⏰ Verificando a cada 60 segundos")
        print("🛑 Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                alertas = self.verificar_alertas()
                if alertas > 0:
                    print(f"🚨 {alertas} alerta(s) enviado(s)!")
                
                print(f"⏳ Próxima verificação em {SETTINGS['check_interval']} segundos...\n")
                time.sleep(SETTINGS['check_interval'])
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoramento interrompido pelo usuário")

def main():
    """Função principal"""
    monitor = CriptoAlertas()
    
    # Para GitHub Actions - executa uma vez
    if os.getenv('GITHUB_ACTIONS'):
        monitor.verificar_alertas()
    else:
        # Para teste local - executa continuamente
        monitor.executar_monitoramento_continuo()

if __name__ == "__main__":
    main()
