"""
🤖 BOT CRIPTO - Alertas de Preço para ARB, ATOM, ADA
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
        self.alertas_enviados = set()  # Para evitar alertas duplicados
    
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
    
    def verificar_alertas(self):
        """Verifica se algum preço atingiu o alvo"""
        print(f"🔍 Verificando alertas para {len(CRIPTO_ALERTAS)} criptomoedas...")
        
        alertas_ativos = []
        relatorio = "📊 **RELATÓRIO CRIPTO - ALERTAS**\n"
        relatorio += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        for nome, info in CRIPTO_ALERTAS.items():
            simbolo = info["simbolo"]
            preco_alvo = info["preco_alvo"]
            emoji = info["emoji"]
            
            preco_atual = self.obter_preco_cripto(simbolo)
            
            if preco_atual > 0:
                # Status atual
                status = "✅ ABAIXO" if preco_atual < preco_alvo else "🚨 ATINGIDO"
                variacao = ((preco_atual - preco_alvo) / preco_alvo) * 100
                
                relatorio += f"{emoji} **{nome}**: ${preco_atual:,.2f}\n"
                relatorio += f"   🎯 Alvo: ${preco_alvo:,.2f}\n"
                relatorio += f"   📊 Status: {status}\n"
                relatorio += f"   📈 Variação: {variacao:+.2f}%\n\n"
                
                # Verifica se atingiu o alvo
                if preco_atual >= preco_alvo:
                    chave_alerta = f"{nome}_{preco_alvo}"
                    if chave_alerta not in self.alertas_enviados:
                        alerta_msg = (
                            f"🚨 **ALERTA ATINGIDO!** 🚨\n\n"
                            f"{emoji} **{nome}** atingiu ${preco_atual:,.2f}\n"
                            f"🎯 **Preço alvo**: ${preco_alvo:,.2f}\n"
                            f"📈 **Variação**: {variacao:+.2f}%\n\n"
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
            print(f"📤 Enviando alerta para {alerta.split()[3]}...")  # Pega o nome da cripto
            self.telegram.enviar_mensagem(alerta)
            time.sleep(2)  # Delay entre alertas
        
        # Envia relatório completo
        if alertas_ativos:
            relatorio += f"🔔 **{len(alertas_ativos)} ALERTA(S) ATIVADO(S)!**\n"
        else:
            relatorio += "✅ **Nenhum alerta atingido no momento**\n"
        
        relatorio += f"\n🎯 Monitorando {len(CRIPTO_ALERTAS)} alvos de preço"
        
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
