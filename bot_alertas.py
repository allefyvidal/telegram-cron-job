"""
Bot de Alertas do Telegram - Versão Melhorada
Envia alertas de ações da bolsa brasileira com análise técnica
"""

import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Gerencia configurações do bot"""
    
    def __init__(self, config_file: str = 'alertas_config.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Carrega configurações do arquivo JSON"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Arquivo {self.config_file} não encontrado")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Retorna configuração padrão"""
        return {
            "telegram": {
                "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
                "chat_id": os.getenv("TELEGRAM_CHAT_ID", "")
            },
            "acoes": [
                {"ticker": "PETR4", "preco_alvo_max": 42.00, "preco_alvo_min": 38.00},
                {"ticker": "VALE3", "preco_alvo_max": 65.00, "preco_alvo_min": 60.00},
                {"ticker": "ITUB4", "preco_alvo_max": 32.00, "preco_alvo_min": 28.00}
            ],
            "alertas": {
                "horario_inicio": "09:00",
                "horario_fim": "18:00",
                "dias_semana": [0, 1, 2, 3, 4]
            }
        }
    
    def get_acoes(self) -> List[Dict]:
        """Retorna lista de ações configuradas"""
        return self.config.get('acoes', [])
    
    def get_telegram_config(self) -> Dict:
        """Retorna configurações do Telegram"""
        return self.config.get('telegram', {})


class BolsaAPI:
    """Integração com API de cotações da bolsa"""
    
    def __init__(self):
        self.base_url = "https://brapi.dev/api/quote"
        self.headers = {"User-Agent": "TelegramBot/1.0"}
    
    def obter_cotacao(self, ticker: str) -> Optional[Dict]:
        """
        Obtém cotação atual de uma ação
        
        Args:
            ticker: Código da ação (ex: PETR4)
            
        Returns:
            Dicionário com dados da cotação ou None em caso de erro
        """
        try:
            url = f"{self.base_url}/{ticker}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                resultado = data['results'][0]
                return {
                    'ticker': ticker,
                    'preco': resultado.get('regularMarketPrice'),
                    'variacao': resultado.get('regularMarketChangePercent'),
                    'volume': resultado.get('regularMarketVolume'),
                    'abertura': resultado.get('regularMarketOpen'),
                    'maxima': resultado.get('regularMarketDayHigh'),
                    'minima': resultado.get('regularMarketDayLow'),
                    'fechamento_anterior': resultado.get('regularMarketPreviousClose')
                }
            
            logger.warning(f"Nenhum resultado encontrado para {ticker}")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao obter cotação de {ticker}: {e}")
            return None
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Erro ao processar dados de {ticker}: {e}")
            return None
    
    def calcular_indicadores(self, cotacao: Dict) -> Dict:
        """Calcula indicadores técnicos simples"""
        if not cotacao:
            return {}
        
        preco = cotacao.get('preco', 0)
        abertura = cotacao.get('abertura', preco)
        maxima = cotacao.get('maxima', preco)
        minima = cotacao.get('minima', preco)
        
        # Calcula amplitude do dia
        amplitude = ((maxima - minima) / minima * 100) if minima > 0 else 0
        
        # Posição no range do dia
        if maxima > minima:
            posicao_range = ((preco - minima) / (maxima - minima) * 100)
        else:
            posicao_range = 50
        
        return {
            'amplitude_dia': round(amplitude, 2),
            'posicao_range': round(posicao_range, 2),
            'tendencia': 'ALTA' if preco > abertura else 'BAIXA' if preco < abertura else 'LATERAL'
        }


class TelegramBot:
    """Gerencia envio de mensagens via Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def enviar_mensagem(self, mensagem: str, parse_mode: str = "HTML") -> bool:
        """
        Envia mensagem para o chat configurado
        
        Args:
            mensagem: Texto da mensagem
            parse_mode: Formato (HTML ou Markdown)
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": mensagem,
                "parse_mode": parse_mode
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("Mensagem enviada com sucesso")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False


