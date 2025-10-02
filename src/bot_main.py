"""
🤖 BOT PRINCIPAL - Versão Modular
"""

import os
import sys

# Adiciona o src ao path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import API_KEYS, BOT_CONFIG
from src.fred_client import FredClient
from src.telegram_client import TelegramClient
from src.message_formatter import MessageFormatter

class BotEconomico:
    def __init__(self):
        self.fred_client = FredClient()
        self.telegram_client = TelegramClient()
        self.formatter = MessageFormatter()
    
    def coletar_dados(self):
        """Coleta dados de todas as APIs"""
        print("📈 Coletando dados...")
        
        todos_dados = []
        
        # Dados do FRED
        dados_fred = self.fred_client.buscar_todos_dados()
        todos_dados.extend(dados_fred)
        
        # Futuro: Adicionar outras APIs aqui
        # dados_alpha = self.alpha_client.buscar_dados()
        # todos_dados.extend(dados_alpha)
        
        print(f"✅ {len(todos_dados)} indicadores coletados")
        return todos_dados
    
    def executar(self):
        """Executa o bot completo"""
        print("🚀 Iniciando Bot Econômico...")
        
        # Verifica configurações
        if not all([BOT_CONFIG['token'], BOT_CONFIG['chat_id'], API_KEYS['fred']]):
            print("❌ Configurações incompletas!")
            print(f"   BOT_TOKEN: {'✅' if BOT_CONFIG['token'] else '❌'}")
            print(f"   CHAT_ID: {'✅' if BOT_CONFIG['chat_id'] else '❌'}")
            print(f"   FRED_API_KEY: {'✅' if API_KEYS['fred'] else '❌'}")
            return
        
        # Coleta dados
        dados = self.coletar_dados()
        
        # Formata e envia
        mensagem = self.formatter.criar_relatorio(dados, "FRED")
        
        print("📤 Enviando para Telegram...")
        sucesso = self.telegram_client.enviar_mensagem(mensagem)
        
        if sucesso:
            print("✅ Mensagem enviada com sucesso!")
        else:
            print("❌ Falha ao enviar mensagem")

if __name__ == "__main__":
    bot = BotEconomico()
    bot.executar()
