"""
💬 FORMATADOR DE MENSAGENS - VERSÃO MELHORADA
"""

from datetime import datetime

class MessageFormatter:
    @staticmethod
    def formatar_indicador(indicador: dict) -> str:
        """Formata um indicador individual com formatação inteligente"""
        nome = indicador['nome']
        valor = indicador['valor']
        
        # FORMATAÇÃO ESPECÍFICA POR TIPO DE DADO
        if nome == 'Dólar':
            return f"💵 **Dólar**: R$ {valor:.2f}"
        elif nome == 'Dólar Mensal':
            return f"📅 **Dólar Mensal**: R$ {valor:.2f}"
        elif nome == 'Câmbio Real Efetivo':
            return f"🌎 **Câmbio Real**: {valor:.1f}"
        elif nome == 'Taxa Juros Brasil':
            return f"🏦 **Juros Brasil**: {valor:.2f}%"
        elif nome == 'Juros Interbancário':
            return f"💳 **Juros Interbancário**: {valor:.2f}%"
        elif nome == 'Inflação Brasil':
            return f"📈 **Inflação Brasil**: {valor:.1f}%"
        elif nome == 'PIB Real Brasil':
            # Converte para bilhões e formata
            pib_bilhoes = valor / 1000
            return f"📊 **PIB Real**: R$ {pib_bilhoes:,.1f} bi"
        elif nome == 'PIB Nominal Brasil':
            pib_bilhoes = valor / 1000
            return f"💰 **PIB Nominal**: R$ {pib_bilhoes:,.1f} bi"
        elif nome == 'PIB per Capita':
            return f"👤 **PIB per Capita**: US$ {valor:,.0f}"
        elif nome == 'Desemprego Brasil':
            return f"📉 **Desemprego**: {valor:.1f}%"
        elif nome == 'Produção Industrial':
            return f"🏭 **Produção Industrial**: {valor:.1f}"
        elif nome == 'IPCA':
            return f"🛒 **IPCA**: {valor:.2f}%"
        elif nome == 'Bitcoin':
            return f"₿ **Bitcoin**: US$ {valor:,.0f}"
        elif nome == 'Selic':
            return f"🇧🇷 **Selic**: {valor:.2f}%"
        else:
            # Formatação genérica para outros valores
            if abs(valor) >= 1000000:
                return f"📊 **{nome}**: {valor:,.1f}"
            elif abs(valor) >= 1000:
                return f"📊 **{nome}**: {valor:,.0f}"
            elif abs(valor) >= 1:
                return f"📊 **{nome}**: {valor:.2f}"
            else:
                return f"📊 **{nome}**: {valor:.4f}"
    
    @staticmethod
    def criar_relatorio(dados: list, fonte: str = "Múltiplas Fontes") -> str:
        """Cria relatório completo formatado"""
        if not dados:
            return "❌ Nenhum dado encontrado hoje"
        
        mensagem = f"📊 **RELATÓRIO ECONÔMICO**\n"
        mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        # Agrupa por categoria
        categorias = {}
        for item in dados:
            cat = item.get('categoria', 'Econômico')
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