class AnalisadorAlertas:
    """Analisa cotações e gera alertas"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.bolsa_api = BolsaAPI()
    
    def verificar_alerta(self, acao_config: Dict, cotacao: Dict) -> Optional[str]:
        """
        Verifica se deve gerar alerta para uma ação
        
        Returns:
            String com alerta ou None se não houver alerta
        """
        if not cotacao:
            return None
        
        ticker = acao_config['ticker']
        preco = cotacao.get('preco')
        preco_max = acao_config.get('preco_alvo_max')
        preco_min = acao_config.get('preco_alvo_min')
        
        if preco is None:
            return None
        
        # Verifica se atingiu algum alvo
        if preco_max and preco >= preco_max:
            return f"🔴 ALERTA VENDA: {ticker} atingiu R$ {preco:.2f} (alvo máximo: R$ {preco_max:.2f})"
        
        if preco_min and preco <= preco_min:
            return f"🟢 ALERTA COMPRA: {ticker} atingiu R$ {preco:.2f} (alvo mínimo: R$ {preco_min:.2f})"
        
        return None
    
    def gerar_relatorio_completo(self) -> str:
        """Gera relatório completo de todas as ações"""
        acoes = self.config.get_acoes()
        
        relatorio = f"📊 <b>Relatório de Mercado</b>\n"
        relatorio += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        relatorio += "─" * 40 + "\n\n"
        
        alertas_encontrados = False
        
        for acao_config in acoes:
            ticker = acao_config['ticker']
            cotacao = self.bolsa_api.obter_cotacao(ticker)
            
            if not cotacao:
                relatorio += f"❌ <b>{ticker}</b>: Erro ao obter cotação\n\n"
                continue
            
            # Verifica alertas
            alerta = self.verificar_alerta(acao_config, cotacao)
            if alerta:
                relatorio += f"{alerta}\n"
                alertas_encontrados = True
            
            # Adiciona informações da ação
            preco = cotacao.get('preco', 0)
            variacao = cotacao.get('variacao', 0)
            
            emoji = "🟢" if variacao > 0 else "🔴" if variacao < 0 else "⚪"
            
            relatorio += f"{emoji} <b>{ticker}</b>: R$ {preco:.2f} "
            relatorio += f"({variacao:+.2f}%)\n"
            
            # Indicadores técnicos
            indicadores = self.bolsa_api.calcular_indicadores(cotacao)
            if indicadores:
                relatorio += f"   └ Tendência: {indicadores.get('tendencia', 'N/A')}\n"
                relatorio += f"   └ Amplitude: {indicadores.get('amplitude_dia', 0):.2f}%\n"
            
            relatorio += "\n"
        
        if not alertas_encontrados:
            relatorio += "✅ Nenhum alerta disparado no momento\n"
        
        return relatorio


def main():
    """Função principal do bot"""
    logger.info("Iniciando bot de alertas...")
    
    # Carrega configurações
    config_manager = ConfigManager()
    telegram_config = config_manager.get_telegram_config()
    
    # Valida configurações do Telegram
    bot_token = telegram_config.get('bot_token')
    chat_id = telegram_config.get('chat_id')
    
    if not bot_token or not chat_id:
        logger.error("Token ou Chat ID do Telegram não configurados!")
        logger.info("Configure as variáveis de ambiente TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID")
        return
    
    # Inicializa componentes
    telegram_bot = TelegramBot(bot_token, chat_id)
    analisador = AnalisadorAlertas(config_manager)
    
    # Gera e envia relatório
    try:
        relatorio = analisador.gerar_relatorio_completo()
        sucesso = telegram_bot.enviar_mensagem(relatorio)
        
        if sucesso:
            logger.info("Relatório enviado com sucesso!")
        else:
            logger.error("Falha ao enviar relatório")
            
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        telegram_bot.enviar_mensagem(f"❌ Erro ao gerar relatório: {str(e)}")


if __name__ == "__main__":
    main()
