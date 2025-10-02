"""
💬 FORMATADOR DE MENSAGENS
"""

from datetime import datetime

class MessageFormatter:
    @staticmethod
    def formatar_indicador(indicador: dict) -> str:
        """Formata um indicador individual"""
        nome = indicador['nome']
        valor = indicador['valor']
        
        if nome == 'Dólar':
            return f"💵 **Dólar**: R$ {valor:.2f}"
        elif nome == 'Bitcoin':
            return f"₿ **Bitcoin**: US$ {valor:,.0f}"
        elif nome == 'Selic':
            return f"🏦 **Selic**: {valor:.2f}%"
        elif nome == 'IPCA':
            return f"📈 **IPCA**: {valor:.2f}%"
        else:
            return f"📊 **{nome}**: {valor}"
    
    @staticmethod
    def criar_relatorio(dados: list, fonte: str = "Múltiplas Fontes") -> str:
        """Cria relatório completo"""
        if not dados:
            return "❌ Nenhum dado encontrado hoje"
        
        mensagem = f"📊 **RELATÓRIO ECONÔMICO**\n"
        mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        # Agrupa por categoria
        categorias = {}
        for item in dados:
            cat = item.get('categoria', 'Geral')
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(item)
        
        # Adiciona por categoria
        for categoria, itens in categorias.items():
            mensagem += f"**{categoria.upper()}:**\n"
            for item in itens:
                mensagem += f"{MessageFormatter.formatar_indicador(item)}\n"
            mensagem += "\n"
        
        mensagem += f"🔗 Fontes: {fonte}"
        return mensagem
