"""
🤖 BOT ALERTAS BOLSA - Versão Melhorada
Simples, rápido e confiável
"""

import os
import json
import requests
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Optional

class BotBolsa:
    def __init__(self, config_file: str = "config.json"):
        self.config = self._carregar_config(config_file)
        self.telegram_token = self.config['telegram']['bot_token']
        self.telegram_chat_id = self.config['telegram']['chat_id']
        
    def _carregar_config(self, config_file: str) -> Dict:
        """Carrega configurações com fallback inteligente"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Substitui variáveis de ambiente
            config['telegram']['bot_token'] = os.getenv(
                'TELEGRAM_BOT_TOKEN', 
                config['telegram']['bot_token'].replace('${TELEGRAM_BOT_TOKEN}', '')
            )
            config['telegram']['chat_id'] = os.getenv(
                'TELEGRAM_CHAT_ID',
                config['telegram']['chat_id'].replace('${TELEGRAM_CHAT_ID}', '')
            )
            
            return config
        except Exception as e:
            print(f"❌ Erro ao carregar config: {e}")
            return self._config_padrao()
    
    def _config_padrao(self) -> Dict:
        """Configuração padrão de fallback"""
        return {
            "telegram": {
                "bot_token": os.getenv('TELEGRAM_BOT_TOKEN', ''),
                "chat_id": os.getenv('TELEGRAM_CHAT_ID', '')
            },
            "acoes": [
                {"ticker": "PETR4.SA", "nome": "Petrobras", "alerta_compra": 35, "alerta_venda": 45},
                {"ticker": "VALE3.SA", "nome": "Vale", "alerta_compra": 60, "alerta_venda": 70}
            ],
            "config": {"intervalo_minutos": 15, "horario_mercado": True}
        }

    def buscar_cotacoes(self) -> List[Dict]:
        """Busca cotações de todas as ações com tratamento robusto"""
        resultados = []
        
        for acao in self.config['acoes']:
            try:
                ticker = yf.Ticker(acao['ticker'])
                historico = ticker.history(period='2d')
                
                if len(historico) < 2:
                    print(f"⚠️  {acao['nome']}: Dados insuficientes")
                    continue
                
                preco_atual = historico['Close'].iloc[-1]
                preco_anterior = historico['Close'].iloc[-2]
                variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
                
                # Verifica alertas
                alerta = self._verificar_alerta(acao, preco_atual)
                
                resultados.append({
                    'nome': acao['nome'],
                    'ticker': acao['ticker'],
                    'preco': preco_atual,
                    'variacao': variacao,
                    'alerta': alerta
                })
                
                print(f"✅ {acao['nome']}: R$ {preco_atual:.2f} ({variacao:+.2f}%)")
                
            except Exception as e:
                print(f"❌ Erro em {acao['nome']}: {e}")
                resultados.append({
                    'nome': acao['nome'],
                    'ticker': acao['ticker'], 
                    'preco': 0,
                    'variacao': 0,
                    'alerta': f"Erro: {str(e)[:50]}"
                })
        
        return resultados

    def _verificar_alerta(self, acao: Dict, preco_atual: float) -> Optional[str]:
        """Verifica se preço atingiu algum alerta"""
        alerta_compra = acao.get('alerta_compra')
        alerta_venda = acao.get('alerta_venda')
        
        if alerta_compra and preco_atual <= alerta_compra:
            return f"🟢 COMPRA! Abaixo de R$ {alerta_compra:.2f}"
        
        if alerta_venda and preco_atual >= alerta_venda:
            return f"🔴 VENDA! Acima de R$ {alerta_venda:.2f}"
        
        # Alerta de proximidade (5%)
        if alerta_compra and preco_atual <= alerta_compra * 1.05:
            return f"⚡ PERTO COMPRA! R$ {alerta_compra:.2f}"
            
        if alerta_venda and preco_atual >= alerta_venda * 0.95:
            return f"⚡ PERTO VENDA! R$ {alerta_venda:.2f}"
        
        return None

    def formatar_mensagem(self, dados: List[Dict]) -> str:
        """Formata mensagem bonita para Telegram"""
        if not dados:
            return "❌ Nenhum dado encontrado"
        
        mensagem = f"📊 **BOLSA AGORA**\n"
        mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        alertas_ativos = []
        
        for acao in dados:
            emoji = "🟢" if acao['variacao'] > 0 else "🔴" if acao['variacao'] < 0 else "⚪"
            
            mensagem += f"{emoji} **{acao['nome']}**\n"
            mensagem += f"💰 R$ {acao['preco']:.2f} "
            mensagem += f"({acao['variacao']:+.2f}%)\n"
            
            if acao['alerta']:
                mensagem += f"🚨 {acao['alerta']}\n"
                alertas_ativos.append(acao['alerta'])
            
            mensagem += "\n"
        
        # Resumo de alertas
        if alertas_ativos:
            mensagem += "---\n"
            mensagem += f"🚨 **ALERTAS ATIVOS:** {len(alertas_ativos)}\n"
        
        mensagem += "📈 Atualizado automaticamente"
        
        return mensagem

    def enviar_telegram(self, mensagem: str) -> bool:
        """Envia mensagem para Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": mensagem,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Erro Telegram: {e}")
            return False

    def executar(self):
        """Executa o bot completo"""
        print("🚀 Iniciando bot de alertas...")
        
        if not self.telegram_token or not self.telegram_chat_id:
            print("❌ Token ou Chat ID não configurados!")
            return
        
        print("📈 Buscando cotações...")
        dados = self.buscar_cotacoes()
        
        print("📝 Formatando mensagem...")
        mensagem = self.formatar_mensagem(dados)
        
        print("📤 Enviando para Telegram...")
        sucesso = self.enviar_telegram(mensagem)
        
        if sucesso:
            print("✅ Mensagem enviada com sucesso!")
        else:
            print("❌ Falha ao enviar mensagem")

def main():
    """Função principal"""
    bot = BotBolsa()
    bot.executar()

if __name__ == "__main__":
    main()
